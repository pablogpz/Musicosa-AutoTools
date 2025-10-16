import random

from common.custom_types import TemplateType
from common.model.models import Template
from stage_4_templates_gen.custom_types import Template as S4Template


def load_templates_from_db(generate_presentations: bool) -> list[S4Template]:
    # noinspection PyTypeChecker
    templates = [
        S4Template(
            template.entry.id,
            template.entry.title,
            TemplateType.ENTRY if not generate_presentations else (TemplateType.ENTRY | TemplateType.PRESENTATION),
        )
        for template in Template.ORM.select(Template.ORM.entry)
    ]

    random.shuffle(templates)  # Randomize order to avoid spoilers

    return templates
