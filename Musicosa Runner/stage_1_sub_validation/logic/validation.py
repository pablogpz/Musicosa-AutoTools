from common.model.settings import get_setting_by_key
from stage_1_sub_validation.type_definitions import AwardForm, MemberSubmission


def validate_score(score: float, min_score: float, max_score: float) -> str | None:
    if not isinstance(score, float) or not (min_score <= score <= max_score):
        return f"Invalid score ({score})"

    return None


def validate_member_submission(submission: MemberSubmission) -> list[str] | None:
    validation_errors: list[str] = []

    if not submission.name:
        validation_errors.append(f"Member name is empty")

    min_score = get_setting_by_key("validation.score_min_value").value
    max_score = get_setting_by_key("validation.score_max_value").value

    for cast_vote in submission.cast_votes:
        if cast_vote.nomination is None or len(cast_vote.nomination) == 0:
            validation_errors.append(f"Nomination is empty")

        if error := validate_score(cast_vote.score, min_score, max_score):
            validation_errors.append(f"[{cast_vote.nomination}] {error}")

    return [f"[{submission.name}] {err_msg}" for err_msg in validation_errors] or None


def validate_award_form(award_form: AwardForm, valid_award_slugs: list[str], members_count: int) -> list[str] | None:
    validation_errors: list[str] = []

    if award_form.award_slug not in valid_award_slugs:
        validation_errors.append(f"Invalid award slug '{award_form.award_slug}'")

    if len(award_form.submissions) != members_count:
        validation_errors.append(f"Members count mismatch ({len(award_form.submissions)}) (Should be {members_count})")

    for submission in award_form.submissions:
        if errors := validate_member_submission(submission):
            validation_errors.extend(errors)

    return [err_msg for err_msg in validation_errors] or None


def validate_award_form_collection(award_forms: list[AwardForm],
                                   valid_award_slugs: list[str],
                                   awards_count: int,
                                   members_count: int) -> list[str] | None:
    validation_errors: list[str] = []

    if len(award_forms) != awards_count:
        validation_errors.append(f"Awards count mismatch ({len(award_forms)}) (Should be {awards_count})")

    for award_form in award_forms:
        if errors := validate_award_form(award_form, valid_award_slugs, members_count):
            validation_errors.extend(errors)

    return [err_msg for err_msg in validation_errors] or None
