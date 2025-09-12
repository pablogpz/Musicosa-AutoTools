from common.model.models import Template
from common.naming.slugify import slugify
from common.types import TemplateType
from stage_4_templates_gen.defaults import DEFAULT_GENERATE_PRESENTATIONS
from stage_4_templates_gen.types import Template as S4Template


def load_templates_from_db(generate_presentations: bool = DEFAULT_GENERATE_PRESENTATIONS) -> list[S4Template]:
    templates: list[Template] = [r.to_domain() for r in Template.ORM.select()]

    return [S4Template(template.nomination.id,
                       slugify(f"{template.nomination.award.slug}"
                               f"-{template.nomination.game_title}"
                               f"{f"-{template.nomination.nominee}" if template.nomination.nominee else ''}"),
                       TemplateType.ENTRY if not generate_presentations else (
                               TemplateType.ENTRY | TemplateType.PRESENTATION))
            for template in templates]
