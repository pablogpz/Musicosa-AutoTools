from common.model.models import SpecialEntryTopic, SettingKeys
from common.model.settings import is_setting_set
from common.types import StageException
from stage_1_validation.logic.validation import validate_contestant_submission_collection
from stage_1_validation.types import StageOneOutput, ContestantSubmission


def execute(submissions: list[ContestantSubmission], valid_titles: list[str],
            special_entry_topics: list[SpecialEntryTopic] | None) -> StageOneOutput:
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

    validation_errors = validate_contestant_submission_collection(submissions=submissions,
                                                                  valid_titles=valid_titles,
                                                                  special_entry_topics=special_entry_topics)

    return StageOneOutput(validation_errors=validation_errors)
