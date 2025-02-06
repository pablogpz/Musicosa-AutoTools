from common.type_definitions import StageException
from stage_3_templates_pre_gen.logic.fulfill_musicosa import generate_unfulfilled_templates_settings, \
    generate_unfulfilled_templates
from stage_3_templates_pre_gen.type_definitions import StageThreeOutput, TFA


def execute(tfa: TFA) -> StageThreeOutput:
    if not tfa:
        raise StageException("TFA data is empty")

    template_settings = generate_unfulfilled_templates_settings()
    templates = generate_unfulfilled_templates(tfa.nominations_index_of_unfulfilled_templates)

    return StageThreeOutput(templates_settings=template_settings, templates=templates)
