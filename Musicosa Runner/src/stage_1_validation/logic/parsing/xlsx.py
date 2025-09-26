import os

from openpyxl.reader.excel import load_workbook

from common.custom_types import StageException
from stage_1_validation.custom_types import ContestantSubmissionEntry, ContestantSubmission
from stage_1_validation.logic.parsing.utils import parse_score_str, parse_video_timestamp_str, parse_entry_topic_str


def parse_contestant_forms_xlsx_folder(forms_folder: str,
                                       contestant_name_coords: str,
                                       entries_data_coords: str) -> list[ContestantSubmission]:
    submissions: list[ContestantSubmission] = []
    form_files = [file for file in os.listdir(forms_folder) if file.endswith('.xlsx')]

    for form_file in form_files:
        submissions.append(parse_contestant_form_xlsx(f"{forms_folder}/{form_file}",
                                                      contestant_name_coords,
                                                      entries_data_coords))

    return submissions


def parse_contestant_form_xlsx(form_file: str,
                               contestant_name_coords: str,
                               entries_data_coords: str) -> ContestantSubmission:
    submission_entries: list[ContestantSubmissionEntry] = []

    workbook = load_workbook(form_file, data_only=True, read_only=True)
    worksheet = workbook.active

    if worksheet is None:
        raise StageException(f"Error loading worksheet from workbook (file '{form_file}')")

    contestant_name = worksheet[contestant_name_coords].value
    data_cells_matrix = worksheet[entries_data_coords]

    for data_cells_row in data_cells_matrix:
        raw_title = data_cells_row[0].value
        raw_score = data_cells_row[1].value
        raw_is_author = data_cells_row[2].value
        raw_video_url = data_cells_row[3].value
        raw_video_timestamp = data_cells_row[4].value
        raw_topic = data_cells_row[5].value

        title = raw_title.strip() if raw_title else raw_title

        try:
            score = parse_score_str(str(raw_score))
        except ValueError as err:
            raise StageException(
                f"[{contestant_name}][{title}] Error parsing score value '{raw_score}': {err}") from err

        is_author = raw_is_author.strip() != "" if raw_is_author else False

        if not is_author:
            submission_entries.append(
                ContestantSubmissionEntry(title, score, is_author, video_url=None, video_timestamp=None,
                                          topic=None))
            continue

        video_url = raw_video_url.strip() if raw_video_url else None

        if raw_video_timestamp and raw_video_timestamp.strip():
            try:
                video_timestamp = parse_video_timestamp_str(raw_video_timestamp)
            except ValueError as err:
                raise StageException(f"[{contestant_name}][{title}] {err}") from err
        else:
            video_timestamp = None

        topic = parse_entry_topic_str(raw_topic) if raw_topic else None

        submission_entries.append(
            ContestantSubmissionEntry(title, score, is_author, video_url, video_timestamp, topic))
    workbook.close()

    return ContestantSubmission(contestant_name, submission_entries)
