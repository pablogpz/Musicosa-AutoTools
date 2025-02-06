from common.model.settings import is_setting_set
from common.type_definitions import StageException
from stage_2_sub_processing.logic.processing import process_tfa
from stage_2_sub_processing.type_definitions import TFA, StageTwoOutput


def execute(tfa: TFA) -> StageTwoOutput:
    if not is_setting_set("ranking.significant_decimal_digits"):
        raise StageException("Setting 'ranking.significant_decimal_digits' not set")

    if not tfa:
        raise StageException("TFA data is empty")

    nomination_stats = process_tfa(tfa=tfa)

    return StageTwoOutput(nomination_stats=nomination_stats)
