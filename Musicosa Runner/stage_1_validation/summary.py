from common.config.config import Config
from common.formatting.tabulate import tab
from stage_1_validation.custom_types import StageOneInput


def stage_summary(config: Config, stage_input: StageOneInput) -> str:
    award_forms_folder = config.stage_1.award_forms_folder
    valid_award_slugs, award_count, member_count, award_forms = (
        stage_input.valid_award_slugs, stage_input.award_count, stage_input.member_count, stage_input.award_forms)

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 1 SUMMARY | Submission Validation]")
    f("")
    f(f"Award forms folder: '{award_forms_folder}'")
    f(f"Valid award slugs:\n"
      f"{"\n".join([tab(1, f"* {award}") for award in valid_award_slugs])}")
    f(f"Award count: {award_count}")
    f(f"Member count: {member_count}")
    f("")
    f(f"# Award forms loaded: {len(award_forms)}")
    f("")

    return "\n".join(log_lines)
