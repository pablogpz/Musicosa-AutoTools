from common.config.config import Config
from common.formatting.tabulate import tab
from stage_6_video_gen.custom_types import StageSixInput, StageSixOutput


def stage_summary(config: Config, stage_input: StageSixInput, stage_output: StageSixOutput) -> str:
    stitch_final_video = config.stitch_final_video
    video_options = stage_input.nominations_video_options
    missing_templates = stage_output.missing_templates
    missing_videoclips = stage_output.missing_videoclips
    generated, skipped, failed = stage_output.video_generation_result
    final_videos_files = stage_output.final_videos_files

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 6 SUMMARY | Video Generation]")
    f("")
    f(f"# Loaded video options: {len(video_options)}")
    f(f"# Total generated or skipped video bits: {len(generated) + len(skipped)}")
    f("")
    if missing_templates:
        f(f"Missing ENTRY TEMPLATE source files:\n"
          f"{"\n".join([tab(1, f"* {missing}") for missing in missing_templates])}")
        f("")
    if missing_videoclips:
        f(f"Missing VIDEOCLIP source files:\n"
          f"{"\n".join([tab(1, f"* {missing}") for missing in missing_videoclips])}")
        f("")
    f(f"# Successfully generated video bits: {len(generated)}")
    if len(skipped) > 0:
        f(f"# Skipped video bits: {len(skipped)}")
    if len(failed) > 0:
        f(f"# Failed to generate video bits: {len(failed)}\n"
          f"{"\n".join([tab(1, f"* {entry_title}") for entry_title in failed])}")
    if stitch_final_video:
        f("")
        f(f"Final videos:\n"
          f"{"\n".join([tab(1, f"* {video}") for video in final_videos_files])}")
    f("")

    return "\n".join(log_lines)
