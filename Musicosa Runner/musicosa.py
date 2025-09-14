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
from stage_2_ranking.custom_types import Musicosa as S2Musicosa, Contestant as S2Contestant, \
    Entry as S2Entry, Score as S2Score, StageTwoOutput, StageTwoInput
from stage_2_ranking.execute import execute as execute_stage_2
from stage_2_ranking.stage_input import load_musicosa_from_db as load_s2_musicosa_from_db
from stage_3_templates_pre_gen.custom_types import Musicosa as S3Musicosa, StageThreeOutput, AvatarPairing, \
    StageThreeInput
from stage_3_templates_pre_gen.execute import execute as execute_stage_3
from stage_3_templates_pre_gen.stage_input import load_musicosa_from_db as load_s3_musicosa_from_db, \
    load_avatars_from_db
from stage_4_templates_gen.custom_types import StageFourOutput, StageFourInput, Template as S4Template
from stage_4_templates_gen.execute import execute as execute_stage_4
from stage_4_templates_gen.stage_input import load_templates_from_db
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput, StageFiveInput
from stage_5_videoclips_acquisition.execute import execute as execute_stage_5
from stage_5_videoclips_acquisition.stage_input import load_entries_from_db
from stage_6_video_gen.custom_types import EntryVideoOptions, Timestamp, StageSixOutput, StageSixInput, \
    TransitionOptions, TransitionType
from stage_6_video_gen.execute import execute as execute_stage_6
from stage_6_video_gen.stage_input import load_entries_video_options_from_db

# FLOW CONTROL GATES

CONTINUE_ON_SUCCESS: Literal["c"] = "c"
RETRY: Literal["r"] = "r"
RELOAD_CONFIG: Literal["rc"] = "rc"
RELOAD_DATA: Literal["rd"] = "rd"
RELOAD_CONFIG_AND_DATA: Literal["re"] = "re"
ABORT: Literal["a"] = "a"

type FlowControl = Literal["c", "r", "rc", "rd", "re", "a"]

ERROR_CONTROLS = {RETRY, RELOAD_CONFIG, RELOAD_DATA, RELOAD_CONFIG_AND_DATA, ABORT}

FLOW_GATE_MESSAGES: dict[FlowControl, str] = {
    CONTINUE_ON_SUCCESS: "continue",
    RETRY: "retry",
    RELOAD_CONFIG: "reload config, then retry",
    RELOAD_DATA: "reload data, then retry",
    RELOAD_CONFIG_AND_DATA: "reload config and data, then retry",
    ABORT: "abort"
}


class StageInputCollector[T](Protocol):
    def __call__(self, *, config: Config) -> T:
        pass


class StageExecutor[SI, SO](Protocol):
    def __call__(self, *, config: Config, stage_input: SI) -> SO:
        pass


type ControlGateSurrogate[SI, SO] = StageInputCollector[SI] | StageExecutor[SI, SO]


