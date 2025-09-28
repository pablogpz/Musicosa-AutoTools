from common.formatting.tabulate import tab
from stage_5_videoclips_acquisition.custom_types import StageFiveInput, StageFiveOutput


def stage_summary(stage_input: StageFiveInput, stage_output: StageFiveOutput) -> str:
    entries = stage_input.entries
    downloaded, skipped, failed = stage_output.download_result

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 5 SUMMARY | Videoclips Acquisition]")
    f("")
    f(f"# Loaded entries: {len(entries)}")
    f(f"# Total downloaded or skipped videoclips: {len(downloaded) + len(skipped)}")
    f("")
    f(f"# Successfully downloaded videoclips: {len(downloaded)}")
    if len(skipped) > 0:
        f(f"# Skipped videoclips: {len(skipped)}")
    if len(failed) > 0:
        f(
            f"# Failed to download videoclips: {len(failed)}\n"
            f"{'\n'.join([tab(1, f'* {entry_title}') for entry_title in failed])}"
        )
    f("")

    return "\n".join(log_lines)
