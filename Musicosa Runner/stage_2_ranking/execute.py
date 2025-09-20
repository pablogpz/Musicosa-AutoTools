from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_2_ranking.custom_types import TFA, StageTwoOutput
from stage_2_ranking.logic.ranking import rank_tfa


def execute(tfa: TFA) -> StageTwoOutput:
    if not is_setting_set(SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS):
        raise StageException(f"Setting '{SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS}' not set")

    if not tfa:
        raise StageException("TFA data is empty")

    nomination_stats = rank_tfa(tfa)

    return StageTwoOutput(nomination_stats)
