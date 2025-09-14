from common.custom_types import TemplateType
from common.model.models import Template
from common.naming.slugify import slugify
from stage_4_templates_gen.custom_types import Template as S4_Template


def load_templates_from_db(generate_presentations: bool) -> list[S4_Template]:
    templates: list[Template] = [r.to_domain() for r in Template.ORM.select()]

    # noinspection PyTypeChecker
    return [S4_Template(template.nomination.id,
                        slugify(f"{template.nomination.award.slug}"
                                f"-{template.nomination.game_title}"
                                f"{f"-{template.nomination.nominee}" if template.nomination.nominee else ''}"),
                        TemplateType.ENTRY if not generate_presentations else (
                                TemplateType.ENTRY | TemplateType.PRESENTATION))
            for template in templates]
