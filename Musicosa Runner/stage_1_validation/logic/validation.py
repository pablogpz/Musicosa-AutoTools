from validators import url as validate_url, ValidationError

from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.model.models import SpecialEntryTopic, SettingKeys
from common.model.settings import get_setting_by_key
from common.time.utils import validate_time_str, parse_time, seconds_between
from stage_1_validation.custom_types import ContestantSubmissionEntry, ContestantSubmission
from stage_1_validation.logic.helpers import find_duplicates


def validate_contestant_submission_collection(submissions: list[ContestantSubmission],
                                              valid_titles: list[str],
                                              special_entry_topics: list[SpecialEntryTopic] | None) -> list[str] | None:
    contestant_count = len(submissions)
    round_count = get_setting_by_key(SettingKeys.GLOBAL_ROUND_COUNT).value
    validation_errors: list[str] = []

    if len(submissions) != contestant_count:
        validation_errors.append(
            f"Submission forms count mismatch ({len(submissions)}) (Should be {contestant_count})")

    # Validate that each entry has exactly one author across all submissions

    author_registry: dict[str, set[str]] = {}

    for sub in submissions:
        contestant_name, entries = sub.name, sub.entries
        for entry in entries:
            title, is_author = entry.title, entry.is_author
            if is_author and title in author_registry:
                author_registry[title].add(contestant_name)
            elif is_author:
                author_registry[title] = {contestant_name}  # Careful: Using 'set()' here would make a set of chars
            elif title not in author_registry:
                author_registry[title] = set()

    if entries_no_author := [item[0] for item in author_registry.items() if len(item[1]) == 0]:
        validation_errors.append(f"Entries with no authors ({len(entries_no_author)}): "
                                 f"{', '.join([f"'{title}'" for title in entries_no_author])}")

    if entries_multiple_authors := [item for item in author_registry.items() if len(item[1]) > 1]:
        for title, authors in entries_multiple_authors:
            validation_errors.append(f"Entry '{title}' has multiple authors ({len(authors)}):"
                                     f" {', '.join([f"'{author}'" for author in authors])}")

    # Validate each contestant submission

    for sub in submissions:
        if submission_errors := validate_contestant_submission(sub, contestant_count, round_count, valid_titles,
                                                               special_entry_topics):
            validation_errors.extend(submission_errors)

    return [err_msg for err_msg in validation_errors] or None


def validate_contestant_submission(submission: ContestantSubmission,
                                   contestants_count: int,
                                   rounds_count: int,
                                   valid_titles: list[str],
                                   special_entry_topics: list[SpecialEntryTopic] | None) -> list[str] | None:
    entries = submission.entries
    entry_count = contestants_count * rounds_count
    validation_errors: list[str] = []

    if len(entries) != entry_count:
        validation_errors.append(f"Submission entries count mismatch ({len(entries)}) (Should be {entry_count})")

    if (authored_entries_count := len([entry for entry in entries if entry.is_author])) != rounds_count:
        validation_errors.append(f"Author claims count mismatch ({authored_entries_count}) (Should be {rounds_count})")

    if duplicates := find_duplicates([entry.title for entry in entries]):
        for title, count in duplicates:
            validation_errors.append(f"Entry '{title}' is duplicated {count} time{"s" if count > 1 else ""}")

    titles = set([entry.title for entry in entries])
    valid_titles = set(valid_titles)

    if invalid_titles := titles - valid_titles:
        validation_errors.append(
            f"Invalid entries ({len(invalid_titles)}): ['{', '.join([f"'{title}'" for title in invalid_titles])}']")
    if missing_titles := valid_titles - titles:
        validation_errors.append(
            f"Missing entries ({len(missing_titles)}): ['{', '.join([f"'{title}'" for title in missing_titles])}']")

    for entry in entries:
        if entry_errors := validate_entry(entry, special_entry_topics):
            validation_errors.extend(entry_errors)

    if special_entry_topics:
        for topic in special_entry_topics:
            entries_with_topics = [entry for entry in entries if entry.special_topic is not None]
            occurrences = len([e for e in entries_with_topics if e.special_topic.lower() == topic.designation.lower()])

            if occurrences == 0:
                validation_errors.append(f"There are no entries designated as '{topic.designation.upper()}'")

            if occurrences > 1:
                validation_errors.append(
                    f"There are multiple ({occurrences}) entries of special topic '{topic.designation.upper()}'")

    return [f"[{submission.name}] {err_msg}" for err_msg in validation_errors] or None


