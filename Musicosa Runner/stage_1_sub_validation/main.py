import argparse

from peewee import PeeweeException

from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.model.models import Entry, Scoring, VideoOptions, Contestant, SpecialEntryTopic
from common.naming.identifiers import generate_contestant_uuid5, generate_entry_uuid5
from common.time.time_utils import parse_time
from common.type_definitions import StageException
from stage_1_sub_validation.defaults import DEFAULT_CSV_FORMS_FOLDER, DEFAULT_VALID_TITLES_FILE
from stage_1_sub_validation.execute import execute
from stage_1_sub_validation.stage_input import get_submissions_from_forms_folder, get_submission_entry_valid_titles, \
    get_special_entry_topics_from_db

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_forms_folder", default=DEFAULT_CSV_FORMS_FOLDER)
    parser.add_argument("--valid_titles_file", default=DEFAULT_VALID_TITLES_FILE)
    args = parser.parse_args()

    forms_folder_arg = args.csv_forms_folder.strip()
    forms_folder = forms_folder_arg.removesuffix("/") if forms_folder_arg.endswith("/") else forms_folder_arg

    valid_titles_file = args.valid_titles_file.strip()

    # Data retrieval

    try:
        submissions = get_submissions_from_forms_folder(forms_folder)
        valid_titles = get_submission_entry_valid_titles(forms_folder, valid_titles_file)
        special_entry_topics = get_special_entry_topics_from_db()
    except Exception as err:
        print(f"[Stage 1 | Data retrieval] {err}")
        exit(1)

    # Stage execution

    try:
        result = execute(submissions=submissions, valid_titles=valid_titles, special_entry_topics=special_entry_topics)
    except StageException as err:
        print(f"[Stage 1 | Execution] {err}")
        exit(1)

    if result.validation_errors:
        for validation_error in result.validation_errors:
            print(validation_error)

    # Data persistence

    contestants_by_name: dict[str, Contestant] = {}
    for sub in submissions:
        contestants_by_name[sub.name] = Contestant(id=generate_contestant_uuid5(sub.name).hex, name=sub.name,
                                                   avatar=None)

    entries_by_name: dict[str, Entry] = {}
    for sub in submissions:
        for entry in sub.entries:
            if entry.is_author:
                special_topic = SpecialEntryTopic(designation=entry.special_topic) if entry.special_topic else None
                entries_by_name[entry.title] = Entry(id=generate_entry_uuid5(entry.title).hex,
                                                     title=entry.title,
                                                     author=contestants_by_name[sub.name],
                                                     video_url=entry.video_url,
                                                     special_topic=special_topic)

    scoring_entries: list[Scoring] = []
    for sub in submissions:
        for entry in sub.entries:
            scoring_entries.append(Scoring(contestant=contestants_by_name[sub.name],
                                           entry=entries_by_name[entry.title],
                                           score=entry.score))

    video_options: list[VideoOptions] = []
    for sub in submissions:
        for entry in sub.entries:
            if entry.video_timestamp:
                start, end = entry.video_timestamp.split(VIDEO_TIMESTAMP_SEPARATOR)
                video_options.append(VideoOptions(entry=entries_by_name[entry.title],
                                                  timestamp_start=parse_time(start),
                                                  timestamp_end=parse_time(end)))

    try:
        with db.atomic():
            Contestant.ORM.insert_many(bulk_pack(contestants_by_name.values())).execute()
            Entry.ORM.insert_many(bulk_pack(entries_by_name.values())).execute()
            Scoring.ORM.insert_many(bulk_pack(scoring_entries)).execute()
            VideoOptions.ORM.insert_many(bulk_pack(video_options)).execute()
    except PeeweeException as err:
        print(f"[Stage 1 | Data persistence] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 1 SUMMARY | Submissions Validation]")
    print(f"  Submission forms folder: '{forms_folder}'")
    print(f"  Valid titles file: '{valid_titles_file}'")
    print("")
    print(f"  # Submission forms loaded: {len(submissions)}")
    contestant_names = [sub.name for sub in submissions]
    print(f"  Contestants ({len(contestant_names)}): {", ".join(contestant_names)}")
    print("")
    for index, name in enumerate(contestant_names):
        if len(submissions[index].entries) >= 3:
            print(f"[{name} ({len(submissions[index].entries)})] - Entries sample")
            for entry in submissions[index].entries[0:3]:
                print(f"    {entry}")
            print("")
