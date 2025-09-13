from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_2_ranking.custom_types import StageTwoOutput, Musicosa
from stage_2_ranking.logic.ranking import rank_musicosa


def execute(musicosa: Musicosa) -> StageTwoOutput:
    if not is_setting_set(SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS):
        raise StageException(f"Setting '{SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS}' not set")

    if not musicosa:
        raise StageException("Musicosa data is empty")

    contestants_stats, entries_stats = rank_musicosa(musicosa=musicosa)

    return StageTwoOutput(contestants_stats=contestants_stats, entries_stats=entries_stats)
