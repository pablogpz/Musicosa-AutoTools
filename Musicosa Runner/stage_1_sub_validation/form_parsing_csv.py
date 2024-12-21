import os
from os.path import basename

from common.type_definitions import StageException
from form_parsing_utils import parse_special_topic_str
from stage_1_sub_validation.constants import CSV_SEPARATOR, CSV_FIELDS_COUNT
from stage_1_sub_validation.form_parsing_utils import parse_score_str, parse_video_timestamp_str
from stage_1_sub_validation.type_definitions import ContestantSubmissionEntry, ContestantSubmission


def parse_contestant_form_entry_csv(entry_line: str) -> ContestantSubmissionEntry:
    line = entry_line.strip().split(CSV_SEPARATOR)

    if len(line) != CSV_FIELDS_COUNT:
        raise StageException(f"Fields count mismatch ({line})")

    title = line[0].strip()

    try:
        score = parse_score_str(line[1])
    except ValueError as err:
        raise StageException(f"[{title}] Error parsing score value '{line[1]}'") from err

    is_author = line[2].strip() != ""

    if not is_author:
        return ContestantSubmissionEntry(title=title, score=score, is_author=is_author, video_timestamp=None,
                                         video_url=None, special_topic=None)

    video_url = line[3].strip() or None

    if raw_video_timestamp := line[4].strip():
        try:
            video_timestamp = parse_video_timestamp_str(raw_video_timestamp)
        except ValueError as err:
            raise StageException(f"[{title}] {err}") from err
    else:
        video_timestamp = None

    if raw_special_topic := line[5].strip():
        special_topic = parse_special_topic_str(raw_special_topic)
    else:
        special_topic = None

    return ContestantSubmissionEntry(title=title, score=score, is_author=is_author, video_timestamp=video_timestamp,
                                     video_url=video_url, special_topic=special_topic)


def parse_contestant_form_csv(form_file: str) -> ContestantSubmission:
    entries: list[ContestantSubmissionEntry] = []
    contestant_name = basename(form_file).rsplit('.', 1)[0]

    with open(form_file, "r", encoding="UTF-8") as file:
        for csv_line in file:
            try:
                entries.append(parse_contestant_form_entry_csv(csv_line))
            except StageException as err:
                raise StageException(f"[{contestant_name}] {err}") from err

    return ContestantSubmission(name=contestant_name, entries=entries)


def parse_contestant_forms_csv_folder(forms_folder: str) -> list[ContestantSubmission]:
    submissions: list[ContestantSubmission] = []
    form_files = [file for file in os.listdir(forms_folder) if file.endswith('.csv')]

    for form_file in form_files:
        submissions.append(parse_contestant_form_csv(f"{forms_folder}/{form_file}"))

    return submissions
