from common.model.settings import is_setting_set
from common.types import StageException
from stage_3_templates_pre_gen.logic.fulfillment import generate_unfulfilled_avatar_pairings, \
    generate_unfulfilled_frame_settings, generate_unfulfilled_templates, generate_unfulfilled_video_options, \
    generate_unfulfilled_generation_settings
from stage_3_templates_pre_gen.types import StageThreeOutput, Musicosa


def execute(musicosa: Musicosa) -> StageThreeOutput:
    if not is_setting_set("validation.entry_video_duration_seconds"):
        raise StageException("Setting 'entry_video_duration_seconds' not set")

    if not musicosa:
        raise StageException("Musicosa data is empty")

    pairings = generate_unfulfilled_avatar_pairings(musicosa.unfulfilled_contestants, musicosa.available_avatars)
    frame_settings = generate_unfulfilled_frame_settings()
    templates = generate_unfulfilled_templates(musicosa.entries_index_of_unfulfilled_templates)
    generation_settings = generate_unfulfilled_generation_settings()
    video_options = generate_unfulfilled_video_options(musicosa.entries_index_of_unfulfilled_video_options)

    return StageThreeOutput(avatar_pairings=pairings,
                            frame_settings=frame_settings,
                            templates=templates,
                            generation_settings=generation_settings,
                            video_options=video_options)
