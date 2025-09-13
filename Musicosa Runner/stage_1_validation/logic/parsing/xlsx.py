import os

from openpyxl.reader.excel import load_workbook

from common.types import StageException
from stage_1_validation.constants import XLSX_CONTESTANT_NAME_COORDS, XLSX_FORM_DATA_COORDS
from stage_1_validation.logic.parsing.utils import parse_score_str, parse_video_timestamp_str, parse_special_topic_str
from stage_1_validation.types import ContestantSubmissionEntry, ContestantSubmission


def parse_contestant_forms_xlsx_folder(forms_folder: str) -> list[ContestantSubmission]:
    submissions: list[ContestantSubmission] = []
    form_files = [file for file in os.listdir(forms_folder) if file.endswith('.xlsx')]

    for form_file in form_files:
        submissions.append(parse_contestant_form_xlsx(f"{forms_folder}/{form_file}"))

    return submissions


def parse_contestant_form_xlsx(form_file: str) -> ContestantSubmission:
    contestant_submission: ContestantSubmission
    submission_entries: list[ContestantSubmissionEntry] = []

    workbook = load_workbook(form_file, data_only=True, read_only=True)
    worksheet = workbook.active

    contestant_name = worksheet[XLSX_CONTESTANT_NAME_COORDS].value
    data_cells_matrix = worksheet[XLSX_FORM_DATA_COORDS]

    for data_cells_row in data_cells_matrix:
        raw_title = data_cells_row[0].value
        raw_score = data_cells_row[1].value
        raw_is_author = data_cells_row[2].value
        raw_video_url = data_cells_row[3].value
        raw_video_timestamp = data_cells_row[4].value
        raw_special_topic = data_cells_row[5].value

        title = raw_title.strip() if raw_title else raw_title

        try:
            score = parse_score_str(str(raw_score))
        except ValueError as err:
            raise StageException(f"[{contestant_name}] [{title}] Error parsing score value '{raw_score}'") from err

        is_author = raw_is_author.strip() != "" if raw_is_author else False

        if not is_author:
            submission_entries.append(
                ContestantSubmissionEntry(title=title, score=score, is_author=is_author, video_timestamp=None,
                                          video_url=None, special_topic=None))
            continue

        video_url = raw_video_url.strip() if raw_video_url else None

        if raw_video_timestamp and raw_video_timestamp.strip():
            try:
                video_timestamp = parse_video_timestamp_str(raw_video_timestamp)
            except ValueError as err:
                raise StageException(f"[{contestant_name}] [{title}] {err}") from err
        else:
            video_timestamp = None

        special_topic = parse_special_topic_str(raw_special_topic) if raw_special_topic else None

        submission_entries.append(
            ContestantSubmissionEntry(title=title, score=score, is_author=is_author, video_timestamp=video_timestamp,
                                      video_url=video_url, special_topic=special_topic))

    workbook.close()

    return ContestantSubmission(name=contestant_name, entries=submission_entries)
