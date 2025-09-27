from common.model.models import Videoclip


def load_videoclips_from_db() -> list[Videoclip]:
    return [r.to_domain() for r in Videoclip.ORM.select()]
