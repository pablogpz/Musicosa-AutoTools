import argparse
import inspect
from collections.abc import Callable
from typing import Literal, Never, Protocol, Any

from peewee import PeeweeException

from common.config.config import Config
from common.config.loader import load_config
from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.custom_types import TemplateType, STAGE_ONE, STAGE_TWO, STAGE_THREE, STAGE_FOUR, STAGE_FIVE, STAGE_SIX
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.formatting.tabulate import tab
from common.input.better_input import better_input
from common.model.metadata import get_metadata_by_field
from common.model.models import Contestant, Avatar, Entry, Scoring, VideoOptions, Template, Setting, ContestantStats, \
    EntryStats, SpecialEntryTopic, MetadataFields
from common.naming.identifiers import generate_contestant_uuid5, generate_entry_uuid5
from common.time.utils import parse_time
from stage_1_validation.custom_types import ContestantSubmission, StageOneOutput, StageOneInput
from stage_1_validation.execute import execute as execute_stage_1
from stage_1_validation.stage_input import get_submissions_from_forms_folder, get_valid_titles, \
    get_special_topics_from_db
from stage_1_validation.summary import stage_summary as stage_1_summary
from stage_2_ranking.custom_types import Musicosa as S2_Musicosa, Contestant as S2_Contestant, \
    Entry as S2_Entry, Score as S2_Score, StageTwoOutput, StageTwoInput
from stage_2_ranking.execute import execute as execute_stage_2
from stage_2_ranking.stage_input import load_musicosa_from_db as load_s2_musicosa_from_db
from stage_2_ranking.summary import stage_summary as stage_2_summary
from stage_3_templates_pre_gen.custom_types import Musicosa as S3_Musicosa, StageThreeOutput, StageThreeInput
from stage_3_templates_pre_gen.execute import execute as execute_stage_3
from stage_3_templates_pre_gen.stage_input import load_musicosa_from_db as load_s3_musicosa_from_db, \
    load_avatars_from_db
from stage_3_templates_pre_gen.summary import stage_summary as stage_3_summary
from stage_4_templates_gen.custom_types import StageFourOutput, StageFourInput, Template as S4_Template
from stage_4_templates_gen.execute import execute as execute_stage_4
from stage_4_templates_gen.stage_input import load_templates_from_db
from stage_4_templates_gen.summary import stage_summary as stage_4_summary
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput, StageFiveInput
from stage_5_videoclips_acquisition.execute import execute as execute_stage_5
from stage_5_videoclips_acquisition.stage_input import load_entries_from_db
from stage_5_videoclips_acquisition.summary import stage_summary as stage_5_summary
from stage_6_video_gen.custom_types import EntryVideoOptions, Timestamp, StageSixOutput, StageSixInput
from stage_6_video_gen.execute import execute as execute_stage_6
from stage_6_video_gen.stage_input import load_entries_video_options_from_db
from stage_6_video_gen.summary import stage_summary as stage_6_summary
from time import sleep


# PIPELINE STEP FLOW GATE Types

class PipelineStep[D, O](Protocol):
    def __call__(self, config: Config | None, reloadable_data: D | None, *args: Any, **kwargs: Any) -> O:
        pass


type ConfigLoader = Callable[[], Config]
type DataCollector[D] = Callable[[Config], D]

# PIPELINE STEP FLOW GATE Controls

CONTINUE: Literal["c"] = "c"
CONTINUE_AND_SKIP: Literal["sk"] = "sk"
RETRY: Literal["r"] = "r"
RELOAD_CONFIG: Literal["rc"] = "rc"
RELOAD_DATA: Literal["rd"] = "rd"
RELOAD_CONFIG_AND_DATA: Literal["re"] = "re"
ABORT: Literal["a"] = "a"

type GateControl = Literal["c", "sk", "r", "rc", "rd", "re", "a"]

ALLOWED_CONTROLS_ON_ERROR = {RETRY, RELOAD_CONFIG, RELOAD_DATA, RELOAD_CONFIG_AND_DATA, ABORT}

