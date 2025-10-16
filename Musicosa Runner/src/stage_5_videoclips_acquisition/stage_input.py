import random

from common.model.models import Videoclip


def load_videoclips_from_db() -> list[Videoclip]:
    entries = [r.to_domain() for r in Videoclip.ORM.select()]

    random.shuffle(entries) # Randomize order to avoid spoilers

    return entries
