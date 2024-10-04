from models import Template
from stage_4_templates_gen.type_definitions import Template as S4Template


def load_templates_from_db() -> list[S4Template]:
    return [S4Template(template.entry.id, template.entry.title) for template in Template.ORM.select(Template.ORM.entry)]
