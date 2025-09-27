from common.custom_types import StageException
from common.model.models import SettingKeys
from common.model.settings import is_setting_set
from stage_2_ranking.custom_types import StageTwoInput, StageTwoOutput
from stage_2_ranking.logic.ranking import rank_tfa


def execute(stage_input: StageTwoInput) -> StageTwoOutput:
    tfa = stage_input.tfa

    if not is_setting_set(SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS):
        raise StageException(f"Setting '{SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS}' not set")

    if not tfa:
        raise StageException("TFA data is empty")

    if len(tfa.awards) == 0:
        raise StageException("Award list is empty")

    nomination_stats = rank_tfa(tfa)

    return StageTwoOutput(nomination_stats)
