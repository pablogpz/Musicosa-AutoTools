from common.custom_types import StageException
from common.model.models import SpecialEntryTopic
from stage_1_validation.custom_types import ContestantSubmission
from stage_1_validation.logic.parsing.xlsx import parse_contestant_forms_xlsx_folder


def get_submissions_from_forms_folder(forms_folder: str,
                                      contestant_name_coords: str,
                                      entries_data_coords: str) -> list[ContestantSubmission]:
    try:
        contestant_submissions = parse_contestant_forms_xlsx_folder(forms_folder,
                                                                    contestant_name_coords,
                                                                    entries_data_coords)
    except Exception as err:
        raise StageException(f"Error parsing submission forms: {err}") from err

    return contestant_submissions


def get_valid_titles(forms_folder: str, valid_titles_file: str) -> list[str]:
    try:
        with open(f"{forms_folder}/{valid_titles_file}", "r", encoding="UTF-8") as file:
            return [line.strip() for line in file.read().splitlines()]
    except IOError as err:
        raise StageException(f"Error loading valid entry titles file '{valid_titles_file}': {err}") from err


def get_special_topics_from_db() -> list[SpecialEntryTopic] | None:
    return [topic.to_domain() for topic in SpecialEntryTopic.ORM.select()] or None
