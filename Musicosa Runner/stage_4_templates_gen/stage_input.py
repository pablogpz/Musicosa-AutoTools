from common.model.models import Template
from common.types import TemplateType
from stage_4_templates_gen.defaults import DEFAULT_GENERATE_PRESENTATIONS
from stage_4_templates_gen.types import Template as S4Template


def load_templates_from_db(generate_presentations: bool = DEFAULT_GENERATE_PRESENTATIONS) -> list[S4Template]:
    return [S4Template(template.entry.id,
                       template.entry.title,
                       TemplateType.ENTRY if not generate_presentations else (
                               TemplateType.ENTRY | TemplateType.PRESENTATION))
            for template in Template.ORM.select(Template.ORM.entry)]