GATE_MESSAGES: dict[GateControl, str] = {
    CONTINUE: "continue",
    CONTINUE_AND_SKIP: "continue, skip future continuation breaks",
    RETRY: "retry",
    RELOAD_CONFIG: "reload config, then retry",
    RELOAD_DATA: "reload data, then retry",
    RELOAD_CONFIG_AND_DATA: "reload config and data, then retry",
    ABORT: "abort"
}


# PIPELINE STEP FLOW GATE Definition

class FlowGate:
    _skip_continuation: bool

    def __init__(self):
        self._skip_continuation = False

    def __call__[D, O](self, step: PipelineStep[D, O],
                       step_args: tuple[Any, ...],
                       step_kwargs: dict[str, Any],
                       /, *,
                       controls: set[GateControl],
                       err_header: str | None = None,
                       config_loader: ConfigLoader | None = None,
                       data_collector: DataCollector[D] | None = None) -> O | Never:
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
                raise RuntimeError(
                    f"Step function '{step}' supports config reloading but does not provide a config loader")

        if not controls.isdisjoint({RELOAD_DATA, RELOAD_CONFIG_AND_DATA}):
            if data_collector is None:
                raise RuntimeError(
                    f"Step function '{step}' supports data reloading but does not provide a data collector")

        def adapted_data_collector(config: Config):
            # Adapt for data collectors with and without config dependency
            if len(inspect.getfullargspec(data_collector).args) > 0:
                return data_collector(config)
            else:
                return data_collector()

        # Step execution

        config_arg, reloadable_data_arg, *other_args = step_args
        step_result = None

        on_success_msg = (f"< Pipeline Step Gate >\n"
                          f"{"\n".join([tab(1, f"[{k}] {v}") for k, v in GATE_MESSAGES.items() if k in controls])}"
                          f"\n")

        error_controls = {ctrl for ctrl in controls if ctrl in ALLOWED_CONTROLS_ON_ERROR}
        on_error_msg = (f"< (!) Action required >\n"
                        f"{"\n".join([tab(1, f"[{k}] {v}") for k, v in GATE_MESSAGES.items() if k in error_controls])}"
                        f"\n")

        while True:
            choice = CONTINUE

            try:
                step_result = step(config_arg, reloadable_data_arg, *other_args, **step_kwargs)

                ask_to_continue_on_success = CONTINUE in controls if not self._skip_continuation else False
                if ask_to_continue_on_success:
                    choice = better_input(on_success_msg,
                                          lambda x: x in controls,
                                          error_message=lambda x: f"Invalid choice '{x}'")
            except Exception as error:
                print(f"{err_header} {err}" if err_header else error)
                choice = better_input(on_error_msg,
                                      lambda x: x in error_controls,
                                      error_message=lambda x: f"Invalid choice '{x}'")

            if choice == ABORT:
                exit(1)

            if choice == CONTINUE_AND_SKIP:
                self._skip_continuation = True

            if choice == CONTINUE or choice == CONTINUE_AND_SKIP:
                break

            if choice == RETRY:
                continue

            if choice == RELOAD_CONFIG or choice == RELOAD_CONFIG_AND_DATA:
                config_arg = config_loader()

            if choice == RELOAD_DATA or choice == RELOAD_CONFIG_AND_DATA:
                reloadable_data_arg = adapted_data_collector(config_arg)

        return step_result


flow_gate = FlowGate()


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
        err_header: str | None = None
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


class ConfiglessStagePipelineStep[D, O](Protocol):
    def __call__(self, reloadable_data: D, *args: Any, **kwargs: Any) -> O:
        pass


def configless_stage[D, O](
        data_collector: DataCollector[D],
        err_header: str | None = None
) -> Callable[[PipelineStep[D, O]], ConfiglessStagePipelineStep[D, O]]:
    decorator = flow_gate_decorator(controls={CONTINUE, CONTINUE_AND_SKIP, RETRY, RELOAD_DATA, ABORT},
                                    err_header=err_header,
                                    data_collector=data_collector)

    def generator(func: PipelineStep[D, O]) -> ConfiglessStagePipelineStep[D, O]:
        adapted_step_func: PipelineStep[D, O] = lambda _c, data, *args, **kwargs: func(data, *args, **kwargs)

        def wrap(data: D, *args: Any, **kwargs: Any) -> O:
            return decorator(adapted_step_func)(None, data, *args, **kwargs)

        return wrap

    return generator


