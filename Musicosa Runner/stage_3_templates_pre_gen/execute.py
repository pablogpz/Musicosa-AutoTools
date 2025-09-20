from common.custom_types import StageException
from stage_3_templates_pre_gen.custom_types import StageThreeOutput, TFA
from stage_3_templates_pre_gen.logic.fulfillment import generate_unfulfilled_frame_settings, \
    generate_unfulfilled_templates


def execute(tfa: TFA) -> StageThreeOutput:
    if not tfa:
        raise StageException("TFA data is empty")

    frame_settings = generate_unfulfilled_frame_settings()
    templates = generate_unfulfilled_templates(tfa.nominations_index_of_unfulfilled_templates)

    return StageThreeOutput(frame_settings, templates)
