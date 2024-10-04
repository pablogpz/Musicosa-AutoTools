from peewee import JOIN

from common.models import Entry, EntryStats, VideoOptions, Template
from stage_6_final_video_bits_gen.type_definitions import EntryVideoOptions, Timestamp


def load_entries_video_options_from_db() -> list[EntryVideoOptions]:
    return ([EntryVideoOptions(entry_id=row.id,
                               entry_title=row.title,
                               sequence_number=row.ranking_sequence,
                               timestamp=Timestamp(start=row.timestamp_start, end=row.timestamp_end),
                               width=row.video_box_width_px,
                               height=row.video_box_height_px,
                               position_top=row.video_box_position_top_px,
                               position_left=row.video_box_position_left_px)
             for row in
             Entry.ORM
             .select(Entry.ORM.id,
                     Entry.ORM.title,
                     EntryStats.ORM.ranking_sequence,
                     VideoOptions.ORM.timestamp_start,
                     VideoOptions.ORM.timestamp_end,
                     Template.ORM.video_box_width_px,
                     Template.ORM.video_box_height_px,
                     Template.ORM.video_box_position_top_px,
                     Template.ORM.video_box_position_left_px)
             .join(EntryStats.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == EntryStats.ORM.entry))
             .join(VideoOptions.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == VideoOptions.ORM.entry))
             .join(Template.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == Template.ORM.entry))
             .objects()])