def stage[D, O](
        config_loader: ConfigLoader,
        data_collector: DataCollector[D],
        err_header: str | None = None
) -> Callable[[PipelineStep[D, O]], PipelineStep[D, O]]:
    return flow_gate_decorator(
        controls={CONTINUE, CONTINUE_AND_SKIP, RETRY, RELOAD_CONFIG, RELOAD_DATA, RELOAD_CONFIG_AND_DATA, ABORT},
        err_header=err_header,
        config_loader=config_loader,
        data_collector=data_collector)


class PipelineStateManager:
    avatars: list[Avatar]
    new_avatars_paired: list[tuple[Contestant, Avatar.Insert]]
    contestants: list[Contestant]
    entries: list[Entry]
    scoring_entries: list[Scoring]
    contestant_stats_collection: list[ContestantStats]
    entry_stats_collection: list[EntryStats]
    templates: list[Template]
    settings: list[Setting]
    video_options: list[VideoOptions]

    # Helper indices

    entries_by_title: dict[str, Entry]
    contestants_by_name: dict[str, Contestant]

    def __init__(self, populate_helper_indices: bool = False):
        self.avatars = []
        self.new_avatars_paired = []
        self.contestants = []
        self.entries = []
        self.scoring_entries = []
        self.contestant_stats_collection = []
        self.entry_stats_collection = []
        self.templates = []
        self.settings = []
        self.video_options = []

        self.entries_by_title = {}
        self.contestants_by_name = {}

        if populate_helper_indices:
            self.build_helper_indices_from_db()

    def build_helper_indices_from_db(self) -> None:
        contestants = [contestant.to_domain() for contestant in Contestant.ORM.select()]
        self.contestants_by_name = dict([(contestant.name, contestant) for contestant in contestants])

        entries = [entry.to_domain() for entry in Entry.ORM.select()]
        self.entries_by_title = dict([(entry.title, entry) for entry in entries])

    def checkpoint(self):
        try:
            with db.atomic() as tx:
                if len(self.new_avatars_paired) > 0:
                    for contestant, new_avatar in self.new_avatars_paired:
                        inserted_avatar = Avatar.ORM.create(**vars(new_avatar))
                        self.contestants_by_name[contestant.name].avatar = inserted_avatar.to_domain()

                if len(self.contestants) > 0:
                    Contestant.ORM.replace_many(bulk_pack(self.contestants)).execute()

                if len(self.entries) > 0:
                    Entry.ORM.replace_many(bulk_pack(self.entries)).execute()

                if len(self.scoring_entries) > 0:
                    Scoring.ORM.replace_many(bulk_pack(self.scoring_entries)).execute()

                if len(self.contestant_stats_collection) > 0:
                    ContestantStats.ORM.replace_many(bulk_pack(self.contestant_stats_collection)).execute()

                if len(self.entry_stats_collection) > 0:
                    EntryStats.ORM.replace_many(bulk_pack(self.entry_stats_collection)).execute()

                if len(self.settings) > 0:
                    Setting.ORM.replace_many(bulk_pack(self.settings)).execute()

                if len(self.templates) > 0:
                    Template.ORM.replace_many(bulk_pack(self.templates)).execute()

                if len(self.video_options) > 0:
                    VideoOptions.ORM.replace_many(bulk_pack(self.video_options)).execute()
        except PeeweeException as error:
            tx.rollback()
            raise RuntimeError(f"DB transaction was rolled back due to an error: {error}") from error

    def register_submissions(self, submissions: list[ContestantSubmission]) -> None:
        # First iteration. Register new contestants and entries
        for sub in submissions:
            new_contestant = Contestant(id=generate_contestant_uuid5(sub.name).hex, name=sub.name, avatar=None)

            self.contestants.append(new_contestant)
            self.contestants_by_name[sub.name] = new_contestant

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
                        self.video_options.append(VideoOptions(entry=new_entry,
                                                               timestamp_start=parse_time(start),
                                                               timestamp_end=parse_time(end)))

                    self.entries.append(new_entry)
                    self.entries_by_title[entry.title] = new_entry

        # Second iteration. Register scores with helper indices
        for sub in submissions:
            for entry in sub.entries:
                self.scoring_entries.append(Scoring(contestant=self.contestants_by_name[sub.name],
                                                    entry=self.entries_by_title[entry.title],
                                                    score=entry.score))

    def produce_stage_2_input(self) -> StageTwoInput:
        s2_contestants: list[S2_Contestant] = []

        for contestant in self.contestants:
            contestant_scorings = [s for s in self.scoring_entries if s.contestant.id == contestant.id]

            s2_contestants.append(
                S2_Contestant(name=contestant.name,
                              scores=[S2_Score(scoring.entry.title, scoring.score) for scoring in contestant_scorings]))

        s2_entries = [S2_Entry(entry.title, entry.author.name) for entry in self.entries]

        return StageTwoInput(S2_Musicosa(s2_contestants, s2_entries))

    def register_stage_2_output(self, stage_output: StageTwoOutput) -> None:
        self.contestant_stats_collection.extend(
            [ContestantStats(contestant=self.contestants_by_name[stat.contestant.name],
                             avg_given_score=stat.avg_given_score,
                             avg_received_score=stat.avg_received_score)
             for stat in stage_output.contestants_stats])

        self.entry_stats_collection.extend(
            [EntryStats(entry=self.entries_by_title[stat.entry.title],
                        avg_score=stat.avg_score,
                        ranking_place=stat.ranking_place,
                        ranking_sequence=stat.ranking_sequence)
             for stat in stage_output.entries_stats])

    def produce_stage_3_input(self) -> StageThreeInput:
        unfulfilled_contestants = [c for c in self.contestants if c.avatar is None]

        if len(self.avatars) == 0:
            self.avatars = load_avatars_from_db()

        entries_index_of_unfulfilled_templates: dict[int, Entry] = (dict([(stat.ranking_sequence, stat.entry)
                                                                          for stat in self.entry_stats_collection]))

        entry_ids_with_video_options = [options.entry.id for options in self.video_options]
        entries_index_of_unfulfilled_video_options: dict[int, Entry] = (
            dict([(stat.ranking_sequence, stat.entry)
                  for stat in self.entry_stats_collection
                  if stat.entry.id not in entry_ids_with_video_options]))

        return StageThreeInput(
            S3_Musicosa(unfulfilled_contestants, self.avatars, entries_index_of_unfulfilled_templates,
                        entries_index_of_unfulfilled_video_options))

    def register_stage_3_output(self, stage_output: StageThreeOutput) -> None:
        if stage_output.avatar_pairings:
            for pairing in stage_output.avatar_pairings:
                if isinstance(pairing.avatar, Avatar):
                    self.contestants_by_name[pairing.contestant.name].avatar = pairing.avatar
                if isinstance(pairing.avatar, Avatar.Insert):
                    self.new_avatars_paired.append((pairing.contestant, pairing.avatar))

        if stage_output.frame_settings:
            self.settings.extend(stage_output.frame_settings)

        if stage_output.templates:
            self.templates.extend(stage_output.templates)

        if stage_output.generation_settings:
            self.settings.extend(stage_output.generation_settings)

        if stage_output.video_options:
            self.video_options.extend(stage_output.video_options)

    def produce_stage_4_input(self, generate_presentations: bool) -> StageFourInput:
        # noinspection PyTypeChecker
        return StageFourInput([S4_Template(template.entry.id,
                                           template.entry.title,
                                           TemplateType.ENTRY if not generate_presentations else (
                                                   TemplateType.ENTRY | TemplateType.PRESENTATION))
                               for template in self.templates])

    def produce_stage_5_input(self) -> StageFiveInput:
        return StageFiveInput(self.entries)

    def produce_stage_6_input(self) -> StageSixInput:
        entries_video_options: list[EntryVideoOptions] = []

        for entry in self.entries:
            entry_id = entry.id
            entry_title = entry.title
            ranking_place = next(s.ranking_place for s in self.entry_stats_collection if s.entry.id == entry_id)
            sequence_number = next(s.ranking_sequence for s in self.entry_stats_collection if s.entry.id == entry_id)
            video_options = next(opt for opt in self.video_options if opt.entry.id == entry_id)
            template = next(t for t in self.templates if t.entry.id == entry_id)

            entries_video_options.append(
                EntryVideoOptions(entry_id=entry_id,
                                  entry_title=entry_title,
                                  ranking_place=ranking_place,
                                  sequence_number=sequence_number,
                                  timestamp=Timestamp(start=str(video_options.timestamp_start),
                                                      end=str(video_options.timestamp_end)),
                                  width=template.video_box_width_px,
                                  height=template.video_box_height_px,
                                  position_top=template.video_box_position_top_px,
                                  position_left=template.video_box_position_left_px))

        return StageSixInput(entries_video_options)