def flow_control_gate[SI, SO](
        func: ControlGateSurrogate[SI, SO],
        f_args: tuple[Any, ...],
        f_kwargs: dict[str, ...],
        /, *,
        controls: set[FlowControl],
        err_header: str | None = None,
        config_file: str | None = None,
        reload_input: StageInputCollector | None = None
) -> SO | Never:
    """
    :param func: Must have the signature of a StageInputCollector or a StageExecutor (see ControlGateSurrogate)
    :param f_args: func's args
    :param f_kwargs: func's kwargs
    :param controls: Set of flow controls to be performed (see FlowControlType)
    :param err_header: Error header to show if an exception is raised by func
    :param config_file: Config file path used to reload the config
    :param reload_input: A function to be used to reload the stage input (see StageInputCollector)
    :return: func's result or nothing if aborted
    """
    controls = {*controls, ABORT}  # Should always have the option to abort

    # Runtime checks

    func_argspec = inspect.getfullargspec(func)

    if not controls.isdisjoint({RELOAD_CONFIG, RELOAD_CONFIG_AND_DATA}):
        if ((func_argspec.kwonlyargs and func_argspec.kwonlyargs[0] != "config") or
                (func_argspec.args and func_argspec.args[0] != "config") or
                func_argspec.annotations.get("config") != Config):
            raise RuntimeError(f"Function {func} does not match ControlGateSurrogate signature. "
                               f"Expected 'config: Config' as first argument")

    if not controls.isdisjoint({RELOAD_DATA, RELOAD_CONFIG_AND_DATA}):
        if ((func_argspec.kwonlyargs and func_argspec.kwonlyargs[1] != "stage_input") or
                (func_argspec.args and func_argspec.args[1] != "stage_input")):
            raise RuntimeError(f"Function {func} does not match ControlGateSurrogate signature. "
                               f"Expected 'stage_input: Generic[SI]' as second argument when reloading data")

    error_controls = {opt for opt in controls if opt in ERROR_CONTROLS}
    on_error_msg = (f"-|Action required|-\n"
                    f"  {'\n  '.join([f"[{k}] {v}" for k, v in FLOW_GATE_MESSAGES.items() if k in error_controls])}"
                    f"\n")

    on_success_msg = (f"-|Control Gate|-\n"
                      f"  {'\n  '.join([f"[{k}] {v}" for k, v in FLOW_GATE_MESSAGES.items() if k in controls])}"
                      f"\n")

    def handle_common_controls(choice: str, enabled_controls: set[FlowControl]) -> None | Never:
        if choice in enabled_controls:
            if choice == RETRY:
                pass

            if choice == RELOAD_CONFIG or choice == RELOAD_CONFIG_AND_DATA:
                f_kwargs["config"] = load_config(config_file)

            if choice == RELOAD_DATA or choice == RELOAD_CONFIG_AND_DATA:
                f_kwargs["stage_input"] = reload_input(config=f_kwargs["config"])

            if choice == ABORT:
                exit(1)

    success = False
    result = None

    while not success:
        try:
            result = func(*f_args, **f_kwargs)

            if CONTINUE_ON_SUCCESS in controls:
                choice = better_input(on_success_msg,
                                      lambda x: x.lower() in controls,
                                      error_message=lambda x: f"Invalid choice '{x}'")

                if choice == CONTINUE_ON_SUCCESS:
                    success = True

                handle_common_controls(choice, controls)
            else:
                success = True
        except Exception as err:
            print(f"{f"{err_header} {err}" if err_header else err}")
            choice = better_input(on_error_msg,
                                  lambda x: x.lower() in error_controls,
                                  error_message=lambda x: f"Invalid choice '{x}'")

            handle_common_controls(choice, error_controls)

    return result


def custom_gate[SI, SO](
        controls: set[FlowControl],
        err_header: str | None = None,
        config_file: str | None = None,
        reload_input: StageInputCollector | None = None
) -> Callable[[ControlGateSurrogate[SI, SO]], ControlGateSurrogate[SI, SO]]:
    def generator(func: ControlGateSurrogate[SI, SO]) -> ControlGateSurrogate[SI, SO]:
        def wrap(*args: Any, **kwargs: Any) -> SO:
            return flow_control_gate(func, args, kwargs,
                                     controls=controls,
                                     err_header=err_header,
                                     config_file=config_file,
                                     reload_input=reload_input)

        return wrap

    return generator


# Gate decorators

def retry[SI, SO](err_header: str | None = None) -> Callable[
    [ControlGateSurrogate[SI, SO]], ControlGateSurrogate[SI, SO]]:
    return custom_gate(controls={RETRY, ABORT}, err_header=err_header)


def retry_or_reconfig[SI, SO](
        err_header: str | None = None,
        config_file: str | None = None
) -> Callable[[ControlGateSurrogate[SI, SO]], ControlGateSurrogate[SI, SO]]:
    return custom_gate(controls={RETRY, RELOAD_CONFIG, ABORT}, err_header=err_header, config_file=config_file)


def stage_gate[SI, SO](
        err_header: str,
        reload_input: StageInputCollector[SI],
        config_file: str | None = None
) -> Callable[[ControlGateSurrogate[SI, SO]], ControlGateSurrogate[SI, SO]]:
    return custom_gate(controls={CONTINUE_ON_SUCCESS, RETRY, RELOAD_CONFIG, RELOAD_DATA, RELOAD_CONFIG_AND_DATA, ABORT},
                       err_header=err_header,
                       config_file=config_file,
                       reload_input=reload_input)


