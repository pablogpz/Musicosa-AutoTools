from common.model.models import SpecialEntryTopic
from common.types import StageException
from stage_1_validation.logic.parsing.xlsx import parse_contestant_forms_xlsx_folder
from stage_1_validation.types import ContestantSubmission


def get_submissions_from_forms_folder(forms_folder: str) -> list[ContestantSubmission]:
    try:
        contestant_submissions = parse_contestant_forms_xlsx_folder(forms_folder)
    except Exception as err:
        raise StageException(f"[Submission forms parsing error] {err}") from err

    return contestant_submissions


def get_submission_entry_valid_titles(forms_folder: str, valid_titles_file: str) -> list[str]:
    try:
        valid_titles = load_valid_titles_from_file(f"{forms_folder}/{valid_titles_file}")
    except IOError as err:
        raise StageException(
            f"[Config parsing error] Error loading valid submission entry titles file '{valid_titles_file}': {err}"
        ) from err

    return valid_titles


def load_valid_titles_from_file(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="UTF-8") as file:
        try:
            return [line.strip() for line in file.read().splitlines()]
        except IOError:
            raise


def get_special_entry_topics_from_db() -> list[SpecialEntryTopic] | None:
    return [topic.to_domain() for topic in SpecialEntryTopic.ORM.select()] or None
