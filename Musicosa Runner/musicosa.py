import argparse
import inspect
import tomllib
from collections.abc import Callable
from dataclasses import dataclass, field
from logging import error
from os import path
from typing import Literal, Never, Protocol, Any, cast

from peewee import PeeweeException

from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.input.better_input import better_input
from common.model.metadata import get_metadata_by_field
from common.model.models import Template, Setting, NominationStats, \
    CastVote, MetadataFields
from common.naming.identifiers import generate_member_uuid5, generate_nomination_uuid5_from_nomination_str
from stage_1_validation.custom_types import StageOneOutput, StageOneInput
from stage_1_validation.execute import execute as execute_stage_1
from stage_1_validation.stage_input import parse_award_forms_folder, get_award_count, get_member_count, \
    get_valid_award_slugs
from stage_2_ranking.custom_types import StageTwoOutput, StageTwoInput
from stage_2_ranking.execute import execute as execute_stage_2
from stage_2_ranking.stage_input import load_tfa_from_db as load_s2_tfa_from_db
from stage_3_templates_pre_gen.custom_types import StageThreeOutput, StageThreeInput
from stage_3_templates_pre_gen.execute import execute as execute_stage_3
from stage_3_templates_pre_gen.stage_input import load_tfa_from_db as load_s3_tfa_from_db
from stage_4_templates_gen.custom_types import StageFourOutput, StageFourInput
from stage_4_templates_gen.execute import execute as execute_stage_4
from stage_4_templates_gen.stage_input import load_templates_from_db
from stage_5_videoclips_acquisition.custom_types import StageFiveOutput, StageFiveInput
from stage_5_videoclips_acquisition.execute import execute as execute_stage_5
from stage_5_videoclips_acquisition.stage_input import load_videoclips_from_db
from stage_6_video_gen.custom_types import StageSixOutput, \
    StageSixInput, TransitionOptions, TransitionType
from stage_6_video_gen.execute import execute as execute_stage_6
from stage_6_video_gen.stage_input import load_video_options_from_db

# STAGE IDs

STAGE_ONE: Literal[1] = 1
STAGE_TWO: Literal[2] = 2
STAGE_THREE: Literal[3] = 3
STAGE_FOUR: Literal[4] = 4
STAGE_FIVE: Literal[5] = 5
STAGE_SIX: Literal[6] = 6

type Stage = Literal[1, 2, 3, 4, 5, 6]

# MUSICOSA CONFIG DEFAULTS

DEFAULT_CONFIG_FILE = "musicosa.config.toml"

# Global defaults
DEFAULT_ARTIFACTS_FOLDER = "artifacts"
DEFAULT_START_FROM_STAGE: Stage = STAGE_ONE
DEFAULT_STITCH_FINAL_VIDEO_FLAG = False
# Stage 1 defaults
DEFAULT_AWARD_FORMS_FOLDER = "award_forms"
# Stage 4 defaults
DEFAULT_TEMPLATES_API_URL = "http://localhost:3000/templates"
DEFAULT_PRESENTATIONS_API_URL = "http://localhost:3000/presentations"
DEFAULT_GENERATION_RETRY_ATTEMPTS = 3
DEFAULT_OVERWRITE_TEMPLATES = True
DEFAULT_OVERWRITE_PRESENTATIONS = True
# Stage 5 defaults
DEFAULT_STAGE_5_QUIET_FFMPEG = True
# Stage 6 defaults
DEFAULT_VIDEO_BITS_FOLDER = f"{DEFAULT_ARTIFACTS_FOLDER}/video_bits"
DEFAULT_OVERWRITE_VIDEO_BITS = True
DEFAULT_PRESENTATION_DURATION = 5
DEFAULT_TRANSITION_DURATION = 3
DEFAULT_TRANSITION_TYPE = "fade"
DEFAULT_STAGE_6_QUIET_FFMPEG = True
DEFAULT_QUIET_FFMPEG_FINAL_VIDEO = True


