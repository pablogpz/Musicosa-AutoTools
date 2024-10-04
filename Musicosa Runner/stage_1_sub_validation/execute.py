from common.models import SpecialEntryTopic
from common.settings import is_setting_set
from common.type_definitions import StageException
from stage_1_sub_validation.type_definitions import StageOneOutput, ContestantSubmission
from stage_1_sub_validation.validation import validate_contestant_submission_collection


def execute(submissions: list[ContestantSubmission], valid_titles: list[str],
            special_entry_topics: list[SpecialEntryTopic] | None) -> StageOneOutput:
    if not is_setting_set("globals.rounds_count"):
        raise StageException("Setting 'globals.rounds_count' not set")

    if not is_setting_set("validation.score_min_value"):
        raise StageException("Setting 'validation.score_min_value' not set")

    if not is_setting_set("validation.score_max_value"):
        raise StageException("Setting 'validation.score_max_value' not set")

    if not is_setting_set("validation.entry_video_duration_seconds"):
        raise StageException("Setting 'validation.entry_video_duration_seconds' not set")

    if not valid_titles:
        raise StageException("Valid entry titles list is empty")

    validation_errors = validate_contestant_submission_collection(submissions=submissions,
                                                                  valid_titles=valid_titles,
                                                                  special_entry_topics=special_entry_topics)

    return StageOneOutput(validation_errors=validation_errors)
