from stage_2_ranking.custom_types import StageTwoInput, StageTwoOutput


def stage_summary(stage_input: StageTwoInput, stage_output: StageTwoOutput) -> str:
    awards = stage_input.tfa.awards
    nomination_stats = stage_output.nomination_stats

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 2 SUMMARY | Ranking]")
    f("")
    f(f"# Awards loaded: {len(awards)}")
    f("")
    f(f"# Ranked nominations: {len(nomination_stats)}")
    f("")

    return "\n".join(log_lines)