# Config dataclasses
#     Note: Keep in sync with TOML keys

@dataclass
class StageOneConfig:
    award_forms_folder: str = DEFAULT_AWARD_FORMS_FOLDER

    def __init__(self, award_forms_folder: str = DEFAULT_AWARD_FORMS_FOLDER):
        award_forms_folder = award_forms_folder.strip()

        self.award_forms_folder = award_forms_folder.removesuffix("/") if award_forms_folder.endswith("/") \
            else award_forms_folder


@dataclass
class StageFourConfig:
    templates_api_url: str = DEFAULT_TEMPLATES_API_URL
    presentations_api_url: str = DEFAULT_PRESENTATIONS_API_URL
    gen_retry_attempts: int = DEFAULT_GENERATION_RETRY_ATTEMPTS
    overwrite_templates: bool = DEFAULT_OVERWRITE_TEMPLATES
    overwrite_presentations: bool = DEFAULT_OVERWRITE_PRESENTATIONS

    def __init__(self, templates_api_url: str = DEFAULT_TEMPLATES_API_URL,
                 presentations_api_url: str = DEFAULT_PRESENTATIONS_API_URL,
                 gen_retry_attempts: int = DEFAULT_GENERATION_RETRY_ATTEMPTS,
                 overwrite_templates: bool = DEFAULT_OVERWRITE_TEMPLATES,
                 overwrite_presentations: bool = DEFAULT_OVERWRITE_PRESENTATIONS):
        templates_api_url = templates_api_url.strip()

        self.templates_api_url = templates_api_url.removesuffix("/") if templates_api_url.endswith("/") \
            else templates_api_url

        presentations_api_url = presentations_api_url.strip()

        self.presentations_api_url = presentations_api_url.removesuffix("/") if presentations_api_url.endswith("/") \
            else presentations_api_url

        self.gen_retry_attempts = gen_retry_attempts
        self.overwrite_templates = overwrite_templates
        self.overwrite_presentations = overwrite_presentations


@dataclass
class StageFiveConfig:
    quiet_ffmpeg: bool = DEFAULT_STAGE_5_QUIET_FFMPEG

    def __init__(self, quiet_ffmpeg: bool = DEFAULT_STAGE_5_QUIET_FFMPEG):
        self.quiet_ffmpeg = quiet_ffmpeg


@dataclass
class StageSixConfig:
    video_bits_folder: str = DEFAULT_VIDEO_BITS_FOLDER
    overwrite_video_bits: bool = DEFAULT_OVERWRITE_VIDEO_BITS
    presentation_duration: int = DEFAULT_PRESENTATION_DURATION
    transition_duration: int = DEFAULT_TRANSITION_DURATION
    transition_type: str = DEFAULT_TRANSITION_TYPE
    quiet_ffmpeg: bool = DEFAULT_STAGE_6_QUIET_FFMPEG
    quiet_ffmpeg_final_video: bool = DEFAULT_QUIET_FFMPEG_FINAL_VIDEO

    def __init__(self, video_bits_folder: str = DEFAULT_VIDEO_BITS_FOLDER,
                 overwrite_video_bits: bool = DEFAULT_OVERWRITE_VIDEO_BITS,
                 presentation_duration: int = DEFAULT_PRESENTATION_DURATION,
                 transition_duration: int = DEFAULT_TRANSITION_DURATION,
                 transition_type: str = DEFAULT_TRANSITION_TYPE,
                 quiet_ffmpeg: bool = DEFAULT_STAGE_6_QUIET_FFMPEG,
                 quiet_ffmpeg_final_video: bool = DEFAULT_QUIET_FFMPEG_FINAL_VIDEO):
        video_bits_folder = video_bits_folder.strip()

        self.video_bits_folder = video_bits_folder.removesuffix("/") if video_bits_folder.endswith("/") \
            else video_bits_folder
        self.overwrite_video_bits = overwrite_video_bits
        self.presentation_duration = presentation_duration
        self.transition_duration = transition_duration
        self.transition_type = transition_type.strip()
        self.quiet_ffmpeg = quiet_ffmpeg
        self.quiet_ffmpeg_final_video = quiet_ffmpeg_final_video


