import argparse
import inspect
from collections.abc import Callable
from typing import Literal, Never, Protocol, Any

from peewee import PeeweeException

from common.config.config import Config
from common.config.loader import load_config
from common.custom_types import STAGE_ONE, STAGE_TWO, STAGE_THREE, STAGE_FOUR, STAGE_FIVE, STAGE_SIX
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.formatting.tabulate import tab
from common.input.better_input import better_input
from common.model.metadata import get_metadata_by_field
from common.model.models import Template, Setting, NominationStats, \
    CastVote, MetadataFields, Member, Nomination
from common.naming.identifiers import generate_nomination_uuid5_from_nomination_str
from stage_1_validation.custom_types import AwardForm, StageOneOutput, StageOneInput
from stage_1_validation.execute import execute as execute_stage_1
from stage_1_validation.stage_input import parse_award_forms_folder, get_award_count, get_member_count, \
    get_valid_award_slugs
from stage_1_validation.summary import stage_summary as stage_1_summary
from stage_2_ranking.custom_types import StageTwoOutput, StageTwoInput
from stage_2_ranking.execute import execute as execute_stage_2
from stage_2_ranking.stage_input import load_tfa_from_db as load_s2_tfa_from_db
from stage_2_ranking.summary import stage_summary as stage_2_summary
from stage_3_templates_pre_gen.custom_types import StageThreeOutput, StageThreeInput
from stage_3_templates_pre_gen.execute import execute as execute_stage_3
from stage_3_templates_pre_gen.stage_input import load_tfa_from_db as load_s3_tfa_from_db
from stage_3_templates_pre_gen.summary import stage_summary as stage_3_summary
from stage_4_templates_gen.custom_types import StageFourOutput, StageFourInput
from stage_4_templates_gen.execute import execute as execute_stage_4
from stage_4_templates_gen.stage_input import load_templates_from_db
from stage_4_templates_gen.summary import stage_summary as stage_4_summary
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput, StageFiveInput
from stage_5_videoclips_acquisition.execute import execute as execute_stage_5
from stage_5_videoclips_acquisition.stage_input import load_videoclips_from_db
from stage_5_videoclips_acquisition.summary import stage_summary as stage_5_summary
from stage_6_video_gen.custom_types import StageSixOutput, \
    StageSixInput
from stage_6_video_gen.execute import execute as execute_stage_6
from stage_6_video_gen.stage_input import load_video_options_from_db
from stage_6_video_gen.summary import stage_summary as stage_6_summary


# PIPELINE STEP FLOW GATE Types

class PipelineStep[D, O](Protocol):
    def __call__(self, config: Config | None, reloadable_data: D | None, *args: Any, **kwargs: Any) -> O:
        pass


