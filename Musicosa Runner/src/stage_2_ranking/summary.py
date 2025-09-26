from common.formatting.tabulate import tab
from stage_2_ranking.custom_types import StageTwoOutput, StageTwoInput


def stage_summary(stage_input: StageTwoInput, stage_output: StageTwoOutput) -> str:
    musicosa = stage_input.musicosa
    contestants_stats, entries_stats = (stage_output.contestants_stats, stage_output.entries_stats)

    log_lines = []

    def f(content: str) -> None:
        log_lines.append(content)

    f("")
    f("[STAGE 2 SUMMARY | Ranking]")
    f("")
    f(f"# Contestants loaded: {len(musicosa.contestants)}")
    f(f"# Entries loaded: {len(musicosa.entries)}")
    f(f"# Entries ranked: {len(entries_stats)}")
    f("")
    stats_display = [(stat.contestant.name, stat.avg_given_score, stat.avg_received_score)
                     for stat in contestants_stats]
    f(f"Contestant stats (avg_given_score, avg_received_score):\n"
      f"{"\n".join([tab(1, f"* {name} (AGS: {ags}, ARS: {ars})") for name, ags, ars in stats_display])}")
    f("")

    return "\n".join(log_lines)
