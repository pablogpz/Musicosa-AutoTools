from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_1_validation.custom_types import StageOneInput, StageOneOutput
from stage_1_validation.logic.validation import validate_contestant_submission_collection


def execute(stage_input: StageOneInput) -> StageOneOutput:
    submissions, valid_titles, entry_topics = (
        stage_input.submissions,
        stage_input.valid_titles,
        stage_input.entry_topics,
    )

    if not is_setting_set(SettingKeys.GLOBAL_ROUND_COUNT):
        raise StageException(f"Setting '{SettingKeys.GLOBAL_ROUND_COUNT}' not set")

    if not is_setting_set(SettingKeys.VALIDATION_SCORE_MIN_VALUE):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_SCORE_MIN_VALUE}' not set")

    if not is_setting_set(SettingKeys.VALIDATION_SCORE_MAX_VALUE):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_SCORE_MAX_VALUE}' not set")

    if not is_setting_set(SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS}' not set")

    if not valid_titles:
        raise StageException("Valid entry titles list is empty")

    validation_errors = validate_contestant_submission_collection(submissions, valid_titles, entry_topics)

    return StageOneOutput(validation_errors)
