from common.settings import is_setting_set
from common.type_definitions import StageException
from stage_3_pre_templates_gen.fulfill_musicosa import generate_unfulfilled_avatar_pairings, \
    generate_unfulfilled_templates_settings, \
    generate_unfulfilled_templates, generate_unfulfilled_video_options, generate_unfulfilled_generation_settings
from stage_3_pre_templates_gen.type_definitions import StageThreeOutput, Musicosa


def execute(musicosa: Musicosa) -> StageThreeOutput:
    if not is_setting_set("validation.entry_video_duration_seconds"):
        raise StageException("Setting 'entry_video_duration_seconds' not set")

    if not musicosa:
        raise StageException("Musicosa data is empty")

    pairings = generate_unfulfilled_avatar_pairings(musicosa.unfulfilled_contestants, musicosa.available_avatars)
    template_settings = generate_unfulfilled_templates_settings()
    templates = generate_unfulfilled_templates(musicosa.entries_index_of_unfulfilled_templates)
    generation_settings = generate_unfulfilled_generation_settings()
    video_options = generate_unfulfilled_video_options(musicosa.entries_index_of_unfulfilled_video_options)

    return StageThreeOutput(avatar_pairings=pairings,
                            templates_settings=template_settings,
                            templates=templates,
                            generation_settings=generation_settings,
                            video_options=video_options)
