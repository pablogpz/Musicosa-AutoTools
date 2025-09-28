from common.config.config import Config
from common.formatting.tabulate import tab
from stage_1_validation.custom_types import StageOneInput


def stage_summary(config: Config, stage_input: StageOneInput) -> str:
    forms_folder, valid_titles_file = (config.stage_1.forms_folder, config.stage_1.valid_titles_file)
    submissions = stage_input.submissions

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 1 SUMMARY | Submission Validation]")
    f("")
    f(f"Submission forms folder: '{forms_folder}'")
    f(f"Valid titles file: '{valid_titles_file}'")
    f("")
    f(
        f"Contestants ({len(submissions)}):\n"
        f"{'\n'.join([tab(1, f'* {sub.name} ({len(sub.entries)} entries)') for sub in submissions])}"
    )
    f("")

    return "\n".join(log_lines)
