import re
from typing import Any, Iterable


def get_missing_sequence_numbers(kv_store: dict[int, Any], expected_numbers: Iterable[int]) -> list[int]:
    return [number for number in expected_numbers if number not in kv_store]


def format_sequence_numbers(sequence_numbers: list[int]) -> str:
    display_bits: list[str] = []
    sorted_sequence = sorted(sequence_numbers)

    cursor = 0
    while cursor < len(sequence_numbers):
        current_number = sorted_sequence[cursor]
        sequence_group = [current_number]

        cursor += 1
        while cursor < len(sequence_numbers) and sorted_sequence[cursor - 1] + 1 == sorted_sequence[cursor]:
            sequence_group.append(sorted_sequence[cursor])
            cursor += 1

        if len(sequence_group) == 1:
            display_bits.append(f"{current_number}")
        else:
            display_bits.append(f"{current_number}..{sequence_group[-1]}")

    return ", ".join(display_bits)


def validate_sequence_selection(selection: str, kv_store: dict[int, Any]) -> bool:
    selection = selection.replace(" ", "")

    if selection == "":
        return True
    elif selection.isdigit():
        return int(selection) in kv_store
    elif re.match(r"^\d*:\d*$", selection) is not None:
        range_bits = selection.split(":")
        start = int(range_bits[0]) if range_bits[0] else 1
        end = int(range_bits[1]) if range_bits[1] else len(kv_store)
        return all([number in kv_store for number in range(start, end + 1)])
    else:
        return False


def parse_sequence_selection_of_kvstore(selection: str,
                                        kv_store: dict[int, Any],
                                        missing_numbers_in_kvstore: list[int]) -> list[int] | None:
    if not validate_sequence_selection(selection, kv_store):
        return None

    selection = selection.replace(" ", "")

    if selection == "":
        return missing_numbers_in_kvstore
    elif selection.isdigit():
        return [int(selection)]
    else:
        range_bits = selection.split(":")
        start = int(range_bits[0]) if range_bits[0] else 1
        end = int(range_bits[1]) if range_bits[1] else len(kv_store)
        return list(range(start, end + 1))
