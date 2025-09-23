from stage_3_templates_pre_gen.custom_types import StageThreeOutput


def stage_summary(stage_output: StageThreeOutput) -> str:
    frame_settings, templates = (stage_output.frame_settings, stage_output.templates)

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 3 SUMMARY | Templates Pre-Generation Fulfillment]")
    f("")
    f(f"# Frame settings set: {len(frame_settings)}")
    f(f"# Nomination templates fulfilled: {len(templates)}")
    f("")

    return "\n".join(log_lines)
