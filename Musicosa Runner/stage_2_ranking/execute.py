from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_2_ranking.custom_types import StageTwoOutput, StageTwoInput
from stage_2_ranking.logic.ranking import rank_musicosa


def execute(stage_input: StageTwoInput) -> StageTwoOutput:
    musicosa = stage_input.musicosa

    if not is_setting_set(SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS):
        raise StageException(f"Setting '{SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS}' not set")

    if not musicosa:
        raise StageException("Musicosa data is empty")

    if len(musicosa.entries) == 0:
        raise StageException("Entry list is empty")

    if len(musicosa.contestants) == 0:
        raise StageException("Contestant list is empty")

    contestants_stats, entries_stats = rank_musicosa(musicosa)

    return StageTwoOutput(contestants_stats, entries_stats)
