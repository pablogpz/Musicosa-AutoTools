from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.time.time_utils import validate_time_str, time_str_zfill
from stage_1_sub_validation.constants import ALLOWED_DECIMAL_SEPARATOR_CHARS, NORMALIZED_DECIMAL_SEPARATOR_CHAR


def parse_score_str(score_str: str) -> float:
    standard_score_str = score_str
    for separator in ALLOWED_DECIMAL_SEPARATOR_CHARS:
        if separator in score_str:
            standard_score_str = score_str.replace(separator, NORMALIZED_DECIMAL_SEPARATOR_CHAR)
            break

    try:
        return float(standard_score_str)
    except ValueError:
        raise


def parse_video_timestamp_str(video_timestamp_str: str) -> str:
    video_timestamp = video_timestamp_str.replace(" ", "").split(VIDEO_TIMESTAMP_SEPARATOR)

    if len(video_timestamp) != 2:
        raise ValueError(f"Error parsing video timestamp '{video_timestamp_str}'")

    timestamp_start, timestamp_end = video_timestamp

    if not validate_time_str(timestamp_start):
        raise ValueError(f"Error parsing video timestamp start '{timestamp_start}'")

    if not validate_time_str(timestamp_end):
        raise ValueError(f"Error parsing video timestamp end '{timestamp_end}'")

    return f"{time_str_zfill(timestamp_start)}{VIDEO_TIMESTAMP_SEPARATOR}{time_str_zfill(timestamp_end)}"


def parse_special_topic_str(special_topic_str: str) -> str:
    return special_topic_str.strip().upper()
