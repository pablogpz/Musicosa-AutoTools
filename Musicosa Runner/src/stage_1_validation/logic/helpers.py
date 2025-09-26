from typing import Iterable


def find_duplicates[T](collection: Iterable[T]) -> list[tuple[T, int]] | None:
    duplicates_registry: dict[T, int] = {}
    aux_set = set()

    for item in collection:
        initial_length = len(aux_set)
        aux_set.add(item)
        if initial_length == len(aux_set):
            if item in duplicates_registry:
                duplicates_registry[item] += 1
            else:
                duplicates_registry[item] = 1

    return [duplicate for duplicate in duplicates_registry.items()] or None
