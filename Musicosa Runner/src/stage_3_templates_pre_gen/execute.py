from common.custom_types import StageException
from stage_3_templates_pre_gen.custom_types import StageThreeInput, StageThreeOutput
from stage_3_templates_pre_gen.logic.fulfillment import (
    fulfill_unfulfilled_frame_settings,
    fulfill_unfulfilled_templates,
)


def execute(stage_input: StageThreeInput) -> StageThreeOutput:
    tfa = stage_input.tfa

    if not tfa:
        raise StageException("TFA data is empty")

    frame_settings = fulfill_unfulfilled_frame_settings()
    templates = fulfill_unfulfilled_templates(tfa.nominations_index_unfulfilled_templates)

    return StageThreeOutput(frame_settings, templates)