type ConfigLoader = Callable[[], Config]
type DataCollector[D] = Callable[[Config], D] | Callable[[], D]

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
            except Exception as err:
                print(f"{err_header} {err}" if err_header else err)
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
    cast_votes: list[CastVote]
    nomination_stats_collection: list[NominationStats]
    templates: list[Template]
    settings: list[Setting]

    # Helper indices

    members_by_name: dict[str, Member]
    nominations_by_id: dict[str, Nomination]

    def __init__(self):
        self.cast_votes = []
        self.nomination_stats_collection = []
        self.templates = []
        self.settings = []

        self.members_by_name = {}
        self.nominations_by_id = {}

        self.build_helper_indices_from_db()

    def build_helper_indices_from_db(self) -> None:
        members = [member.to_domain() for member in Member.ORM.select()]
        self.members_by_name = dict([(member.name, member) for member in members])

        nominations = [nomination.to_domain() for nomination in Nomination.ORM.select()]
        self.nominations_by_id = dict([(nomination.id, nomination) for nomination in nominations])

    def register_award_forms(self, award_forms: list[AwardForm]) -> None:
        for award in award_forms:
            for submission in award.submissions:
                for cast_vote in submission.cast_votes:
                    nomination_id = (
                        generate_nomination_uuid5_from_nomination_str(cast_vote.nomination, award.award_slug).hex)
                    self.cast_votes.append(
                        CastVote(member=self.members_by_name[submission.name],
                                 nomination=self.nominations_by_id[nomination_id],
                                 score=cast_vote.score))

    def save_cast_votes(self) -> None:
        try:
            with db.atomic() as tx:
                if len(self.cast_votes) > 0:
                    CastVote.ORM.replace_many(bulk_pack(self.cast_votes)).execute()
        except PeeweeException as err:
            tx.rollback()
            raise RuntimeError(f"DB transaction was rolled back due to an error: {err}") from err

    def register_stage_2_output(self, stage_output: StageTwoOutput) -> None:
        for stat in stage_output.nomination_stats:
            self.nomination_stats_collection.append(
                NominationStats(nomination=self.nominations_by_id[stat.nomination_id],
                                avg_score=stat.avg_score,
                                ranking_place=stat.ranking_place,
                                ranking_sequence=stat.ranking_sequence))

    def save_nomination_stats(self) -> None:
        try:
            with db.atomic() as tx:
                if len(self.nomination_stats_collection) > 0:
                    NominationStats.ORM.replace_many(bulk_pack(self.nomination_stats_collection)).execute()
        except PeeweeException as err:
            tx.rollback()
            raise RuntimeError(f"DB transaction was rolled back due to an error: {err}") from err

    def register_stage_3_output(self, stage_output: StageThreeOutput) -> None:
        if stage_output.frame_settings:
            self.settings.extend(stage_output.frame_settings)

        if stage_output.templates:
            self.templates.extend(stage_output.templates)

    def save_settings_and_templates(self) -> None:
        try:
            with db.atomic() as tx:
                if len(self.settings) > 0:
                    Setting.ORM.replace_many(bulk_pack(self.settings)).execute()

                if len(self.templates) > 0:
                    Template.ORM.replace_many(bulk_pack(self.templates)).execute()
        except PeeweeException as err:
            tx.rollback()
            raise RuntimeError(f"DB transaction was rolled back due to an error: {err}") from err


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
        print(f"Config loading error: {err}")
        exit(1)

    # STATE MANAGEMENT

    state_manager = PipelineStateManager()

    # PIPELINE EXECUTION

    tfa_edition = get_metadata_by_field(MetadataFields.EDITION).value

    print(f"[TFA {tfa_edition}º EDITION]")
    print(f"  Edition: {tfa_edition}")


    # STAGE 1

    @retry_or_reconfig(err_header="[Stage 1 | Input collection ERROR]", config_loader=config_loader)
    def stage_1_collect_input(config: Config) -> StageOneInput:
        award_forms = parse_award_forms_folder(config.stage_1.award_forms_folder)
        valid_award_slugs = get_valid_award_slugs()
        awards_count = get_award_count()
        members_count = get_member_count()

        return StageOneInput(award_forms, valid_award_slugs, awards_count, members_count)


    @stage(err_header="[Stage 1 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_1_collect_input)
    def stage_1_do_execute(config: Config, stage_input: StageOneInput) -> StageOneOutput:
        result = execute_stage_1(stage_input)

        print(stage_1_summary(config, stage_input))

        return result


    if config.start_from <= STAGE_ONE:
        print("")
        print("[STAGE 1 | Submission Validation]")
        print("")

        stage_1_input = stage_1_collect_input(config)
        stage_1_do_execute(config, stage_1_input)

        state_manager.register_award_forms(stage_1_input.award_forms)

        print("")
        print("Saving cast votes to database...")
        print("")

        try:
            state_manager.save_cast_votes()
        except RuntimeError as err:
            print(f"Database insertion failed: {err}")
            print("Aborting...")
            exit(1)

        print("Save done ✔")


    # STAGE 2

    @retry(err_header="[Stage 2 | Input collection ERROR]")
    def stage_2_collect_input() -> StageTwoInput:
        return StageTwoInput(load_s2_tfa_from_db())


    @configless_stage(err_header="[Stage 2 | Execution ERROR]", data_collector=stage_2_collect_input)
    def stage_2_do_execute(stage_input: StageTwoInput) -> StageTwoOutput:
        result = execute_stage_2(stage_input)

        print(stage_2_summary(stage_input, result))

        return result


    if config.start_from <= STAGE_TWO:
        print("")
        print("[STAGE 2 | Ranking]")
        print("")

        stage_2_input = stage_2_collect_input()
        stage_2_result = stage_2_do_execute(stage_2_input)

        state_manager.register_stage_2_output(stage_2_result)

        print("")
        print("Saving nomination stats to database...")
        print("")

        try:
            state_manager.save_nomination_stats()
        except RuntimeError as err:
            print(f"Database insertion failed: {err}")
            print("Aborting...")
            exit(1)

        print("Save done ✔")


    # STAGE 3

    @retry(err_header="[Stage 3 | Input collection ERROR]")
    def stage_3_collect_input() -> StageThreeInput:
        return StageThreeInput(load_s3_tfa_from_db())


    @configless_stage(err_header="[Stage 3 | Execution ERROR]", data_collector=stage_3_collect_input)
    def stage_3_do_execute(stage_input: StageThreeInput) -> StageThreeOutput:
        result = execute_stage_3(stage_input)

        print(stage_3_summary(result))

        return result


    if config.start_from <= STAGE_THREE:
        print("")
        print("[STAGE 3 | Templates Pre-Generation Fulfillment]")
        print("")

        stage_3_input = stage_3_collect_input()
        stage_3_result = stage_3_do_execute(stage_3_input)

        state_manager.register_stage_3_output(stage_3_result)

        print("")
        print("Saving settings and templates to database...")
        print("")

        try:
            state_manager.save_settings_and_templates()
        except RuntimeError as err:
            print(f"Database insertion failed. Cause: {err}")
            print("Aborting...")
            exit(1)

        print("Save done ✔")


    # STAGE 4

    @retry_or_reconfig(err_header="[Stage 4 | Input collection ERROR]", config_loader=config_loader)
    def stage_4_collect_input(config: Config) -> StageFourInput:
        return StageFourInput(load_templates_from_db(generate_presentations=config.stitch_final_video))


    @stage(err_header="[Stage 4 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_4_collect_input)
    def stage_4_do_execute(config: Config, stage_input: StageFourInput) -> StageFourOutput:
        result = execute_stage_4(config, stage_input)

        print(stage_4_summary(config, stage_input, result))

        return result


    if config.start_from <= STAGE_FOUR:
        print("")
        print("[STAGE 4 | Templates Generation]")
        print("")

        stage_4_do_execute(config, stage_4_collect_input(config))


    # STAGE 5

    @retry(err_header="[Stage 5 | Input collection ERROR]")
    def stage_5_collect_input() -> StageFiveInput:
        return StageFiveInput(load_videoclips_from_db())


    @stage(err_header="[Stage 5 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_5_collect_input)
    def stage_5_do_execute(config: Config, stage_input: StageFiveInput) -> StageFiveOutput:
        videoclips = stage_input.videoclips

        result = execute_stage_5(config, stage_input)

        print(stage_5_summary(stage_input, result))

        return result


    if config.start_from <= STAGE_FIVE:
        print("")
        print("[STAGE 5 | Videoclips Acquisition]")
        print("")

        stage_5_do_execute(config, stage_5_collect_input())


    # STAGE 6

    @retry(err_header="[Stage 6 | Input collection ERROR]")
    def stage_6_collect_input() -> StageSixInput:
        return StageSixInput(nominations_video_options=load_video_options_from_db())


    @stage(err_header="[Stage 6 | Execution ERROR]",
           config_loader=config_loader,
           data_collector=stage_6_collect_input)
    def stage_6_do_execute(config: Config, stage_input: StageSixInput) -> StageSixOutput:
        result = execute_stage_6(config, stage_input)

        print(stage_6_summary(config, stage_input, result))

        if config.stitch_final_video:
            print(f"  Final video files: '{result.final_videos_files}'")

        return result


    if config.start_from <= STAGE_SIX:
        print("")
        print("[STAGE 6 | Video Generation]")
        print("")

        stage_6_do_execute(config, stage_6_collect_input())

    print("")
    print("Pipeline execution completed ✔")
    print("")
