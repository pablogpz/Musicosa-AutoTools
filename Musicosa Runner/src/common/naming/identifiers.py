from uuid import NAMESPACE_OID, UUID, uuid5

CONTESTANTS_NAMESPACE = NAMESPACE_OID
ENTRIES_NAMESPACE = NAMESPACE_OID


def generate_contestant_uuid5(contestant_name: str) -> UUID:
    if not contestant_name:
        raise ValueError("Contestant name cannot be empty")

    return uuid5(CONTESTANTS_NAMESPACE, contestant_name)


def generate_entry_uuid5(entry_title: str) -> UUID:
    if not entry_title:
        raise ValueError("Entry title cannot be empty")

    return uuid5(ENTRIES_NAMESPACE, entry_title)
