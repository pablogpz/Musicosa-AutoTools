import argparse

from peewee import PeeweeException

from common.config.loader import load_config
from common.constants import VIDEO_TIMESTAMP_SEPARATOR
from common.custom_types import StageException
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.model.models import Entry, Scoring, VideoOptions, Contestant, SpecialEntryTopic
from common.naming.identifiers import generate_contestant_uuid5, generate_entry_uuid5
from common.time.utils import parse_time
from stage_1_validation.custom_types import StageOneInput
from stage_1_validation.execute import execute
from stage_1_validation.stage_input import get_submissions_from_forms_folder, get_valid_titles, \
    get_special_topics_from_db
from stage_1_validation.summary import stage_summary

if __name__ == "__main__":

    # Configuration

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file")
    args = parser.parse_args()

    try:
        config = load_config(args.config_file.strip() if args.config_file else None)
    except FileNotFoundError | IOError | TypeError as err:
        print(f"[Stage 1 | Configuration] {err}")
        exit(1)

    forms_folder = config.stage_1.forms_folder
    valid_titles_file = config.stage_1.valid_titles_file
    contestant_name_coords = config.stage_1.contestant_name_coords
    entries_data_coords = config.stage_1.entries_data_coords

    # Data retrieval

    try:
        submissions = get_submissions_from_forms_folder(forms_folder, contestant_name_coords, entries_data_coords)
        valid_titles = get_valid_titles(forms_folder, valid_titles_file)
        special_entry_topics = get_special_topics_from_db()
    except Exception as err:
        print(f"[Stage 1 | Data retrieval] {err}")
        exit(1)

    stage_input = StageOneInput(submissions, valid_titles, special_entry_topics)

    # Stage execution

    try:
        result = execute(stage_input)
    except StageException as err:
        print(f"[Stage 1 | Execution] {err}")
        exit(1)

    if result.validation_errors:
        for validation_error in result.validation_errors:
            print(validation_error)

    # Data persistence

    contestants_by_name: dict[str, Contestant] = {}
    for sub in submissions:
        contestants_by_name[sub.name] = Contestant(id=generate_contestant_uuid5(sub.name).hex,
                                                   name=sub.name,
                                                   avatar=None)

    entries_by_title: dict[str, Entry] = {}
    for sub in submissions:
        for entry in sub.entries:
            if entry.is_author:
                # noinspection PyTypeChecker
                special_topic = SpecialEntryTopic(designation=entry.special_topic) if entry.special_topic else None
                entries_by_title[entry.title] = Entry(id=generate_entry_uuid5(entry.title).hex,
                                                      title=entry.title,
                                                      author=contestants_by_name[sub.name],
                                                      video_url=entry.video_url,
                                                      special_topic=special_topic)

    scoring_entries: list[Scoring] = []
    for sub in submissions:
        for entry in sub.entries:
            scoring_entries.append(Scoring(contestant=contestants_by_name[sub.name],
                                           entry=entries_by_title[entry.title],
                                           score=entry.score))

    video_options: list[VideoOptions] = []
    for sub in submissions:
        for entry in sub.entries:
            if entry.video_timestamp:
                start, end = entry.video_timestamp.split(VIDEO_TIMESTAMP_SEPARATOR)
                video_options.append(VideoOptions(entry=entries_by_title[entry.title],
                                                  timestamp_start=parse_time(start),
                                                  timestamp_end=parse_time(end)))

    try:
        with db.atomic() as tx:
            Contestant.ORM.insert_many(bulk_pack(contestants_by_name.values())).execute()
            Entry.ORM.insert_many(bulk_pack(entries_by_title.values())).execute()
            Scoring.ORM.insert_many(bulk_pack(scoring_entries)).execute()
            VideoOptions.ORM.insert_many(bulk_pack(video_options)).execute()
    except PeeweeException as err:
        tx.rollback()
        print(f"[Stage 1 | Data persistence] {err}")
        exit(1)

    # Stage execution summary

    print(stage_summary(config, stage_input))
