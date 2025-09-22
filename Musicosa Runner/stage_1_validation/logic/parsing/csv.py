import os
from os.path import basename

from common.custom_types import StageException
from stage_1_validation.constants import CSV_SEPARATOR, CSV_MEMBER_NAME_HEADER, CSV_UNUSED_HEADERS
from stage_1_validation.custom_types import AwardForm, MemberSubmission, CastVote
from stage_1_validation.logic.parsing.utils import parse_score_str, unquote


def parse_award_forms_csv_folder(forms_folder: str) -> list[AwardForm]:
    award_forms: list[AwardForm] = []

    for form_file in [f for f in os.listdir(forms_folder) if f.endswith(".csv")]:
        award_forms.append(parse_award_form_csv(f"{forms_folder}/{form_file}"))

    return award_forms


def parse_award_form_csv(form_file: str) -> AwardForm:
    award_slug = basename(form_file).removesuffix(".csv")
    submissions: list[MemberSubmission] = []

    try:
        with open(form_file, "r", encoding="UTF-8-SIG") as file:
            lines = file.readlines()
            header_line = lines[0]
            submission_lines = lines[1:]

            headers = [header.replace('"', "").strip() for header in header_line.split(f"\"{CSV_SEPARATOR}\"")]

            for line in submission_lines:
                submission_values = {k: v for (k, v)
                                     in zip(headers, [unquote(v) for v in line.split(CSV_SEPARATOR)])
                                     if k not in CSV_UNUSED_HEADERS}
                try:
                    submissions.append(parse_member_submission(submission_values))
                except StageException as err:
                    raise StageException(f"[{award_slug}] {err}") from err
    except IOError as err:
        raise StageException(f"Error opening CSV form file '{form_file}'. Cause: {err}")

    return AwardForm(award_slug, submissions)


def parse_member_submission(submission_values: dict[str, str]) -> MemberSubmission:
    member_name = submission_values[CSV_MEMBER_NAME_HEADER]
    cast_votes: list[CastVote] = []

    for nominee, score_str in {k: v for (k, v) in submission_values.items() if k != CSV_MEMBER_NAME_HEADER}.items():
        try:
            score = parse_score_str(score_str) / 100
        except ValueError as err:
            raise StageException(f"[{member_name}][{nominee}] Error parsing score value '{score_str}'") from err

        cast_votes.append(CastVote(nominee, score))

    return MemberSubmission(member_name, cast_votes)
