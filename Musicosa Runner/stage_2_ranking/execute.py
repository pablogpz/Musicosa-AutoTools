from common.model.settings import is_setting_set
from common.types import StageException
from stage_2_ranking.logic.ranking import process_tfa
from stage_2_ranking.types import TFA, StageTwoOutput


def execute(tfa: TFA) -> StageTwoOutput:
    if not is_setting_set("ranking.significant_decimal_digits"):
        raise StageException("Setting 'ranking.significant_decimal_digits' not set")

    if not tfa:
        raise StageException("TFA data is empty")

    nomination_stats = process_tfa(tfa=tfa)

    return StageTwoOutput(nomination_stats=nomination_stats)
