from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_1_validation.custom_types import StageOneInput, StageOneOutput
from stage_1_validation.logic.validation import validate_award_form_collection


def execute(stage_input: StageOneInput) -> StageOneOutput:
    award_forms, valid_award_slugs, award_count, member_count = (
        stage_input.award_forms,
        stage_input.valid_award_slugs,
        stage_input.award_count,
        stage_input.member_count,
    )

    if not is_setting_set(SettingKeys.VALIDATION_SCORE_MIN_VALUE):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_SCORE_MIN_VALUE}' not set")

    if not is_setting_set(SettingKeys.VALIDATION_SCORE_MAX_VALUE):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_SCORE_MAX_VALUE}' not set")

    if len(valid_award_slugs) == 0:
        raise StageException("Valid award slugs not provided")

    validation_errors = validate_award_form_collection(award_forms, valid_award_slugs, award_count, member_count)

    return StageOneOutput(validation_errors)