@dataclass
class Config:
    start_from: Stage = DEFAULT_START_FROM_STAGE
    artifacts_folder: str = DEFAULT_ARTIFACTS_FOLDER
    stitch_final_video: bool = DEFAULT_STITCH_FINAL_VIDEO_FLAG
    stage_1: StageOneConfig = field(default_factory=StageOneConfig)
    stage_4: StageFourConfig = field(default_factory=StageFourConfig)
    stage_5: StageFiveConfig = field(default_factory=StageFiveConfig)
    stage_6: StageSixConfig = field(default_factory=StageSixConfig)

    def __init__(self, start_from: Stage = DEFAULT_START_FROM_STAGE,
                 artifacts_folder: str = DEFAULT_ARTIFACTS_FOLDER,
                 stitch_final_video: bool = DEFAULT_STITCH_FINAL_VIDEO_FLAG,
                 stage_1: StageOneConfig = StageOneConfig(),
                 stage_4: StageFourConfig = StageFourConfig(),
                 stage_5: StageFiveConfig = StageFiveConfig(),
                 stage_6: StageSixConfig = StageSixConfig()):
        self.start_from = start_from
        self.artifacts_folder = artifacts_folder.strip()
        self.stitch_final_video = stitch_final_video
        self.stage_1 = stage_1
        self.stage_4 = stage_4
        self.stage_5 = stage_5
        self.stage_6 = stage_6


def load_config(toml_config_file: str = DEFAULT_CONFIG_FILE) -> Config:
    if not path.isfile(toml_config_file):
        raise FileNotFoundError(f"Config file '{toml_config_file}' not found")

    with open(toml_config_file, "r") as config:
        try:
            config_str_contents = config.read()
        except IOError as err:
            raise IOError(f"Couldn't read config file contents: {err}") from err

    config_dict = tomllib.loads(config_str_contents, parse_float=float)

    try:
        return Config(start_from=config_dict["start_from"],
                      artifacts_folder=config_dict["artifacts_folder"],
                      stitch_final_video=config_dict["stitch_final_video"],
                      stage_1=StageOneConfig(**config_dict["stage_1"]),
                      stage_4=StageFourConfig(**config_dict["stage_4"]),
                      stage_5=StageFiveConfig(**config_dict["stage_5"]),
                      stage_6=StageSixConfig(**config_dict["stage_6"]))
    except TypeError as err:
        raise TypeError(f"Couldn't parse config file: {err}") from err


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
        config_file: str = DEFAULT_CONFIG_FILE,
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
        config_file: str = DEFAULT_CONFIG_FILE,
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
        config_file: str = DEFAULT_CONFIG_FILE
) -> Callable[[ControlGateSurrogate[SI, SO]], ControlGateSurrogate[SI, SO]]:
    return custom_gate(controls={RETRY, RELOAD_CONFIG, ABORT}, err_header=err_header, config_file=config_file)


