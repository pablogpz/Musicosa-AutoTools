import argparse

from peewee import PeeweeException

from common.db.database import db
from common.model.models import CastVote
from common.naming.identifiers import generate_member_uuid5, generate_nomination_uuid5_from_nomination_str
from common.types import StageException
from stage_1_validation.defaults import DEFAULT_AWARD_FORMS_FOLDER
from stage_1_validation.execute import execute
from stage_1_validation.stage_input import parse_award_forms_folder, get_valid_award_slugs, get_awards_count, \
    get_members_count

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument('--award_forms_folder', default=DEFAULT_AWARD_FORMS_FOLDER)
    args = parser.parse_args()

    award_forms_folder_arg = args.award_forms_folder.strip()
    award_forms_folder = award_forms_folder_arg.removesuffix('/') if award_forms_folder_arg.endswith('/') \
        else award_forms_folder_arg

    # Data retrieval

    try:
        award_forms = parse_award_forms_folder(award_forms_folder)
        valid_award_slugs = get_valid_award_slugs()
        awards_count = get_awards_count()
        members_count = get_members_count()
    except Exception as err:
        print(f"[Stage 1 | Data retrieval] {err}")
        exit(1)

    # Stage execution

    try:
        result = execute(award_forms=award_forms, valid_award_slugs=valid_award_slugs, awards_count=awards_count,
                         members_count=members_count)
    except StageException as err:
        print(f"[Stage 1 | Execution] {err}")
        exit(1)

    if result.validation_errors:
        for validation_error in result.validation_errors:
            print(validation_error)

    # Data persistence

    raw_cast_votes: list[CastVote.ORM] = []
    for award in award_forms:
        for submission in award.submissions:
            for cast_vote in submission.cast_votes:
                raw_cast_votes.append(
                    CastVote.ORM(member=generate_member_uuid5(submission.name).hex,
                                 nomination=generate_nomination_uuid5_from_nomination_str(cast_vote.nomination,
                                                                                          award.award_slug).hex,
                                 score=cast_vote.score))
    try:
        with db.atomic():
            CastVote.ORM.insert_many([vote.__data__ for vote in raw_cast_votes]).execute()  # CAREFUL!
    except PeeweeException as err:
        print(f"[Stage 1 | Data persistence] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 1 SUMMARY | Submissions Validation]")
    print(f"  Award forms folder: '{award_forms_folder}'")
    print(f"  Valid award slugs: {valid_award_slugs}")
    print(f"  Awards count: {awards_count}")
    print(f"  Members count: {members_count}")
    print("")
    print(f"  # Award forms loaded: {len(award_forms)}")