class NoConfStageExecutor[SI, SO](Protocol):
    def __call__(self, *, stage_input: SI) -> SO:
        ...


def noconf_stage_gate[SI, SO](
        err_header: str,
        reload_input_with_oob_config: Callable[[], SI],
) -> Callable[[NoConfStageExecutor[SI, SO]], NoConfStageExecutor[SI, SO]]:
    def generator(func: NoConfStageExecutor[SI, SO]) -> NoConfStageExecutor[SI, SO]:
        adapted_executor: StageExecutor[SI, SO] = lambda config, stage_input: func(stage_input=stage_input)

        def wrap(*args: Any, **kwargs: Any) -> SO:
            adapted_kwargs = {"config": None, **kwargs}
            adapted_reload_input = lambda config: reload_input_with_oob_config()

            return flow_control_gate(adapted_executor, args, adapted_kwargs,
                                     controls={CONTINUE_ON_SUCCESS, RETRY, RELOAD_DATA, ABORT},
                                     err_header=err_header,
                                     config_file=config_file,
                                     reload_input=adapted_reload_input)

        return wrap

    return generator


if __name__ == '__main__':

    # CONFIGURATION

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    args = parser.parse_args()

    config_file = args.config_file.strip() if args.config_file else None

    try:
        config = load_config(config_file)
    except FileNotFoundError | IOError | TypeError as err:
        print(err)
        exit(1)

    # MUSICOSA PIPELINE

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

    # Pipeline Execution

    musicosa_edition = get_metadata_by_field(MetadataFields.EDITION).value
    musicosa_topic = get_metadata_by_field(MetadataFields.TOPIC).value
    musicosa_organiser = get_metadata_by_field(MetadataFields.ORGANISER).value

    print(f"[MUSICOSA {musicosa_edition}º EDITION]")
    print(f"  Topic: {musicosa_topic}")
    print(f"  Organiser: {musicosa_organiser}")


    # STAGE 1

    @retry_or_reconfig(err_header="[Stage 1 | Input collection ERROR]", config_file=config_file)
    def stage_1_collect_input(*, config: Config) -> StageOneInput:
        submissions = get_submissions_from_forms_folder(config.stage_1.forms_folder,
                                                        config.stage_1.contestant_name_coords,
                                                        config.stage_1.entries_data_coords)
        valid_titles = get_valid_titles(config.stage_1.forms_folder, config.stage_1.valid_titles_file)
        special_entry_topics = get_special_topics_from_db()

        return StageOneInput(submissions=submissions, valid_titles=valid_titles,
                             special_entry_topics=special_entry_topics)


    @stage_gate(err_header="[Stage 1 | Execution ERROR]", config_file=config_file, reload_input=stage_1_collect_input)
    def stage_1_do_execute(*, config: Config, stage_input: StageOneInput) -> StageOneOutput:
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
        stage_1_input: StageOneInput = stage_1_collect_input(config=config)
        stage_1_result: StageOneOutput = stage_1_do_execute(config=config, stage_input=stage_1_input)

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
    def stage_2_collect_input(*, config: Config) -> StageTwoInput:
        if config.start_from == STAGE_TWO:
            return StageTwoInput(musicosa=load_s2_musicosa_from_db())

        s2_contestants: list[S2Contestant] = []

        for contestant in contestant_models:
            contestant_scorings = [s for s in scoring_models if s.contestant.id == contestant.id]
            s2_contestants.append(
                S2Contestant(name=contestant.name,
                             scores=[S2Score(entry_title=scoring.entry.title, value=scoring.score)
                                     for scoring in contestant_scorings]))

        s2_entries = [S2Entry(title=entry.title, author_name=entry.author.name) for entry in entry_models]

        return StageTwoInput(musicosa=S2Musicosa(contestants=s2_contestants, entries=s2_entries))


    @noconf_stage_gate(err_header="[Stage 2 | Execution ERROR]",
                       reload_input_with_oob_config=lambda: stage_2_collect_input(config=config))
    def stage_2_do_execute(*, stage_input: StageTwoInput) -> StageTwoOutput:
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
        stage_2_input: StageTwoInput = stage_2_collect_input(config=config)
        stage_2_result: StageTwoOutput = stage_2_do_execute(stage_input=stage_2_input)

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
    def stage_3_collect_input(*, config: Config) -> StageThreeInput:
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
            musicosa=S3Musicosa(unfulfilled_contestants=unfulfilled_contestants,
                                avatars=available_avatars,
                                entries_index_of_unfulfilled_templates=entries_index_of_unfulfilled_templates,
                                entries_index_of_unfulfilled_video_options=entries_index_of_unfulfilled_video_options))


    @noconf_stage_gate(err_header="[Stage 3 | Execution ERROR]",
                       reload_input_with_oob_config=lambda: stage_3_collect_input(config=config))
    def stage_3_do_execute(*, stage_input: StageThreeInput) -> StageThreeOutput:
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
        stage_3_input: StageThreeInput = stage_3_collect_input(config=config)
        stage_3_result: StageThreeOutput = stage_3_do_execute(stage_input=stage_3_input)

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

    @retry_or_reconfig(err_header="[Stage 4 | Input collection ERROR]", config_file=config_file)
    def stage_4_collect_input(*, config: Config) -> StageFourInput:
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
                              templates=[S4Template(template.entry.id,
                                                    template.entry.title,
                                                    TemplateType.ENTRY if not config.stitch_final_video else (
                                                            TemplateType.ENTRY | TemplateType.PRESENTATION))
                                         for template in template_models],
                              retry_attempts=config.stage_4.gen_retry_attempts,
                              overwrite_templates=config.stage_4.overwrite_templates,
                              overwrite_presentations=config.stage_4.overwrite_presentations)


    @stage_gate(err_header="[Stage 4 | Execution ERROR]", config_file=config_file, reload_input=stage_4_collect_input)
    def stage_4_do_execute(*, config: Config, stage_input: StageFourInput) -> StageFourOutput:
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
        stage_4_input: StageFourInput = stage_4_collect_input(config=config)
        stage_4_result: StageFourOutput = stage_4_do_execute(config=config, stage_input=stage_4_input)


    # STAGE 5

    @retry_or_reconfig(err_header="[Stage 5 | Input collection ERROR]", config_file=config_file)
    def stage_5_collect_input(*, config: Config) -> StageFiveInput:
        if config.start_from > STAGE_ONE:
            return StageFiveInput(artifacts_folder=config.artifacts_folder, quiet_ffmpeg=config.stage_5.quiet_ffmpeg,
                                  entries=load_entries_from_db())

        return StageFiveInput(artifacts_folder=config.artifacts_folder, quiet_ffmpeg=config.stage_5.quiet_ffmpeg,
                              entries=entry_models)


    @stage_gate(err_header="[Stage 5 | Execution ERROR]", config_file=config_file, reload_input=stage_5_collect_input)
    def stage_5_do_execute(*, config: Config, stage_input: StageFiveInput) -> StageFiveOutput:
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
        stage_5_input: StageFiveInput = stage_5_collect_input(config=config)
        stage_5_result: StageFiveOutput = stage_5_do_execute(config=config, stage_input=stage_5_input)


    # STAGE 6

    @retry_or_reconfig(err_header="[Stage 6 | Input collection ERROR]", config_file=config_file)
    def stage_6_collect_input(*, config: Config) -> StageSixInput:
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


    @stage_gate(err_header="[Stage 6 | Execution ERROR]", config_file=config_file, reload_input=stage_6_collect_input)
    def stage_6_do_execute(*, config: Config, stage_input: StageSixInput) -> StageSixOutput:
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
        stage_6_input: StageSixInput = stage_6_collect_input(config=config)
        stage_6_result: StageSixOutput = stage_6_do_execute(config=config, stage_input=stage_6_input)

    # END OF MUSICOSA PIPELINE

    print("")
    print("Pipeline execution completed ✔")
