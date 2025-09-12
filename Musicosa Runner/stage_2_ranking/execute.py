from common.model.settings import is_setting_set
from common.types import StageException
from stage_2_ranking.logic.ranking import musicosa_ranking
from stage_2_ranking.types import StageTwoOutput, Musicosa


def execute(musicosa: Musicosa) -> StageTwoOutput:
    if not is_setting_set("ranking.significant_decimal_digits"):
        raise StageException("Setting 'ranking.significant_decimal_digits' not set")

    if not musicosa:
        raise StageException("Musicosa data is empty")

    contestants_stats, entries_stats = musicosa_ranking(musicosa=musicosa)

    return StageTwoOutput(contestants_stats=contestants_stats, entries_stats=entries_stats)
