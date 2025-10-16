import random

from peewee import JOIN

from common.model.models import Entry, EntryStats, Template, VideoOptions
from stage_6_video_gen.custom_types import EntryVideoOptions, Timestamp


def load_entries_video_options_from_db() -> list[EntryVideoOptions]:
    video_options = [
        EntryVideoOptions(
            entry_id=row.id,
            entry_title=row.title,
            ranking_place=row.ranking_place,
            sequence_number=row.ranking_sequence,
            timestamp=Timestamp(start=row.timestamp_start, end=row.timestamp_end),
            width=row.video_box_width_px,
            height=row.video_box_height_px,
            position_top=row.video_box_position_top_px,
            position_left=row.video_box_position_left_px,
        )
        for row in Entry.ORM.select(
            Entry.ORM.id,
            Entry.ORM.title,
            EntryStats.ORM.ranking_place,
            EntryStats.ORM.ranking_sequence,
            VideoOptions.ORM.timestamp_start,
            VideoOptions.ORM.timestamp_end,
            Template.ORM.video_box_width_px,
            Template.ORM.video_box_height_px,
            Template.ORM.video_box_position_top_px,
            Template.ORM.video_box_position_left_px,
        )
        .join(EntryStats.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == EntryStats.ORM.entry))
        .join(VideoOptions.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == VideoOptions.ORM.entry))
        .join(Template.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == Template.ORM.entry))
        .objects()
    ]

    random.shuffle(video_options)  # Randomize order to avoid spoilers

    return video_options