def stage_gate[SI, SO](
        err_header: str,
        reload_input: StageInputCollector[SI],
        config_file: str = DEFAULT_CONFIG_FILE
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

    # MUSICOSA CONFIG

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", default=DEFAULT_CONFIG_FILE)
    args = parser.parse_args()

    config_file = args.config_file.strip()

    try:
        config = load_config(config_file)
    except FileNotFoundError | IOError | TypeError as err:
        error(f"Config loading error: {err}")
        exit(1)

    # MUSICOSA PIPELINE

    # Pipeline State

    raw_cast_vote_models: list[CastVote.ORM] = []
    raw_nomination_stats_models: list[NominationStats.ORM] = []
    template_models: list[Template] = []
    setting_models: list[Setting] = []

    # Pipeline Execution

    musicosa_edition = get_metadata_by_field(MetadataFields.EDITION).value

    print(f"[TFA {musicosa_edition}º EDITION]")
    print(f"  Edition: {musicosa_edition}")


    # STAGE 1

    @retry_or_reconfig(err_header="[Stage 1 | Input collection ERROR]", config_file=config_file)
    def stage_1_collect_input(*, config: Config) -> StageOneInput:
        award_forms = parse_award_forms_folder(config.stage_1.award_forms_folder)
        valid_award_slugs = get_valid_award_slugs()
        awards_count = get_award_count()
        members_count = get_member_count()

        return StageOneInput(award_forms=award_forms, valid_award_slugs=valid_award_slugs, award_count=awards_count,
                             member_count=members_count)


    @stage_gate(err_header="[Stage 1 | Execution ERROR]",
                config_file=config_file,
                reload_input=stage_1_collect_input)
    def stage_1_do_execute(*, config: Config, stage_input: StageOneInput) -> StageOneOutput:
        award_forms, valid_award_slugs, awards_count, members_count = (stage_input.award_forms,
                                                                       stage_input.valid_award_slugs,
                                                                       stage_input.award_count,
                                                                       stage_input.member_count)

        result = execute_stage_1(award_forms=award_forms, valid_award_slugs=valid_award_slugs,
                                 award_count=awards_count, member_count=members_count)

        print("")
        print("[STAGE 1 SUMMARY | Submissions Validation]")
        print(f"  Award forms folder: '{config.stage_1.award_forms_folder}'")
        print(f"  Valid award slugs: {valid_award_slugs}")
        print(f"  Awards count: {awards_count}")
        print(f"  Members count: {members_count}")
        print("")
        print(f"  # Award forms loaded: {len(award_forms)}")

        print("Validation errors:")
        if result.validation_errors:
            for validation_error in result.validation_errors:
                print(f"  {validation_error}")
        else:
            print("  All submissions are valid ✔")
        print("")

        return result


    if config.start_from <= STAGE_ONE:
        stage_1_input: StageOneInput = stage_1_collect_input(config=config)
        stage_1_result: StageOneOutput = stage_1_do_execute(config=config, stage_input=stage_1_input)

        # Update pipeline state

        for award in stage_1_input.award_forms:
            for submission in award.submissions:
                for cast_vote in submission.cast_votes:
                    raw_cast_vote_models.append(
                        CastVote.ORM(member=generate_member_uuid5(submission.name).hex,
                                     nomination=generate_nomination_uuid5_from_nomination_str(cast_vote.nomination,
                                                                                              award.award_slug).hex,
                                     score=cast_vote.score))

        print("")
        print("Checkpointing Musicosa model to database...")

        try:
            with db.atomic():
                if raw_cast_vote_models:
                    CastVote.ORM.replace_many([vote.__data__ for vote in raw_cast_vote_models]).execute()  # CAREFUL!
        except PeeweeException as err:
            print(f"Database checkpoint failed: {err}")
            print("Aborting...")
            exit(1)

        print("Checkpointing done ✔")
        print("")


    # STAGE 2

    @retry(err_header="[Stage 2 | Input collection ERROR]")
    def stage_2_collect_input(*, config: Config) -> StageTwoInput:
        return StageTwoInput(tfa=load_s2_tfa_from_db())


    @noconf_stage_gate(err_header="[Stage 2 | Execution ERROR]",
                       reload_input_with_oob_config=lambda: stage_2_collect_input(config=config))
    def stage_2_do_execute(*, stage_input: StageTwoInput) -> StageTwoOutput:
        tfa = stage_input.tfa

        result = execute_stage_2(tfa=tfa)

        print("")
        print("[STAGE 2 SUMMARY | TFA Ranking]")
        print(f"  # Awards loaded: {len(tfa.awards)}")
        print("")
        print(f"  # Ranked nominations: {len(result.nomination_stats)}")
        print("")

        return result


    if config.start_from <= STAGE_TWO:
        stage_2_input: StageTwoInput = stage_2_collect_input(config=config)
        stage_2_result: StageTwoOutput = stage_2_do_execute(stage_input=stage_2_input)

        # Update pipeline state

        for stat in stage_2_result.nomination_stats:
            raw_nomination_stats_models.append(
                NominationStats.ORM(nomination=stat.nomination_id,
                                    avg_score=stat.avg_score,
                                    ranking_place=stat.ranking_place,
                                    ranking_sequence=stat.ranking_sequence))

        print("")
        print("Checkpointing Musicosa model to database...")

        try:
            with db.atomic():
                if raw_nomination_stats_models:
                    NominationStats.ORM.replace_many(
                        [nomination.__data__ for nomination in raw_nomination_stats_models]).execute()  # CAREFUL!
        except PeeweeException as err:
            print(f"Database checkpoint failed: {err}")
            print("Aborting...")
            exit(1)

        print("Checkpointing done ✔")
        print("")


    # STAGE 3

    @retry(err_header="[Stage 3 | Input collection ERROR]")
    def stage_3_collect_input(*, config: Config) -> StageThreeInput:
        return StageThreeInput(tfa=load_s3_tfa_from_db())


    @noconf_stage_gate(err_header="[Stage 3 | Execution ERROR]",
                       reload_input_with_oob_config=lambda: stage_3_collect_input(config=config))
    def stage_3_do_execute(*, stage_input: StageThreeInput) -> StageThreeOutput:
        result = execute_stage_3(tfa=stage_input.tfa)

        print("")
        print("[STAGE 3 SUMMARY | Templates Pre-Generation]")
        print("")
        print(f"  # Frame settings set: {len(result.frame_settings) if result.frame_settings else 0}")
        print(f"  # Entry templates fulfilled: {len(result.templates) if result.templates else 0}")

        print("")
        print(" [!] Database checkpoint ahead")
        print("")

        return result


    if config.start_from <= STAGE_THREE:
        stage_3_input: StageThreeInput = stage_3_collect_input(config=config)
        stage_3_result: StageThreeOutput = stage_3_do_execute(stage_input=stage_3_input)

        # Update pipeline state

        if stage_3_result.frame_settings:
            setting_models.extend(stage_3_result.frame_settings)

        if stage_3_result.templates:
            template_models.extend(stage_3_result.templates)

    # DATA PERSISTENCE CHECKPOINT

    if config.start_from <= STAGE_THREE:

        print("")
        print("Checkpointing Musicosa model to database...")

        try:
            with db.atomic():
                if setting_models:
                    Setting.ORM.replace_many(bulk_pack(setting_models)).execute()

                if template_models:
                    Template.ORM.replace_many(bulk_pack(template_models)).execute()
        except PeeweeException as err:
            print(f"Database checkpoint failed: {err}")
            print("Aborting...")
            exit(1)

        print("Checkpointing done ✔")
        print("")


    # STAGE 4

    @retry_or_reconfig(err_header="[Stage 4 | Input collection ERROR]", config_file=config_file)
    def stage_4_collect_input(*, config: Config) -> StageFourInput:
        return StageFourInput(templates_api_url=config.stage_4.templates_api_url,
                              presentations_api_url=config.stage_4.presentations_api_url,
                              artifacts_folder=config.artifacts_folder,
                              templates=load_templates_from_db(config.stitch_final_video),
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
              f"{len(result.generated_templates_slugs) if result.generated_templates_slugs else 0}")

        if result.failed_templates_uuids:
            print(f"  Failed to generate templates ['{"', '".join(result.failed_templates_uuids)}']")
        print("")

        return result


    if config.start_from <= STAGE_FOUR:
        stage_4_input: StageFourInput = stage_4_collect_input(config=config)
        stage_4_result: StageFourOutput = stage_4_do_execute(config=config, stage_input=stage_4_input)


    # STAGE 5

    @retry_or_reconfig(err_header="[Stage 5 | Input collection ERROR]", config_file=config_file)
    def stage_5_collect_input(*, config: Config) -> StageFiveInput:
        return StageFiveInput(artifacts_folder=config.artifacts_folder, quiet_ffmpeg=config.stage_5.quiet_ffmpeg,
                              videoclips=load_videoclips_from_db())


    @stage_gate(err_header="[Stage 5 | Execution ERROR]", config_file=config_file, reload_input=stage_5_collect_input)
    def stage_5_do_execute(*, config: Config, stage_input: StageFiveInput) -> StageFiveOutput:
        result = execute_stage_5(artifacts_folder=config.artifacts_folder, quiet_ffmpeg=config.stage_5.quiet_ffmpeg,
                                 videoclips=stage_input.videoclips)

        print("")
        print("[STAGE 5 SUMMARY | Videoclips Acquisition]")
        print(f"  # Videoclips: {len(stage_input.videoclips)}")
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
        return StageSixInput(artifacts_folder=config.artifacts_folder,
                             video_bits_folder=config.stage_6.video_bits_folder,
                             nominations_video_options=load_video_options_from_db(),
                             overwrite=config.stage_6.overwrite_video_bits,
                             stitch_final_video=config.stitch_final_video,
                             transition_options=TransitionOptions(config.stage_6.presentation_duration,
                                                                  config.stage_6.transition_duration,
                                                                  cast(TransitionType,
                                                                       config.stage_6.transition_type)),
                             quiet_ffmpeg=config.stage_6.quiet_ffmpeg,
                             quiet_ffmpeg_final_video=config.stage_6.quiet_ffmpeg_final_video)


    @stage_gate(err_header="[Stage 6 | Execution ERROR]", config_file=config_file, reload_input=stage_6_collect_input)
    def stage_6_do_execute(*, config: Config, stage_input: StageSixInput) -> StageSixOutput:
        result = execute_stage_6(artifacts_folder=config.artifacts_folder,
                                 video_bits_folder=config.stage_6.video_bits_folder,
                                 nominations_video_options=stage_input.nominations_video_options,
                                 overwrite=config.stage_6.overwrite_video_bits,
                                 stitch_final_video=config.stitch_final_video,
                                 transition_options=TransitionOptions(config.stage_6.presentation_duration,
                                                                      config.stage_6.transition_duration,
                                                                      cast(TransitionType,
                                                                           config.stage_6.transition_type)),
                                 quiet_ffmpeg=config.stage_6.quiet_ffmpeg,
                                 quiet_ffmpeg_final_video=config.stage_6.quiet_ffmpeg_final_video)

        print("")
        print("[STAGE 6 SUMMARY | Video Generation]")
        print(f"  # Loaded nominations: {len(stage_input.nominations_video_options)}")
        print("")

        if result.nominations_missing_sources:
            print(f"  Nominations missing source files: ['{"', '".join(result.nominations_missing_sources)}']")
        print(f"  # Generated video bits: "
              f"{len(result.generated_video_bit_files) if result.generated_video_bit_files else 0}")
        if result.failed_video_bits:
            print(f"  Failed video bits: ['{"', '".join(result.failed_video_bits)}']")
        print("")

        if config.stitch_final_video:
            print(f"  Final video files: '{result.final_videos_files}'")

        return result


    if config.start_from <= STAGE_SIX:
        stage_6_input: StageSixInput = stage_6_collect_input(config=config)
        stage_6_result: StageSixOutput = stage_6_do_execute(config=config, stage_input=stage_6_input)

    # END OF MUSICOSA PIPELINE

    print("")
    print("Pipeline execution completed ✔")
