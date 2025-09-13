from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from common.types import StageException
from stage_1_validation.logic.validation import validate_award_form_collection
from stage_1_validation.types import StageOneOutput, AwardForm


def execute(award_forms: list[AwardForm],
            valid_award_slugs: list[str],
            awards_count: int,
            members_count: int) -> StageOneOutput:
    if not is_setting_set(SettingKeys.VALIDATION_SCORE_MIN_VALUE):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_SCORE_MIN_VALUE}' not set")

    if not is_setting_set(SettingKeys.VALIDATION_SCORE_MAX_VALUE):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_SCORE_MAX_VALUE}' not set")

    if len(valid_award_slugs) == 0:
        raise StageException('Valid award slugs not provided')

    validation_errors = validate_award_form_collection(award_forms, valid_award_slugs, awards_count, members_count)

    return StageOneOutput(validation_errors=validation_errors)
