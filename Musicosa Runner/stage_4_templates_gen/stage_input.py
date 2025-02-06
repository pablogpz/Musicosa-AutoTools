from common.model.models import Template
from common.naming.slugify import slugify
from stage_4_templates_gen.type_definitions import Template as S4Template


def load_templates_from_db() -> list[S4Template]:
    templates: list[Template] = [r.to_domain() for r in Template.ORM.select()]

    return [S4Template(template.nomination.id,
                       slugify(f"{template.nomination.award.slug}"
                               f"-{template.nomination.game_title}"
                               f"{f"-{template.nomination.nominee}" if template.nomination.nominee else ''}"))
            for template in templates]
