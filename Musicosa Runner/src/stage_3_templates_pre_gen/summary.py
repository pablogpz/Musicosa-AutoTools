from stage_3_templates_pre_gen.custom_types import StageThreeOutput


def stage_summary(stage_output: StageThreeOutput) -> str:
    avatar_pairings = stage_output.avatar_pairings
    frame_settings = stage_output.frame_settings
    templates = stage_output.templates
    generation_settings = stage_output.generation_settings
    video_options = stage_output.video_options

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 3 SUMMARY | Templates Pre-Generation Fulfillment]")
    f("")
    f(f"# Paired contestants to avatars: {len(avatar_pairings)}")
    f(f"# Frame settings set: {len(frame_settings)}")
    f(f"# Fulfilled entry templates: {len(templates)}")
    f(f"# Generation general settings set: {len(generation_settings)}")
    f(f"# Fulfilled entry video options: {len(video_options)}")
    f("")

    return "\n".join(log_lines)