def validate_entry(entry: ContestantSubmissionEntry, special_entry_topics: list[SpecialEntryTopic] | None) \
        -> list[str] | None:
    title, score, is_author, video_url, video_timestamp, special_topic = (
        entry.title, entry.score, entry.is_author, entry.video_url, entry.video_timestamp, entry.special_topic)
    validation_errors: list[str] = []

    if not is_author and video_timestamp:
        validation_errors.append("Video timestamp is only allowed for authors")

    if not is_author and video_url:
        validation_errors.append("Video URL is only allowed for authors")

    min_score = get_setting_by_key(SettingKeys.VALIDATION_SCORE_MIN_VALUE).value
    max_score = get_setting_by_key(SettingKeys.VALIDATION_SCORE_MAX_VALUE).value

    validation_errors.append(validate_title(title))
    validation_errors.append(validate_score(score, min_score, max_score))

    if is_author and video_url:
        validation_errors.append(validate_video_url(video_url))
    elif not is_author and video_url:
        validation_errors.append("Video URL provided but no authorship was claimed")

    if is_author and video_timestamp:
        validation_errors.append(validate_video_timestamp(video_timestamp))
    elif not is_author and video_timestamp:
        validation_errors.append("Video timestamp provided but no authorship was claimed")

    if is_author and special_topic:
        if not special_entry_topics:
            validation_errors.append(
                f"Special topic designation '{special_topic}' specified, but no special topics are registered")
        else:
            validation_errors.append(validate_special_topic(special_topic, special_entry_topics))
    elif not is_author and special_topic:
        validation_errors.append("Special entry topic provided but no authorship was claimed")

    return [f"[{title}] {err_msg}" for err_msg in validation_errors if err_msg is not None] or None


def validate_title(title: str) -> str | None:
    if not isinstance(title, str) or not title:
        return "Title is not a string or is empty"

    return None


def validate_score(score: float, min_score: float, max_score: float) -> str | None:
    if not isinstance(score, float) or not (min_score <= score <= max_score):
        return f"Invalid score ({score})"

    return None


def validate_video_timestamp(video_timestamp: str) -> str | None:
    if not isinstance(video_timestamp, str) or not video_timestamp:
        return "Video timestamp is not a string or is empty"

    video_timestamp_bits = video_timestamp.split(VIDEO_TIMESTAMP_SEPARATOR)

    if len(video_timestamp_bits) != 2:
        return f"Invalid video timestamp format '{video_timestamp}' (Should be '[HH:]MM:SS-[HH:]MM:SS')"

    start, end = video_timestamp_bits

    # Is a valid time format

    if not validate_time_str(start):
        return f"Invalid start timestamp ({start})"

    if not validate_time_str(end):
        return f"Invalid end timestamp ({end})"

    # The start before the end

    start_time, end_time = parse_time(start), parse_time(end)

    if start_time >= end_time:
        return f"Start is at or after the end ({video_timestamp})"

    # The duration is as set in the settings

    allowed_video_duration = get_setting_by_key(SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS).value

    if (duration := seconds_between(start_time, end_time)) != allowed_video_duration:
        return f"Invalid video duration ({duration}s [{video_timestamp}]) (Should be {allowed_video_duration} seconds)"

    return None


def validate_video_url(video_url: str) -> str | None:
    if not isinstance(video_url, str) or not video_url:
        return "Video URL is not a string or is empty"

    if isinstance(validate_url(video_url), ValidationError):
        return f"Invalid URL '{video_url}'"

    return None


def validate_special_topic(topic: str, special_entry_topics: list[SpecialEntryTopic]) -> str | None:
    if not isinstance(topic, str) or not topic:
        return "Special topic is not a string or is empty"

    if topic.lower() not in [valid_topic.designation.lower() for valid_topic in special_entry_topics]:
        return f"Invalid special topic designation '{topic}' (Should be one of the allowed designations)"

    return None
