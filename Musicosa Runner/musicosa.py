import argparse
import inspect
from collections.abc import Callable
from typing import Literal, Never, Protocol, Any, cast

from peewee import PeeweeException

from common.config.config import Config
from common.config.loader import load_config
from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.custom_types import TemplateType, STAGE_ONE, STAGE_TWO, STAGE_THREE, STAGE_FOUR, STAGE_FIVE, STAGE_SIX
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.input.better_input import better_input
from common.model.metadata import get_metadata_by_field
from common.model.models import Contestant, Avatar, Entry, Scoring, VideoOptions, Template, Setting, ContestantStats, \
    EntryStats, SpecialEntryTopic, MetadataFields
from common.naming.identifiers import generate_contestant_uuid5, generate_entry_uuid5
from common.time.utils import parse_time
from stage_1_validation.custom_types import StageOneOutput, StageOneInput
from stage_1_validation.execute import execute as execute_stage_1
from stage_1_validation.stage_input import get_submissions_from_forms_folder, get_valid_titles, \
    get_special_topics_from_db
from stage_2_ranking.custom_types import Musicosa as S2_Musicosa, Contestant as S2_Contestant, \
    Entry as S2_Entry, Score as S2_Score, StageTwoOutput, StageTwoInput
from stage_2_ranking.execute import execute as execute_stage_2
from stage_2_ranking.stage_input import load_musicosa_from_db as load_s2_musicosa_from_db
from stage_3_templates_pre_gen.custom_types import Musicosa as S3_Musicosa, StageThreeOutput, AvatarPairing, \
    StageThreeInput
from stage_3_templates_pre_gen.execute import execute as execute_stage_3
from stage_3_templates_pre_gen.stage_input import load_musicosa_from_db as load_s3_musicosa_from_db, \
    load_avatars_from_db
from stage_4_templates_gen.custom_types import StageFourOutput, StageFourInput, Template as S4_Template
from stage_4_templates_gen.execute import execute as execute_stage_4
from stage_4_templates_gen.stage_input import load_templates_from_db
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput, StageFiveInput
from stage_5_videoclips_acquisition.execute import execute as execute_stage_5
from stage_5_videoclips_acquisition.stage_input import load_entries_from_db
from stage_6_video_gen.custom_types import EntryVideoOptions, Timestamp, StageSixOutput, StageSixInput, \
    TransitionOptions, TransitionType
from stage_6_video_gen.execute import execute as execute_stage_6
from stage_6_video_gen.stage_input import load_entries_video_options_from_db


# PIPELINE STEP FLOW GATE Types

class PipelineStep[D, O](Protocol):
    def __call__(self, config: Config | None, reloadable_data: D | None, *args: Any, **kwargs: Any) -> O:
        pass


type ConfigLoader = Callable[[], Config]
type DataCollector[D] = Callable[[Config], D]

# PIPELINE STEP FLOW GATE Controls

CONTINUE: Literal["c"] = "c"
RETRY: Literal["r"] = "r"
RELOAD_CONFIG: Literal["rc"] = "rc"
RELOAD_DATA: Literal["rd"] = "rd"
RELOAD_CONFIG_AND_DATA: Literal["re"] = "re"
ABORT: Literal["a"] = "a"

type GateControl = Literal["c", "r", "rc", "rd", "re", "a"]

ALLOWED_CONTROLS_ON_ERROR = {RETRY, RELOAD_CONFIG, RELOAD_DATA, RELOAD_CONFIG_AND_DATA, ABORT}

GATE_MESSAGES: dict[GateControl, str] = {
    CONTINUE: "continue",
    RETRY: "retry",
    RELOAD_CONFIG: "reload config, then retry",
    RELOAD_DATA: "reload data, then retry",
    RELOAD_CONFIG_AND_DATA: "reload config and data, then retry",
    ABORT: "abort"
}


# PIPELINE STEP FLOW GATE Definition

