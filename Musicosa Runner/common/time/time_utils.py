from datetime import time


def time_str_zfill(time_str: str) -> str | None:
    time_bits = time_str.split(":")

    if not (len(time_bits) == 2 or len(time_bits) == 3):
        return None

    if len(time_bits) == 2:
        time_bits.insert(0, "00")
        time_bits[1] = time_bits[1].zfill(2)
    else:
        time_bits[0] = time_bits[0].zfill(2)
        time_bits[1] = time_bits[1].zfill(2)

    return ":".join(time_bits)


def validate_time_str(time_str: str) -> bool:
    timestamp_bits = time_str.split(":")

    if not (len(timestamp_bits) == 2 or len(timestamp_bits) == 3):
        return False

    try:
        time.fromisoformat(time_str_zfill(time_str))
        return True
    except ValueError:
        return False


def parse_time(time_str: str) -> time | None:
    if not validate_time_str(time_str):
        return None

    return time.fromisoformat(time_str_zfill(time_str))


def time_to_seconds(time_value: time) -> int:
    return time_value.hour * 3600 + time_value.minute * 60 + time_value.second


def seconds_between(start: time, end: time) -> int:
    return time_to_seconds(end) - time_to_seconds(start)
