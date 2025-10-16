import random

from common.model.models import Entry


def load_entries_from_db() -> list[Entry]:
    entries = [entry.to_domain() for entry in Entry.ORM.select()]

    random.shuffle(entries) # Randomize order to avoid spoilers

    return entries