def flow_gate[D, O](
        step: PipelineStep[D, O],
        step_args: tuple[Any, ...],
        step_kwargs: dict[str, Any],
        /, *,
        controls: set[GateControl],
        err_header: str | None = None,
        config_loader: ConfigLoader | None = None,
        data_collector: DataCollector[D] | None = None
) -> O | Never:
    """
    :param step: Pipeline step function to be executed (see PipelineStep)
    :param step_args: step's args
    :param step_kwargs: step's kwargs
    :param controls: Set of gate controls that are available to this step (see GateControl)
    :param err_header: Error header to show to the user if an exception is raised by the step
    :param config_loader: Function used to reload the configuration of the step
    :param data_collector: Function to be used to reload the step's data
    :return: step's result or nothing if aborted
    """
    controls = {*controls, ABORT}  # Should always have the option to abort

    # Runtime checks

    if len(inspect.getfullargspec(step).args) < 2:
        raise RuntimeError(f"Step function '{step}' is missing mandatory positional arguments")

    if not controls.isdisjoint({RELOAD_CONFIG, RELOAD_CONFIG_AND_DATA}):
        if config_loader is None:
            raise RuntimeError(f"Step function '{step}' supports config reloading but does not provide a config loader")

    if not controls.isdisjoint({RELOAD_DATA, RELOAD_CONFIG_AND_DATA}):
        if data_collector is None:
            raise RuntimeError(f"Step function '{step}' supports data reloading but does not provide a data collector")

    # Step execution

    config_arg, reloadable_data_arg, *other_args = step_args
    step_result = None

    on_success_msg = (f"-|Pipeline Step Gate|-\n"
                      f"  {'\n  '.join([f"[{k}] {v}" for k, v in GATE_MESSAGES.items() if k in controls])}"
                      f"\n")

    error_controls = {ctrl for ctrl in controls if ctrl in ALLOWED_CONTROLS_ON_ERROR}
    on_error_msg = (f"-|Action required|-\n"
                    f"  {'\n  '.join([f"[{k}] {v}" for k, v in GATE_MESSAGES.items() if k in error_controls])}"
                    f"\n")

    choice = CONTINUE

    while True:
        try:
            step_result = step(config_arg, reloadable_data_arg, *other_args, **step_kwargs)

            if CONTINUE in controls:
                choice = better_input(on_success_msg,
                                      lambda x: x in controls,
                                      error_message=lambda x: f"Invalid choice '{x}'")
        except Exception as err:
            print(f"{err_header} {err}" if err_header else err)
            choice = better_input(on_error_msg,
                                  lambda x: x in error_controls,
                                  error_message=lambda x: f"Invalid choice '{x}'")

        if choice == ABORT:
            exit(1)

        if choice == CONTINUE:
            break

        if choice == RETRY:
            continue

        if choice == RELOAD_CONFIG or choice == RELOAD_CONFIG_AND_DATA:
            config_arg = config_loader()

        if choice == RELOAD_DATA or choice == RELOAD_CONFIG_AND_DATA:
            reloadable_data_arg = data_collector(config_arg)

    return step_result


# PIPELINE STEP FLOW GATE Decorators

def flow_gate_decorator[D, O](
        controls: set[GateControl],
        err_header: str | None = None,
        config_loader: ConfigLoader | None = None,
        data_collector: DataCollector[D] | None = None
) -> Callable[[PipelineStep[D, O]], PipelineStep[D, O]]:
    def generator(step_func: PipelineStep[D, O]) -> PipelineStep[D, O]:
        def wrap(*args: Any, **kwargs: Any) -> O:
            return flow_gate(step_func, args, kwargs,
                             controls=controls,
                             err_header=err_header,
                             config_loader=config_loader,
                             data_collector=data_collector)

        return wrap

    return generator


