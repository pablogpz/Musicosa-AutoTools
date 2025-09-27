from validators import ValidationError
from validators import url as validate_url

from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.formatting.tabulate import tab
from common.model.models import EntryTopic, SettingKeys
from common.model.settings import get_setting_by_key
from common.time.utils import parse_time, seconds_between, validate_time_str
from stage_1_validation.custom_types import ContestantSubmission, ContestantSubmissionEntry
from stage_1_validation.logic.helpers import find_duplicates


def validate_contestant_submission_collection(
    submissions: list[ContestantSubmission], valid_titles: list[str], entry_topics: list[EntryTopic] | None
) -> list[str] | None:
    contestant_count = len(submissions)
    validation_errors: list[str] = []

    if len(submissions) != contestant_count:
        validation_errors.append(f"Submission form count mismatch ({len(submissions)}) (Should be {contestant_count})")

    # Validate that each entry has exactly one author across all submissions

    author_registry: dict[str, set[str]] = {}

    for sub in submissions:
        contestant_name, entries = sub.name, sub.entries
        for entry in entries:
            title, is_author = entry.title, entry.is_author
            if is_author and title in author_registry:
                author_registry[title].add(contestant_name)
            elif is_author:
                author_registry[title] = {contestant_name}  # CAREFUL: Using 'set()' here would make a set of chars
            elif title not in author_registry:
                author_registry[title] = set()

    if entries_no_author := [entry for entry, authors in author_registry.items() if len(authors) == 0]:
        validation_errors.append(
            f"Entries with no author ({len(entries_no_author)}):\n"
            f"{'\n'.join([tab(1, f'* {title}') for title in entries_no_author])}"
        )

    if entries_multiple_authors := [entry for entry, authors in author_registry.items() if len(authors) > 1]:
        for title, authors in entries_multiple_authors:
            validation_errors.append(
                f"Entry '{title}' has multiple authors ({len(authors)}):"
                f" {', '.join([f'{author}' for author in authors])}"
            )

    # Validate each contestant submission

    for sub in submissions:
        if submission_errors := validate_contestant_submission(sub, contestant_count, valid_titles, entry_topics):
            validation_errors.extend(submission_errors)

    return [err_msg for err_msg in validation_errors] or None


def validate_contestant_submission(
    submission: ContestantSubmission,
    contestants_count: int,
    valid_titles: list[str],
    entry_topics: list[EntryTopic] | None,
) -> list[str] | None:
    round_count: int = get_setting_by_key(SettingKeys.GLOBAL_ROUND_COUNT).value  # pyright: ignore [reportOptionalMemberAccess, reportAssignmentType]

    entries = submission.entries
    entry_count = contestants_count * round_count
    validation_errors: list[str] = []

    if len(entries) != entry_count:
        validation_errors.append(f"Submission entry count mismatch ({len(entries)}) (Should be {entry_count})")

    if (authored_entries_count := len([entry for entry in entries if entry.is_author])) != round_count:
        validation_errors.append(f"Author claim count mismatch ({authored_entries_count}) (Should be {round_count})")

    if duplicates := find_duplicates([entry.title for entry in entries]):
        for title, count in duplicates:
            validation_errors.append(f"Entry '{title}' is duplicated {count} time{'s' if count > 1 else ''}")

    titles = set([entry.title for entry in entries])

    if invalid_titles := titles - set(valid_titles):
        validation_errors.append(
            f"Invalid entries ({len(invalid_titles)}):\n{'\n'.join([tab(2, f'* {title}') for title in invalid_titles])}"
        )

    if missing_titles := set(valid_titles) - titles:
        validation_errors.append(
            f"Missing entries ({len(missing_titles)}):\n{'\n'.join([tab(2, f'* {title}') for title in missing_titles])}"
        )

    for entry in entries:
        if entry_errors := validate_entry(entry, entry_topics):
            validation_errors.extend(entry_errors)

    if entry_topics:
        for topic in entry_topics:
            entries_with_topic = [entry for entry in entries if entry.topic is not None]
            occurrences = [e for e in entries_with_topic if e.topic.lower() == topic.designation.lower()]  # pyright: ignore [reportOptionalMemberAccess]

            if len(occurrences) == 0:
                validation_errors.append(f"There are no entries designated as '{topic.designation.upper()}'")

            if len(occurrences) > 1:
                validation_errors.append(
                    f"There are multiple entries ({len(occurrences)}) of topic '{topic.designation.upper()}':\n"
                    f"{'\n'.join([tab(1, f'* {entry.title}') for entry in occurrences])}"
                )

    return [f"[{submission.name}] {err_msg}" for err_msg in validation_errors] or None


