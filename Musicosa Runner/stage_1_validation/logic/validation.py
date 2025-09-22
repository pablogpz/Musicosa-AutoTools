from common.model.models import SettingKeys
from common.model.settings import get_setting_by_key
from stage_1_validation.custom_types import AwardForm, MemberSubmission


def validate_award_form_collection(award_forms: list[AwardForm],
                                   valid_award_slugs: list[str],
                                   award_count: int,
                                   member_count: int) -> list[str] | None:
    validation_errors: list[str] = []

    if len(award_forms) != award_count:
        validation_errors.append(f"Award count mismatch ({len(award_forms)}) (Should be {award_count})")

    for award_form in award_forms:
        if errors := validate_award_form(award_form, valid_award_slugs, member_count):
            validation_errors.extend(errors)

    return [err_msg for err_msg in validation_errors] or None


def validate_award_form(award_form: AwardForm, valid_award_slugs: list[str], member_count: int) -> list[str] | None:
    validation_errors: list[str] = []

    if award_form.award_slug not in valid_award_slugs:
        validation_errors.append(f"Invalid award slug '{award_form.award_slug}'")

    if len(award_form.submissions) != member_count:
        validation_errors.append(f"Member count mismatch ({len(award_form.submissions)}) (Should be {member_count})")

    for submission in award_form.submissions:
        if errors := validate_member_submission(submission):
            validation_errors.extend(errors)

    return [err_msg for err_msg in validation_errors] or None


def validate_member_submission(submission: MemberSubmission) -> list[str] | None:
    validation_errors: list[str] = []

    if not submission.name:
        validation_errors.append(f"Member name is empty")

    min_score = get_setting_by_key(SettingKeys.VALIDATION_SCORE_MIN_VALUE).value
    max_score = get_setting_by_key(SettingKeys.VALIDATION_SCORE_MAX_VALUE).value

    for cast_vote in submission.cast_votes:
        if cast_vote.nomination is None or len(cast_vote.nomination) == 0:
            validation_errors.append(f"Nomination is empty")

        if error := validate_score(cast_vote.score, min_score, max_score):
            validation_errors.append(f"[{cast_vote.nomination}] {error}")

    return [f"[{submission.name}] {err_msg}" for err_msg in validation_errors] or None


def validate_score(score: float, min_score: float, max_score: float) -> str | None:
    if not isinstance(score, float) or not (min_score <= score <= max_score):
        return f"Invalid score '{score}' (Should be a number between {min_score} and {max_score})"

    return None
