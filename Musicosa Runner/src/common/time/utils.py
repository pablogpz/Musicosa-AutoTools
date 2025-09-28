from datetime import time

from common.constants import VIDEO_TIMESTAMP_SEPARATOR


def validate_time_str(time_str: str) -> bool:
    timestamp_bits = time_str.split(":")

    if len(timestamp_bits) not in [2, 3]:
        return False

    try:
        time.fromisoformat(time_str_zfill(time_str))
        return True
    except ValueError:
        return False


def validate_video_timestamp_str(timestamp_str: str, duration: int | None = None) -> bool:
    timestamp_bits = timestamp_str.split(VIDEO_TIMESTAMP_SEPARATOR)

    if len(timestamp_bits) != 2:
        return False

    start, end = timestamp_bits

    if not validate_time_str(start) or not validate_time_str(end):
        return False

    start_time, end_time = parse_time(start), parse_time(end)

    if start_time >= end_time:  # pyright: ignore [reportOperatorIssue]
        return False

    if duration and seconds_between(start_time, end_time) != duration:  # pyright: ignore [reportArgumentType]
        return False

    return True


def parse_time(time_str: str) -> time | None:
    if not validate_time_str(time_str):
        return None

    return time.fromisoformat(time_str_zfill(time_str))


def time_str_zfill(time_str: str) -> str:
    time_bits = time_str.split(":")

    if len(time_bits) not in [2, 3]:
        return ""

    if len(time_bits) == 2:
        time_bits.insert(0, "00")
        time_bits[1] = time_bits[1].zfill(2)
    else:
        time_bits[0] = time_bits[0].zfill(2)
        time_bits[1] = time_bits[1].zfill(2)

    return ":".join(time_bits)


def time_to_seconds(time_value: time) -> int:
    return time_value.hour * 3600 + time_value.minute * 60 + time_value.second


def seconds_between(start: time, end: time) -> int:
    return time_to_seconds(end) - time_to_seconds(start)
