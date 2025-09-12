from peewee import JOIN

from common.model.models import Nomination, NominationStats, VideoOptions, Template
from model.models import Videoclip
from stage_6_video_gen.types import NominationVideoOptions, Timestamp


def load_video_options_from_db() -> list[NominationVideoOptions]:
    return ([NominationVideoOptions(award=row.award,
                                    template_friendly_name=f"{row.award}"
                                                           f"-{row.game_title}"
                                                           f"{f"-{row.nominee}" if row.nominee else ''}",
                                    sequence_number=row.ranking_sequence,
                                    videoclip_friendly_name=row.url,
                                    timestamp=Timestamp(start=row.timestamp_start, end=row.timestamp_end),
                                    width=row.video_box_width_px,
                                    height=row.video_box_height_px,
                                    position_top=row.video_box_position_top_px,
                                    position_left=row.video_box_position_left_px)
             for row in
             Nomination.ORM
             .select(Nomination.ORM.game_title,
                     Nomination.ORM.nominee,
                     Nomination.ORM.award,
                     NominationStats.ORM.ranking_sequence,
                     VideoOptions.ORM.timestamp_start,
                     VideoOptions.ORM.timestamp_end,
                     Videoclip.ORM.url,
                     Template.ORM.video_box_width_px,
                     Template.ORM.video_box_height_px,
                     Template.ORM.video_box_position_top_px,
                     Template.ORM.video_box_position_left_px)
             .join(NominationStats.ORM, join_type=JOIN.INNER, on=(Nomination.ORM.id == NominationStats.ORM.nomination))
             .join(Template.ORM, join_type=JOIN.INNER, on=(Nomination.ORM.id == Template.ORM.nomination))
             .join(VideoOptions.ORM, join_type=JOIN.INNER, on=(Nomination.ORM.id == VideoOptions.ORM.nomination))
             .join(Videoclip.ORM, join_type=JOIN.INNER, on=(VideoOptions.ORM.videoclip == Videoclip.ORM.id))
             .objects()])
