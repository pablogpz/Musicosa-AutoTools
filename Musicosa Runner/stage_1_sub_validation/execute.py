from common.model.settings import is_setting_set
from common.type_definitions import StageException
from stage_1_sub_validation.logic.validation import validate_award_form_collection
from stage_1_sub_validation.type_definitions import StageOneOutput, AwardForm


def execute(award_forms: list[AwardForm],
            valid_award_slugs: list[str],
            awards_count: int,
            members_count: int) -> StageOneOutput:
    if not is_setting_set('validation.score_min_value'):
        raise StageException("Setting 'validation.score_min_value' not set")

    if not is_setting_set('validation.score_max_value'):
        raise StageException("Setting 'validation.score_max_value' not set")

    if len(valid_award_slugs) == 0:
        raise StageException('Valid award slugs not provided')

    validation_errors = validate_award_form_collection(award_forms, valid_award_slugs, awards_count, members_count)

    return StageOneOutput(validation_errors=validation_errors)
