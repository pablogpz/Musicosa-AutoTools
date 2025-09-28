from common.config.config import Config
from common.formatting.tabulate import tab
from stage_4_templates_gen.custom_types import StageFourInput, StageFourOutput


def stage_summary(config: Config, stage_input: StageFourInput, stage_output: StageFourOutput) -> str:
    templates = stage_input.templates
    generated_entries, skipped_entries, failed_entries = stage_output.entry_templates_result
    generated_presentations, skipped_presentations, failed_presentations = stage_output.presentation_templates_result

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 4 SUMMARY | Templates Generation]")
    f("")
    f(f"# Templates to generate: {len(templates) if not config.stitch_final_video else len(templates) * 2}")
    f(
        f"# Total generated or skipped templates: {
            len(generated_entries) + len(skipped_entries) + len(generated_presentations) + len(skipped_presentations)
        }"
    )
    f("")
    f(f"# Successfully generated ENTRY templates: {len(generated_entries)}")
    if len(skipped_entries) > 0:
        f(f"# Skipped ENTRY templates: {len(skipped_entries)}")
    if len(failed_entries) > 0:
        f(
            f"# Failed to generate ENTRY templates: {len(failed_entries)}\n"
            f"{'\n'.join([tab(1, f'* {template_id}') for template_id in failed_entries])}"
        )
    f(f"# Successfully generated PRESENTATION templates: {len(generated_presentations)}")
    if len(skipped_presentations) > 0:
        f(f"# Skipped PRESENTATION templates: {len(skipped_presentations)}")
    if len(failed_presentations) > 0:
        f(
            f"# Failed to generate PRESENTATION templates: {len(failed_presentations)}\n"
            f"{'\n'.join([tab(1, f'* {template_id}') for template_id in failed_presentations])}"
        )
    f("")

    return "\n".join(log_lines)
