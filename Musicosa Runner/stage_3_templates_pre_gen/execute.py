from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_3_templates_pre_gen.custom_types import StageThreeOutput, StageThreeInput
from stage_3_templates_pre_gen.logic.fulfillment import generate_unfulfilled_avatar_pairings, \
    generate_unfulfilled_frame_settings, generate_unfulfilled_templates, generate_unfulfilled_video_options, \
    generate_unfulfilled_generation_settings


def execute(stage_input: StageThreeInput) -> StageThreeOutput:
    musicosa = stage_input.musicosa

    if not is_setting_set(SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS):
        raise StageException(f"Setting '{SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS}' not set")

    if not musicosa:
        raise StageException("Musicosa data is empty")

    avatar_pairings = generate_unfulfilled_avatar_pairings(musicosa.unfulfilled_contestants, musicosa.avatars)
    frame_settings = generate_unfulfilled_frame_settings()
    templates = generate_unfulfilled_templates(musicosa.entries_index_of_unfulfilled_templates)
    generation_settings = generate_unfulfilled_generation_settings()
    video_options = generate_unfulfilled_video_options(musicosa.entries_index_of_unfulfilled_video_options)

    return StageThreeOutput(avatar_pairings, frame_settings, templates, generation_settings, video_options)