def validate_entry(entry: ContestantSubmissionEntry, entry_topics: list[EntryTopic] | None) -> list[str] | None:
    title, score, is_author, video_url, video_timestamp, topic = (
        entry.title,
        entry.score,
        entry.is_author,
        entry.video_url,
        entry.video_timestamp,
        entry.topic,
    )
    validation_errors: list[str] = []

    if not is_author and video_url:
        validation_errors.append("Video URL is only allowed for authors")

    if not is_author and video_timestamp:
        validation_errors.append("Video timestamp is only allowed for authors")

    if not is_author and topic:
        validation_errors.append("Topic is only allowed for authors")

    min_score: int = get_setting_by_key(SettingKeys.VALIDATION_SCORE_MIN_VALUE).value  # pyright: ignore [reportAssignmentType, reportOptionalMemberAccess]
    max_score: int = get_setting_by_key(SettingKeys.VALIDATION_SCORE_MAX_VALUE).value  # pyright: ignore [reportAssignmentType, reportOptionalMemberAccess]

    if errors := validate_title(title):
        validation_errors.append(errors)
    if errors := validate_score(score, min_score, max_score):
        validation_errors.append(errors)

    if is_author and video_url:
        if errors := validate_video_url(video_url):
            validation_errors.append(errors)

    if is_author and video_timestamp:
        if errors := validate_video_timestamp(video_timestamp):
            validation_errors.append(errors)

    if is_author and topic:
        if not entry_topics:
            validation_errors.append(f"Topic designation '{topic}' specified, but no entry topics are expected")
        else:
            if errors := validate_topic(topic, entry_topics):
                validation_errors.append(errors)

    return [f"[{title}] {err_msg}" for err_msg in validation_errors if err_msg is not None] or None


def validate_title(title: str) -> str | None:
    if not isinstance(title, str) or not title:
        return "Title is not a string or is empty"

    return None


def validate_score(score: float, min_score: float, max_score: float) -> str | None:
    if not isinstance(score, float) or not (min_score <= score <= max_score):
        return f"Invalid score '{score}' (Should be a number between {min_score} and {max_score})"

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
        return f"Invalid start timestamp '{start}'"

    if not validate_time_str(end):
        return f"Invalid end timestamp '{end}'"

    # The start before the end

    start_time, end_time = parse_time(start), parse_time(end)

    if start_time >= end_time:  # pyright: ignore [reportOperatorIssue]
        return f"Start is at or after the end ('{video_timestamp}')"

    # The duration is as set in the settings

    allowed_video_duration: int = get_setting_by_key(SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS).value  # pyright: ignore [reportOptionalMemberAccess, reportAssignmentType]

    if (duration := seconds_between(start_time, end_time)) != allowed_video_duration:  # pyright: ignore [reportArgumentType]
        return f"Invalid video duration ({duration}s [{video_timestamp}]) (Should be {allowed_video_duration} seconds)"

    return None


def validate_video_url(video_url: str) -> str | None:
    if not isinstance(video_url, str) or not video_url:
        return "Video URL is not a string or is empty"

    if isinstance(validate_url(video_url), ValidationError):
        return f"Invalid URL '{video_url}'"

    return None


def validate_topic(topic: str, entry_topics: list[EntryTopic]) -> str | None:
    if not isinstance(topic, str) or not topic:
        return "Topic is not a string or is empty"

    if topic.lower() not in [valid_topic.designation.lower() for valid_topic in entry_topics]:
        return f"Invalid topic designation '{topic}' (Should be one of the allowed designations)"

    return None
