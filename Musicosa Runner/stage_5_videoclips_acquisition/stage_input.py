from common.models import Entry


def load_entries_from_db() -> list[Entry]:
    return [entry.to_domain() for entry in Entry.ORM.select()]