class RetryPipelineStep[O](Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> O:
        pass


def retry[O](err_header: str | None = None) -> Callable[[PipelineStep[None, O]], RetryPipelineStep[O]]:
    decorator = flow_gate_decorator(controls={RETRY, ABORT}, err_header=err_header)

    def generator(func: PipelineStep[None, O]) -> RetryPipelineStep[O]:
        adapted_step_func: PipelineStep[None, O] = lambda _c, _d, *args, **kwargs: func(*args, **kwargs)

        def wrap(*args: Any, **kwargs: Any) -> O:
            return decorator(adapted_step_func)(None, None, *args, **kwargs)

        return wrap

    return generator


class RetryReconfigPipelineStep[O](Protocol):
    def __call__(self, config: Config, *args: Any, **kwargs: Any) -> O:
        pass


def retry_or_reconfig[O](
        config_loader: ConfigLoader,
        err_header: str | None = None,
) -> Callable[[PipelineStep[None, O]], RetryReconfigPipelineStep[O]]:
    decorator = flow_gate_decorator(controls={RETRY, RELOAD_CONFIG, ABORT},
                                    err_header=err_header,
                                    config_loader=config_loader)

    def generator(func: PipelineStep[None, O]) -> RetryReconfigPipelineStep[O]:
        adapted_step_func: PipelineStep[None, O] = lambda config, _d, *args, **kwargs: func(config, *args, **kwargs)

        def wrap(config: Config, *args: Any, **kwargs: Any) -> O:
            return decorator(adapted_step_func)(config, None, *args, **kwargs)

        return wrap

    return generator


def stage[D, O](
        config_loader: ConfigLoader,
        data_collector: DataCollector[D],
        err_header: str | None = None,
) -> Callable[[PipelineStep[D, O]], PipelineStep[D, O]]:
    return flow_gate_decorator(controls={CONTINUE, RETRY, RELOAD_CONFIG, RELOAD_DATA, RELOAD_CONFIG_AND_DATA, ABORT},
                               err_header=err_header,
                               config_loader=config_loader,
                               data_collector=data_collector)


class ConfiglessStagePipelineStep[O](Protocol):
    def __call__(self, reloadable_data: Any, *args: Any, **kwargs: Any) -> O:
        pass


def configless_stage[D, O](
        data_collector: DataCollector[D],
        err_header: str | None = None
) -> Callable[[PipelineStep[D, O]], ConfiglessStagePipelineStep[O]]:
    decorator = flow_gate_decorator(controls={CONTINUE, RETRY, RELOAD_DATA, ABORT},
                                    err_header=err_header,
                                    data_collector=data_collector)

    def generator(func: PipelineStep[D, O]) -> ConfiglessStagePipelineStep[O]:
        adapted_step_func: PipelineStep[D, O] = lambda _c, data, *args, **kwargs: func(data, *args, **kwargs)

        def wrap(data: D, *args: Any, **kwargs: Any) -> O:
            return decorator(adapted_step_func)(None, data, *args, **kwargs)

        return wrap

    return generator


if __name__ == '__main__':

    # CONFIGURATION

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    args = parser.parse_args()

    config_file = args.config_file.strip() if args.config_file else None
    config_loader: ConfigLoader = lambda: load_config(config_file)

    try:
        config = config_loader()
    except FileNotFoundError | IOError | TypeError as err:
        print(err)
        exit(1)

    # Pipeline state

    # Pipeline State

    avatar_pairings: list[AvatarPairing] = []
    contestant_models: list[Contestant] = []
    entry_models: list[Entry] = []
    scoring_models: list[Scoring] = []
    contestant_stats_models: list[ContestantStats] = []
    entry_stats_models: list[EntryStats] = []
    template_models: list[Template] = []
    setting_models: list[Setting] = []
    video_options_models: list[VideoOptions] = []

    # Helper indexes (pre-populated from DB when starting after STAGE 1)

    contestants_by_name: dict[str, Contestant] = {}
    if config.start_from > STAGE_ONE:
        loaded_contestants = [contestant.to_domain() for contestant in Contestant.ORM.select()]
        contestants_by_name = dict([(contestant.name, contestant) for contestant in loaded_contestants])

    entries_by_title: dict[str, Entry] = {}
    if config.start_from > STAGE_ONE:
        loaded_entries = [entry.to_domain() for entry in Entry.ORM.select()]
        entries_by_title = dict([(entry.title, entry) for entry in loaded_entries])

    # PIPELINE EXECUTION

    musicosa_edition = get_metadata_by_field(MetadataFields.EDITION).value
    musicosa_topic = get_metadata_by_field(MetadataFields.TOPIC).value
    musicosa_organiser = get_metadata_by_field(MetadataFields.ORGANISER).value

    print(f"[MUSICOSA {musicosa_edition}º EDITION]")
    print(f"  Topic: {musicosa_topic}")
    print(f"  Organiser: {musicosa_organiser}")


    # STAGE 1

    @retry_or_reconfig(err_header="[Stage 1 | Input collection ERROR]", config_loader=config_loader)
    def stage_1_collect_input(config: Config) -> StageOneInput:
        submissions = get_submissions_from_forms_folder(config.stage_1.forms_folder,
                                                        config.stage_1.contestant_name_coords,
                                                        config.stage_1.entries_data_coords)
        valid_titles = get_valid_titles(config.stage_1.forms_folder, config.stage_1.valid_titles_file)
        special_entry_topics = get_special_topics_from_db()

        return StageOneInput(submissions=submissions,
                             valid_titles=valid_titles,
                             special_entry_topics=special_entry_topics)


    @stage(err_header="[Stage 1 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_1_collect_input)
    def stage_1_do_execute(config: Config, stage_input: StageOneInput) -> StageOneOutput:
        submissions, valid_titles, special_entry_topics = (
            stage_input.submissions, stage_input.valid_titles, stage_input.special_entry_topics)

        result = execute_stage_1(submissions=submissions, valid_titles=valid_titles,
                                 special_entry_topics=special_entry_topics)

        print("")
        print("[STAGE 1 SUMMARY | Submissions Validation]")
        print(f"  Submission forms folder: '{config.stage_1.forms_folder}'")
        print(f"  # Submission forms loaded: {len(submissions)}")
        print(f"  Valid titles file: '{config.stage_1.valid_titles_file}'")
        print("")
        print("Validation errors:")
        if result.validation_errors:
            for validation_error in result.validation_errors:
                print(f"  {validation_error}")
        else:
            print("  All submissions are valid ✔")
        print("")
        contestant_names = [sub.name for sub in submissions]
        print(f"Contestants ({len(contestant_names)}): {", ".join(contestant_names)}")
        for index, name in enumerate(contestant_names):
            if len(submissions[index].entries) >= 3:
                print("")
                print(f"[{name} ({len(submissions[index].entries)})] - Entries sample")
                for entry in submissions[index].entries[0:3]:
                    print(f"    {entry}")
        print("")

        return result


    if config.start_from <= STAGE_ONE:
        stage_1_input: StageOneInput = stage_1_collect_input(config)
        stage_1_result: StageOneOutput = stage_1_do_execute(config, stage_1_input)

        # Update pipeline state

        for sub in stage_1_input.submissions:
            new_contestant = Contestant(id=generate_contestant_uuid5(sub.name).hex, name=sub.name, avatar=None)
            for entry in sub.entries:
                if entry.is_author:
                    # noinspection PyTypeChecker
                    special_topic = SpecialEntryTopic(designation=entry.special_topic) if entry.special_topic else None
                    new_entry = Entry(id=generate_entry_uuid5(entry.title).hex,
                                      title=entry.title,
                                      author=new_contestant,
                                      video_url=entry.video_url,
                                      special_topic=special_topic)

                    if entry.video_timestamp:
                        start, end = entry.video_timestamp.split(VIDEO_TIMESTAMP_SEPARATOR)
                        video_options_models.append(VideoOptions(entry=new_entry,
                                                                 timestamp_start=parse_time(start),
                                                                 timestamp_end=parse_time(end)))

                    entry_models.append(new_entry)
                    entries_by_title[entry.title] = new_entry

            contestant_models.append(new_contestant)
            contestants_by_name[sub.name] = new_contestant

        for sub in stage_1_input.submissions:
            for entry in sub.entries:
                scoring_models.append(Scoring(contestant=contestants_by_name[sub.name],
                                              entry=entries_by_title[entry.title],
                                              score=entry.score))


    # STAGE 2

    @retry(err_header="[Stage 2 | Input collection ERROR]")
    def stage_2_collect_input() -> StageTwoInput:
        if config.start_from == STAGE_TWO:
            return StageTwoInput(musicosa=load_s2_musicosa_from_db())

        s2_contestants: list[S2_Contestant] = []

        for contestant in contestant_models:
            contestant_scorings = [s for s in scoring_models if s.contestant.id == contestant.id]
            s2_contestants.append(
                S2_Contestant(name=contestant.name,
                              scores=[S2_Score(entry_title=scoring.entry.title, value=scoring.score)
                                      for scoring in contestant_scorings]))

        s2_entries = [S2_Entry(title=entry.title, author_name=entry.author.name) for entry in entry_models]

        return StageTwoInput(musicosa=S2_Musicosa(contestants=s2_contestants, entries=s2_entries))


    @configless_stage(err_header="[Stage 2 | Execution ERROR]", data_collector=stage_2_collect_input)
    def stage_2_do_execute(stage_input: StageTwoInput) -> StageTwoOutput:
        musicosa = stage_input.musicosa

        result = execute_stage_2(musicosa=musicosa)

        print("")
        print("[STAGE 2 SUMMARY | Musicosa Ranking]")
        print(f"  # Contestants loaded: {len(musicosa.contestants)}")
        print(f"  # Entries loaded: {len(musicosa.entries)}")
        print("")
        contestant_stats_display = [(stat.contestant.name, stat.avg_given_score, stat.avg_received_score)
                                    for stat in result.contestants_stats]
        print(f"  Contestant stats (name, avg_given_score, avg_received_score): {contestant_stats_display}")
        print(f"  # Ranked entries: {len(result.entries_stats)}")
        print("")

        return result


    if config.start_from <= STAGE_TWO:
        stage_2_input: StageTwoInput = stage_2_collect_input()
        stage_2_result: StageTwoOutput = stage_2_do_execute(stage_2_input)

        # Update pipeline state

        contestant_stats_models.extend(
            [ContestantStats(contestant=contestants_by_name[stat.contestant.name],
                             avg_given_score=stat.avg_given_score,
                             avg_received_score=stat.avg_received_score)
             for stat in stage_2_result.contestants_stats])

        entry_stats_models.extend(
            [EntryStats(entry=entries_by_title[stat.entry.title],
                        avg_score=stat.avg_score,
                        ranking_place=stat.ranking_place,
                        ranking_sequence=stat.ranking_sequence)
             for stat in stage_2_result.entries_stats])


    # STAGE 3

    @retry(err_header="[Stage 3 | Input collection ERROR]")
    def stage_3_collect_input() -> StageThreeInput:
        if config.start_from >= STAGE_TWO:
            return StageThreeInput(musicosa=load_s3_musicosa_from_db())

        unfulfilled_contestants = [c for c in contestant_models if c.avatar is None]

        available_avatars: list[Avatar] = load_avatars_from_db()

        entries_index_of_unfulfilled_templates: dict[int, Entry] = (
            dict([(stat.ranking_sequence, stat.entry) for stat in entry_stats_models]))

        entry_ids_with_video_options = [options.entry.id for options in video_options_models]
        entries_index_of_unfulfilled_video_options: dict[int, Entry] = (
            dict([(stat.ranking_sequence, stat.entry)
                  for stat in entry_stats_models
                  if stat.entry.id not in entry_ids_with_video_options]))

        return StageThreeInput(
            musicosa=S3_Musicosa(unfulfilled_contestants=unfulfilled_contestants,
                                 avatars=available_avatars,
                                 entries_index_of_unfulfilled_templates=entries_index_of_unfulfilled_templates,
                                 entries_index_of_unfulfilled_video_options=entries_index_of_unfulfilled_video_options))


    @configless_stage(err_header="[Stage 3 | Execution ERROR]", data_collector=stage_3_collect_input)
    def stage_3_do_execute(stage_input: StageThreeInput) -> StageThreeOutput:
        result = execute_stage_3(musicosa=stage_input.musicosa)

        print("")
        print("[STAGE 3 SUMMARY | Templates Pre-Generation]")
        print("")
        print(f"  # Paired contestants to avatars: {len(result.avatar_pairings) if result.avatar_pairings else 0}")
        print(f"  # Frame settings set: {len(result.frame_settings) if result.frame_settings else 0}")
        print(f"  # Entry templates fulfilled: {len(result.templates) if result.templates else 0}")
        print(f"  # Generation general settings set: "
              f"{len(result.generation_settings) if result.generation_settings else 0}")
        print(f"  # Entry video options fulfilled: {len(result.video_options) if result.video_options else 0}")

        print("")
        print(" [!] Database checkpoint ahead")
        print("")

        return result


    if config.start_from <= STAGE_THREE:
        stage_3_input: StageThreeInput = stage_3_collect_input()
        stage_3_result: StageThreeOutput = stage_3_do_execute(stage_3_input)

        # Update pipeline state

        if stage_3_result.avatar_pairings:
            avatar_pairings.extend(stage_3_result.avatar_pairings)

        if stage_3_result.frame_settings:
            setting_models.extend(stage_3_result.frame_settings)

        if stage_3_result.templates:
            template_models.extend(stage_3_result.templates)

        if stage_3_result.generation_settings:
            setting_models.extend(stage_3_result.generation_settings)

        if stage_3_result.video_options:
            video_options_models.extend(stage_3_result.video_options)

    # DATA PERSISTENCE CHECKPOINT

    if config.start_from <= STAGE_THREE:

        print("")
        print("Checkpointing Musicosa model to database...")

        try:
            with db.atomic():
                if avatar_pairings:
                    for pairing in avatar_pairings:
                        if isinstance(pairing.avatar, Avatar.Insert):
                            paired_avatar_entity = Avatar.ORM.create(**vars(pairing.avatar))
                            contestants_by_name[pairing.contestant.name].avatar = paired_avatar_entity.to_domain()
                        else:
                            contestants_by_name[pairing.contestant.name].avatar = pairing.avatar

                if contestant_models:
                    Contestant.ORM.replace_many(bulk_pack(contestant_models)).execute()

                if entry_models:
                    Entry.ORM.replace_many(bulk_pack(entry_models)).execute()

                if scoring_models:
                    Scoring.ORM.replace_many(bulk_pack(scoring_models)).execute()

                if contestant_stats_models:
                    ContestantStats.ORM.replace_many(bulk_pack(contestant_stats_models)).execute()

                if entry_stats_models:
                    EntryStats.ORM.replace_many(bulk_pack(entry_stats_models)).execute()

                if setting_models:
                    Setting.ORM.replace_many(bulk_pack(setting_models)).execute()

                if template_models:
                    Template.ORM.replace_many(bulk_pack(template_models)).execute()

                if video_options_models:
                    VideoOptions.ORM.replace_many(bulk_pack(video_options_models)).execute()
        except PeeweeException as err:
            print(f"Database checkpoint failed: {err}")
            print("Aborting...")
            exit(1)

        print("Checkpointing done ✔")
        print("")


    # STAGE 4

    @retry_or_reconfig(err_header="[Stage 4 | Input collection ERROR]", config_loader=config_loader)
    def stage_4_collect_input(config: Config) -> StageFourInput:
        if config.start_from == STAGE_FOUR:
            return StageFourInput(templates_api_url=config.stage_4.templates_api_url,
                                  presentations_api_url=config.stage_4.presentations_api_url,
                                  artifacts_folder=config.artifacts_folder,
                                  templates=load_templates_from_db(config.stitch_final_video),
                                  retry_attempts=config.stage_4.gen_retry_attempts,
                                  overwrite_templates=config.stage_4.overwrite_templates,
                                  overwrite_presentations=config.stage_4.overwrite_presentations)

        # noinspection PyTypeChecker
        return StageFourInput(templates_api_url=config.stage_4.templates_api_url,
                              presentations_api_url=config.stage_4.presentations_api_url,
                              artifacts_folder=config.artifacts_folder,
                              templates=[S4_Template(template.entry.id,
                                                     template.entry.title,
                                                     TemplateType.ENTRY if not config.stitch_final_video else (
                                                             TemplateType.ENTRY | TemplateType.PRESENTATION))
                                         for template in template_models],
                              retry_attempts=config.stage_4.gen_retry_attempts,
                              overwrite_templates=config.stage_4.overwrite_templates,
                              overwrite_presentations=config.stage_4.overwrite_presentations)


    @stage(err_header="[Stage 4 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_4_collect_input)
    def stage_4_do_execute(config: Config, stage_input: StageFourInput) -> StageFourOutput:
        result = execute_stage_4(templates_api_url=config.stage_4.templates_api_url,
                                 presentations_api_url=config.stage_4.presentations_api_url,
                                 artifacts_folder=config.artifacts_folder,
                                 templates=stage_input.templates,
                                 retry_attempts=config.stage_4.gen_retry_attempts,
                                 overwrite_templates=config.stage_4.overwrite_templates,
                                 overwrite_presentations=config.stage_4.overwrite_presentations)

        print("")
        print("[STAGE 4 SUMMARY | Templates Generation]")
        print(f"  # Templates to generate: {len(stage_input.templates)}")
        print("")
        print(f"  # Successfully generated templates: "
              f"{len(result.generated_template_titles) if result.generated_template_titles else 0}")
        if result.failed_template_uuids:
            print(f"  Failed to generate templates ['{"', '".join(result.failed_template_uuids)}']")
        print("")

        return result


    if config.start_from <= STAGE_FOUR:
        stage_4_input: StageFourInput = stage_4_collect_input(config)
        stage_4_result: StageFourOutput = stage_4_do_execute(config, stage_4_input)


    # STAGE 5

    @retry_or_reconfig(err_header="[Stage 5 | Input collection ERROR]", config_loader=config_loader)
    def stage_5_collect_input(config: Config) -> StageFiveInput:
        if config.start_from > STAGE_ONE:
            return StageFiveInput(artifacts_folder=config.artifacts_folder, quiet_ffmpeg=config.stage_5.quiet_ffmpeg,
                                  entries=load_entries_from_db())

        return StageFiveInput(artifacts_folder=config.artifacts_folder, quiet_ffmpeg=config.stage_5.quiet_ffmpeg,
                              entries=entry_models)


    @stage(err_header="[Stage 5 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_5_collect_input)
    def stage_5_do_execute(config: Config, stage_input: StageFiveInput) -> StageFiveOutput:
        result = execute_stage_5(artifacts_folder=config.artifacts_folder, quiet_ffmpeg=config.stage_5.quiet_ffmpeg,
                                 entries=stage_input.entries)

        print("")
        print("[STAGE 5 SUMMARY | Videoclips Acquisition]")
        print(f"  # Entries: {len(stage_input.entries)}")
        print("")
        print(
            f"  # Acquired videoclips: {len(result.acquired_videoclip_titles) if result.acquired_videoclip_titles else 0}")
        if result.failed_videoclip_titles:
            print(f"  Failed to acquire videoclips for: ['{"', '".join(result.failed_videoclip_titles)}']")
        print("")

        return result


    if config.start_from <= STAGE_FIVE:
        stage_5_input: StageFiveInput = stage_5_collect_input(config)
        stage_5_result: StageFiveOutput = stage_5_do_execute(config, stage_5_input)


    # STAGE 6

    @retry_or_reconfig(err_header="[Stage 6 | Input collection ERROR]", config_loader=config_loader)
    def stage_6_collect_input(config: Config) -> StageSixInput:
        if config.start_from > STAGE_ONE:
            return StageSixInput(artifacts_folder=config.artifacts_folder,
                                 video_bits_folder=config.stage_6.video_bits_folder,
                                 entries_video_options=load_entries_video_options_from_db(),
                                 overwrite=config.stage_6.overwrite_video_bits,
                                 stitch_final_video=config.stitch_final_video,
                                 final_video_name=config.stage_6.final_video_name,
                                 transition_options=TransitionOptions(config.stage_6.presentation_duration,
                                                                      config.stage_6.transition_duration,
                                                                      cast(TransitionType,
                                                                           config.stage_6.transition_type)),
                                 quiet_ffmpeg=config.stage_6.quiet_ffmpeg,
                                 quiet_ffmpeg_final_video=config.stage_6.quiet_ffmpeg_final_video)

        entries_video_options: list[EntryVideoOptions] = []
        for entry in entry_models:
            entry_id = entry.id
            entry_title = entry.title
            sequence_number = next(s.ranking_sequence for s in entry_stats_models if s.entry.id == entry_id)
            video_options = next(opt for opt in video_options_models if opt.entry.id == entry_id)
            template = next(t for t in template_models if t.entry.id == entry_id)

            entries_video_options.append(EntryVideoOptions(entry_id=entry_id,
                                                           entry_title=entry_title,
                                                           sequence_number=sequence_number,
                                                           timestamp=Timestamp(start=str(video_options.timestamp_start),
                                                                               end=str(video_options.timestamp_end)),
                                                           width=template.video_box_width_px,
                                                           height=template.video_box_height_px,
                                                           position_top=template.video_box_position_top_px,
                                                           position_left=template.video_box_position_left_px))

        return StageSixInput(artifacts_folder=config.artifacts_folder,
                             video_bits_folder=config.stage_6.video_bits_folder,
                             entries_video_options=entries_video_options,
                             overwrite=config.stage_6.overwrite_video_bits,
                             stitch_final_video=config.stitch_final_video,
                             final_video_name=config.stage_6.final_video_name,
                             transition_options=TransitionOptions(config.stage_6.presentation_duration,
                                                                  config.stage_6.transition_duration,
                                                                  cast(TransitionType, config.stage_6.transition_type)),
                             quiet_ffmpeg=config.stage_6.quiet_ffmpeg,
                             quiet_ffmpeg_final_video=config.stage_6.quiet_ffmpeg_final_video)


    @stage(err_header="[Stage 6 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_6_collect_input)
    def stage_6_do_execute(config: Config, stage_input: StageSixInput) -> StageSixOutput:
        result = execute_stage_6(artifacts_folder=config.artifacts_folder,
                                 video_bits_folder=config.stage_6.video_bits_folder,
                                 entries_video_options=stage_input.entries_video_options,
                                 overwrite=config.stage_6.overwrite_video_bits,
                                 stitch_final_video=config.stitch_final_video,
                                 final_video_name=config.stage_6.final_video_name,
                                 transition_options=TransitionOptions(config.stage_6.presentation_duration,
                                                                      config.stage_6.transition_duration,
                                                                      cast(TransitionType,
                                                                           config.stage_6.transition_type)),
                                 quiet_ffmpeg=config.stage_6.quiet_ffmpeg,
                                 quiet_ffmpeg_final_video=config.stage_6.quiet_ffmpeg_final_video)

        print("")
        print("[STAGE 6 SUMMARY | Video Generation]")
        print(f"  # Loaded entries: {len(stage_input.entries_video_options)}")
        print("")
        if result.entries_missing_sources:
            print(f"  Entries missing source files: ['{"', '".join(result.entries_missing_sources)}']")
        print(f"  # Generated video bits: "
              f"{len(result.generated_video_bit_files) if result.generated_video_bit_files else 0}")
        if result.failed_video_bits:
            print(f"  Failed video bits: ['{"', '".join(result.failed_video_bits)}']")
        if config.stitch_final_video:
            print(f"  Final video file: '{result.final_video_file}'")
        print("")

        return result


    if config.start_from <= STAGE_SIX:
        stage_6_input: StageSixInput = stage_6_collect_input(config)
        stage_6_result: StageSixOutput = stage_6_do_execute(config, stage_6_input)

    # END OF MUSICOSA PIPELINE

    print("")
    print("Pipeline execution completed ✔")
