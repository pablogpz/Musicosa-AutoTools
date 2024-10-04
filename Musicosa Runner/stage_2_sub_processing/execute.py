from common.settings import is_setting_set
from common.type_definitions import StageException
from stage_2_sub_processing.processing import process_musicosa
from stage_2_sub_processing.type_definitions import StageTwoOutput, Musicosa


def execute(musicosa: Musicosa) -> StageTwoOutput:
    if not is_setting_set("ranking.significant_decimal_digits"):
        raise StageException("Setting 'ranking.significant_decimal_digits' not set")

    if not musicosa:
        raise StageException("Musicosa data is empty")

    contestants_stats, entries_stats = process_musicosa(musicosa=musicosa)

    return StageTwoOutput(contestants_stats=contestants_stats, entries_stats=entries_stats)