if __name__ == '__main__':

    # CONFIGURATION

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    arguments = parser.parse_args()

    configuration_file = arguments.config_file.strip() if arguments.config_file else None
    configuration_loader: ConfigLoader = lambda: load_config(configuration_file)

    try:
        configuration = configuration_loader()
    except FileNotFoundError | IOError | TypeError as err:
        print(err)
        exit(1)

    # STATE MANAGEMENT

    state_manager = PipelineStateManager(populate_helper_indices=configuration.start_from > STAGE_ONE)

    # PIPELINE EXECUTION

    musicosa_edition = get_metadata_by_field(MetadataFields.EDITION).value
    musicosa_topic = get_metadata_by_field(MetadataFields.TOPIC).value
    musicosa_organiser = get_metadata_by_field(MetadataFields.ORGANISER).value

    print(f"[MUSICOSA {musicosa_edition}º EDITION]")
    print(f"  Topic: {musicosa_topic}")
    print(f"  Organiser: {musicosa_organiser}")


    # STAGE 1

    @retry_or_reconfig(err_header="[Stage 1 | Input collection ERROR]", config_loader=configuration_loader)
    def stage_1_collect_input(config: Config) -> StageOneInput:
        submissions = get_submissions_from_forms_folder(config.stage_1.forms_folder,
                                                        config.stage_1.contestant_name_coords,
                                                        config.stage_1.entries_data_coords)
        valid_titles = get_valid_titles(config.stage_1.forms_folder, config.stage_1.valid_titles_file)
        special_entry_topics = get_special_topics_from_db()

        return StageOneInput(submissions, valid_titles, special_entry_topics)


    @stage(err_header="[Stage 1 | Execution ERROR]",
           config_loader=configuration_loader,
           data_collector=stage_1_collect_input)
    def stage_1_do_execute(config: Config, stage_input: StageOneInput) -> StageOneOutput:
        result = execute_stage_1(stage_input)

        if result.validation_errors:
            for validation_error in result.validation_errors:
                print(validation_error)

        print(stage_1_summary(config, stage_input))

        return result


    if configuration.start_from <= STAGE_ONE:
        print("")
        print("[STAGE 1 | Submission Validation]")
        print("")

        stage_1_input = stage_1_collect_input(configuration)
        stage_1_do_execute(configuration, stage_1_input)

        state_manager.register_submissions(stage_1_input.submissions)


    # STAGE 2

    @retry(err_header="[Stage 2 | Input collection ERROR]")
    def stage_2_collect_input() -> StageTwoInput:
        if configuration.start_from == STAGE_TWO:
            return StageTwoInput(load_s2_musicosa_from_db())
        else:
            return state_manager.produce_stage_2_input()


    @configless_stage(err_header="[Stage 2 | Execution ERROR]", data_collector=stage_2_collect_input)
    def stage_2_do_execute(stage_input: StageTwoInput) -> StageTwoOutput:
        result = execute_stage_2(stage_input)

        print(stage_2_summary(stage_input, result))

        return result


    if configuration.start_from <= STAGE_TWO:
        print("")
        print("[STAGE 2 | Ranking]")
        print("")

        stage_2_input = stage_2_collect_input()
        stage_2_result = stage_2_do_execute(stage_2_input)

        state_manager.register_stage_2_output(stage_2_result)


    # STAGE 3

    @retry(err_header="[Stage 3 | Input collection ERROR]")
    def stage_3_collect_input() -> StageThreeInput:
        if configuration.start_from >= STAGE_TWO:
            return StageThreeInput(load_s3_musicosa_from_db())
        else:
            return state_manager.produce_stage_3_input()


    @configless_stage(err_header="[Stage 3 | Execution ERROR]", data_collector=stage_3_collect_input)
    def stage_3_do_execute(stage_input: StageThreeInput) -> StageThreeOutput:
        result = execute_stage_3(stage_input)

        print(stage_3_summary(result))

        return result


    if configuration.start_from <= STAGE_THREE:
        print("")
        print("[STAGE 3 | Templates Pre-Generation Fulfillment]")
        print("")
        print(tab(1, "(!) Database checkpoint ahead"))
        print("")
        sleep(1)

        stage_3_input = stage_3_collect_input()
        stage_3_result = stage_3_do_execute(stage_3_input)

        state_manager.register_stage_3_output(stage_3_result)

    # DATA PERSISTENCE CHECKPOINT

    if configuration.start_from <= STAGE_THREE:
        print("")
        print("Checkpointing state to database...")
        print("")

        try:
            state_manager.checkpoint()
        except RuntimeError as err:
            print(f"Database checkpoint failed. Cause: {err}")
            print("Aborting...")
            exit(1)

        print("Checkpointing done ✔")
        print("")


    # STAGE 4

    @retry_or_reconfig(err_header="[Stage 4 | Input collection ERROR]", config_loader=configuration_loader)
    def stage_4_collect_input(config: Config) -> StageFourInput:
        if config.start_from == STAGE_FOUR:
            return StageFourInput(load_templates_from_db(generate_presentations=config.stitch_final_video))
        else:
            return state_manager.produce_stage_4_input(generate_presentations=config.stitch_final_video)


    @stage(err_header="[Stage 4 | Execution ERROR]",
           config_loader=configuration_loader,
           data_collector=stage_4_collect_input)
    def stage_4_do_execute(config: Config, stage_input: StageFourInput) -> StageFourOutput:
        result = execute_stage_4(config, stage_input)

        print(stage_4_summary(config, stage_input, result))

        return result


    if configuration.start_from <= STAGE_FOUR:
        print("")
        print("[STAGE 4 | Templates Generation]")
        print("")

        stage_4_do_execute(configuration, stage_4_collect_input(configuration))


    # STAGE 5

    @retry_or_reconfig(err_header="[Stage 5 | Input collection ERROR]", config_loader=configuration_loader)
    def stage_5_collect_input(config: Config) -> StageFiveInput:
        if config.start_from > STAGE_ONE:
            return StageFiveInput(load_entries_from_db())
        else:
            return state_manager.produce_stage_5_input()


    @stage(err_header="[Stage 5 | Execution ERROR]",
           config_loader=configuration_loader,
           data_collector=stage_5_collect_input)
    def stage_5_do_execute(config: Config, stage_input: StageFiveInput) -> StageFiveOutput:
        result = execute_stage_5(config, stage_input)

        print(stage_5_summary(stage_input, result))

        return result


    if configuration.start_from <= STAGE_FIVE:
        print("")
        print("[STAGE 5 | Videoclips Acquisition]")
        print("")

        stage_5_do_execute(configuration, stage_5_collect_input(configuration))


    # STAGE 6

    @retry_or_reconfig(err_header="[Stage 6 | Input collection ERROR]", config_loader=configuration_loader)
    def stage_6_collect_input(config: Config) -> StageSixInput:
        if config.start_from > STAGE_ONE:
            return StageSixInput(load_entries_video_options_from_db())
        else:
            return state_manager.produce_stage_6_input()


    @stage(err_header="[Stage 6 | Execution ERROR]",
           config_loader=configuration_loader,
           data_collector=stage_6_collect_input)
    def stage_6_do_execute(config: Config, stage_input: StageSixInput) -> StageSixOutput:
        result = execute_stage_6(config, stage_input)

        print(stage_6_summary(config, stage_input, result))

        return result


    if configuration.start_from <= STAGE_SIX:
        print("")
        print("[STAGE 6 | Video Generation]")
        print("")

        stage_6_do_execute(configuration, stage_6_collect_input(configuration))

    print("")
    print("Pipeline execution completed ✔")
    print("")
