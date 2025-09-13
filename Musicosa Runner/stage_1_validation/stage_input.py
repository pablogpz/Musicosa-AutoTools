from common.model.models import Award, Member
from common.types import StageException
from stage_1_validation.logic.parsing.csv import parse_award_forms_csv_folder
from stage_1_validation.types import AwardForm


def parse_award_forms_folder(forms_folder: str) -> list[AwardForm]:
    try:
        award_forms = parse_award_forms_csv_folder(forms_folder)
    except Exception as err:
        raise StageException(f"[Award forms parsing error] {err}") from err

    return award_forms


def get_valid_award_slugs() -> list[str]:
    return [award.to_domain().slug for award in Award.ORM.select()]


def get_award_count() -> int:
    return len([r for r in Award.ORM.select()])


def get_member_count() -> int:
    return len([r for r in Member.ORM.select()])
