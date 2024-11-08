import os
from os.path import basename

from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.time_utils import validate_time_str, time_str_zfill
from common.type_definitions import StageException
from stage_1_sub_validation.constants import CSV_SEPARATOR, CSV_FIELDS_COUNT, ALLOWED_DECIMAL_SEPARATOR_CHARS, \
    NORMALIZED_DECIMAL_SEPARATOR_CHAR
from stage_1_sub_validation.type_definitions import ContestantSubmissionEntry, ContestantSubmission


def parse_contestant_form_entry_csv(entry_line: str) -> ContestantSubmissionEntry:
    line = entry_line.strip().split(CSV_SEPARATOR)

    if len(line) != CSV_FIELDS_COUNT:
        raise StageException(f"Fields count mismatch ({line})")

    title = line[0].strip()

    score_normalized = line[1].strip()
    for separator in ALLOWED_DECIMAL_SEPARATOR_CHARS:
        if separator in score_normalized:
            score_normalized = score_normalized.replace(separator, NORMALIZED_DECIMAL_SEPARATOR_CHAR)
    try:
        score = float(score_normalized)
    except ValueError as err:
        raise StageException(f"[{title}] Error parsing score value '{line[1]}'") from err

    is_author = line[2].strip() != ""

    if not is_author:
        return ContestantSubmissionEntry(title=title, score=score, is_author=is_author, video_timestamp=None,
                                         video_url=None, special_topic=None)

    video_url = line[3].strip() or None

    if raw_video_timestamp := line[4].strip():
        raw_video_timestamp = raw_video_timestamp.replace(" ", "").split(VIDEO_TIMESTAMP_SEPARATOR)

        if len(raw_video_timestamp) != 2:
            raise StageException(f"[{title}] Error parsing video timestamp '{line[4]}'")

        timestamp_start, timestamp_end = raw_video_timestamp

        if not validate_time_str(timestamp_start):
            raise StageException(f"[{title}] Error parsing video timestamp start '{timestamp_start}'")

        if not validate_time_str(timestamp_end):
            raise StageException(f"[{title}] Error parsing video timestamp end '{timestamp_end}'")

        video_timestamp = f"{time_str_zfill(timestamp_start)}{VIDEO_TIMESTAMP_SEPARATOR}{time_str_zfill(timestamp_end)}"
    else:
        video_timestamp = None

    if special_topic := line[5].strip():
        special_topic = special_topic.upper()
    else:
        special_topic = None

    return ContestantSubmissionEntry(title=title, score=score, is_author=is_author, video_timestamp=video_timestamp,
                                     video_url=video_url, special_topic=special_topic)


def parse_contestant_form_csv(form_file: str) -> ContestantSubmission:
    contestant_name = basename(form_file).rsplit('.', 1)[0]
    entries: list[ContestantSubmissionEntry] = []

    with open(form_file, "r") as file:
        for csv_line in file:
            try:
                entries.append(parse_contestant_form_entry_csv(csv_line))
            except StageException as err:
                raise StageException(f"[{contestant_name}] {err}") from err

    return ContestantSubmission(name=contestant_name, entries=entries)


def parse_contestant_forms_csv_folder(forms_folder: str) -> list[ContestantSubmission]:
    form_files = [file for file in os.listdir(forms_folder) if file.endswith('.csv')]
    submissions: list[ContestantSubmission] = []

    for form_file in form_files:
        submissions.append(parse_contestant_form_csv(f"{forms_folder}/{form_file}"))

    return submissions
