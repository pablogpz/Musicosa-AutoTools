from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from common.types import StageException
from stage_2_ranking.logic.ranking import rank_tfa
from stage_2_ranking.types import TFA, StageTwoOutput


def execute(tfa: TFA) -> StageTwoOutput:
    if not is_setting_set(SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS):
        raise StageException(f"Setting '{SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS}' not set")

    if not tfa:
        raise StageException("TFA data is empty")

    nomination_stats = rank_tfa(tfa=tfa)

    return StageTwoOutput(nomination_stats=nomination_stats)
