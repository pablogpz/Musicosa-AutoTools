from dataclasses import dataclass
from datetime import time
from enum import Enum
from typing import Literal

from peewee import Model, TextField, CompositeKey, AutoField, FloatField, ForeignKeyField, IntegerField

from common.db.database import db
from common.model.settings import parse_setting_value
from common.time.utils import parse_time


@dataclass
class Metadata:
    field: str
    value: str

    class ORM(Model):
        field = TextField(column_name="field", primary_key=True)
        value = TextField(column_name="value")

        class Meta:
            database = db
            table_name = "metadata"

        def to_domain(self) -> "Metadata":
            # noinspection PyTypeChecker
            return Metadata(field=self.field, value=self.value)

    def to_orm(self) -> ORM:
        return Metadata.ORM(field=self.field, value=self.value)


class MetadataFields(Enum):
    EDITION = "edition"


type SettingType = Literal["integer", "real", "string", "boolean"]
type SettingValueType = int | float | str | bool | None


@dataclass
class Setting:
    group_key: str
    setting: str
    type: SettingType
    value: SettingValueType

    class ORM(Model):
        group_key = TextField(column_name="group_key")
        setting = TextField(column_name="setting")
        value = TextField(column_name="value", null=True)
        type = TextField(column_name="type", choices=["integer", "real", "string", "boolean"], default="string")

        class Meta:
            database = db
            table_name = "settings"
            primary_key = CompositeKey("group_key", "setting")

        def to_domain(self) -> "Setting":
            # noinspection PyTypeChecker
            return Setting(group_key=self.group_key, setting=self.setting, type=self.type,
                           value=parse_setting_value(type_str=self.type, value=self.value))

    def to_orm(self) -> ORM:
        return Setting.ORM(group_key=self.group_key, setting=self.setting, type=self.type, value=str(self.value))


class SettingGroupKeys(Enum):
    VALIDATION = "validation"
    RANKING = "ranking"
    FRAME = "frame"


class ValidationSettingNames(Enum):
    SCORE_MIN_VALUE = "score_min_value"
    SCORE_MAX_VALUE = "score_max_value"


class RankingSettingNames(Enum):
    SIGNIFICANT_DECIMAL_DIGITS = "significant_decimal_digits"


class FrameSettingNames(Enum):
    WIDTH_PX = "width_px"
    HEIGHT_PX = "height_px"


type SettingKeys = Literal[
    "validation.score_min_value",
    "validation.score_max_value",
    "ranking.significant_decimal_digits",
    "frame.width_px",
    "frame.height_px",
]


@dataclass
class Avatar:
    id: int
    image_filename: str
    image_height: float
    score_box_position_top: float
    score_box_position_left: float
    score_box_font_scale: float
    score_box_font_color: str | None

    class ORM(Model):
        id = AutoField(primary_key=True)
        image_filename = TextField(column_name="image_filename")
        image_height = FloatField(column_name="image_height")
        score_box_position_top = FloatField(column_name="score_box_position_top")
        score_box_position_left = FloatField(column_name="score_box_position_left")
        score_box_font_scale = FloatField(column_name="score_box_font_scale")
        score_box_font_color = TextField(column_name="score_box_font_color", null=True)

        class Meta:
            database = db
            table_name = "avatars"

        def to_domain(self) -> "Avatar":
            # noinspection PyTypeChecker
            return Avatar(id=self.id,
                          image_filename=self.image_filename,
                          image_height=self.image_height,
                          score_box_position_top=self.score_box_position_top,
                          score_box_position_left=self.score_box_position_left,
                          score_box_font_scale=self.score_box_font_scale,
                          score_box_font_color=self.score_box_font_color)

    def to_orm(self) -> "Avatar.ORM":
        return Avatar.ORM(id=self.id,
                          image_filename=self.image_filename,
                          image_height=self.image_height,
                          score_box_position_top=self.score_box_position_top,
                          score_box_position_left=self.score_box_position_left,
                          score_box_font_scale=self.score_box_font_scale,
                          score_box_font_color=self.score_box_font_color)


@dataclass
class Member:
    id: str
    name: str
    avatar: Avatar | None

    class ORM(Model):
        id = TextField(column_name="id", primary_key=True)
        name = TextField(column_name="name", unique=True)
        avatar = ForeignKeyField(Avatar.ORM, column_name="avatar", null=True)

        class Meta:
            database = db
            table_name = "members"

        def to_domain(self) -> "Member":
            # noinspection PyTypeChecker
            return Member(id=self.id, name=self.name, avatar=self.avatar.to_domain() if self.avatar else None)

    def to_orm(self) -> "Member.ORM":
        return Member.ORM(id=self.id, name=self.name, avatar=self.avatar.to_orm() if self.avatar else None)


@dataclass
class Award:
    slug: str
    designation: str

    class ORM(Model):
        slug = TextField(column_name="slug", primary_key=True)
        designation = TextField(column_name="designation")

        class Meta:
            database = db
            table_name = "awards"

        def to_domain(self) -> "Award":
            # noinspection PyTypeChecker
            return Award(slug=self.slug, designation=self.designation)

    def to_orm(self) -> "Award.ORM":
        return Award.ORM(slug=self.slug, designation=self.designation)


@dataclass
class Nomination:
    id: str
    game_title: str
    nominee: str | None
    award: Award

    class ORM(Model):
        id = TextField(column_name="id", primary_key=True)
        game_title = TextField(column_name="game_title")
        nominee = TextField(column_name="nominee", null=True)
        award = ForeignKeyField(Award.ORM, column_name="award")

        class Meta:
            database = db
            table_name = "nominations"

        def to_domain(self) -> "Nomination":
            # noinspection PyTypeChecker
            return Nomination(id=self.id,
                              game_title=self.game_title,
                              nominee=self.nominee,
                              award=self.award.to_domain())

    def to_orm(self) -> "Nomination.ORM":
        return Nomination.ORM(id=self.id,
                              game_title=self.game_title,
                              nominee=self.nominee,
                              award=self.award.to_orm())


@dataclass
class Template:
    nomination: Nomination
    avatar_scale: float
    video_box_width_px: int
    video_box_height_px: int
    video_box_position_top_px: int
    video_box_position_left_px: int

    class ORM(Model):
        nomination = ForeignKeyField(Nomination.ORM, column_name="nomination", primary_key=True)
        avatar_scale = FloatField(column_name="avatar_scale", default=1.0)
        video_box_width_px = IntegerField(column_name="video_box_width_px")
        video_box_height_px = IntegerField(column_name="video_box_height_px")
        video_box_position_top_px = IntegerField(column_name="video_box_position_top_px")
        video_box_position_left_px = IntegerField(column_name="video_box_position_left_px")

        class Meta:
            database = db
            table_name = "templates"

        def to_domain(self) -> "Template":
            # noinspection PyTypeChecker
            return Template(nomination=self.nomination.to_domain(),
                            avatar_scale=self.avatar_scale,
                            video_box_width_px=self.video_box_width_px,
                            video_box_height_px=self.video_box_height_px,
                            video_box_position_top_px=self.video_box_position_top_px,
                            video_box_position_left_px=self.video_box_position_left_px)

    def to_orm(self) -> "Template.ORM":
        return Template.ORM(nomination=self.nomination.to_orm(),
                            avatar_scale=self.avatar_scale,
                            video_box_width_px=self.video_box_width_px,
                            video_box_height_px=self.video_box_height_px,
                            video_box_position_top_px=self.video_box_position_top_px,
                            video_box_position_left_px=self.video_box_position_left_px)


@dataclass
class Videoclip:
    id: int
    url: str

    class ORM(Model):
        id = IntegerField(column_name="id", primary_key=True)
        url = TextField(column_name="url")

        class Meta:
            database = db
            table_name = "videoclips"

        def to_domain(self) -> "Videoclip":
            # noinspection PyTypeChecker
            return Videoclip(id=self.id, url=self.url)

    def to_orm(self) -> "Videoclip.ORM":
        return Videoclip.ORM(id=self.id, url=self.url)


@dataclass
class VideoOptions:
    nomination: Nomination
    videoclip: Videoclip
    timestamp_start: time
    timestamp_end: time

    class ORM(Model):
        nomination = ForeignKeyField(Nomination.ORM, column_name="nomination", primary_key=True)
        videoclip = ForeignKeyField(Videoclip.ORM, column_name="videoclip")
        timestamp_start = TextField(column_name="timestamp_start")
        timestamp_end = TextField(column_name="timestamp_end")

        class Meta:
            database = db
            table_name = "video_options"

        def to_domain(self) -> "VideoOptions":
            # noinspection PyTypeChecker
            return VideoOptions(nomination=self.nomination.to_domain(),
                                videoclip=self.videoclip.to_domain(),
                                timestamp_start=parse_time(self.timestamp_start),
                                timestamp_end=parse_time(self.timestamp_end))

    def to_orm(self) -> "VideoOptions.ORM":
        return VideoOptions.ORM(nomination=self.nomination.to_orm(),
                                videoclip=self.videoclip.to_orm(),
                                timestamp_start=str(self.timestamp_start),
                                timestamp_end=str(self.timestamp_end))


@dataclass
class CastVote:
    member: Member | None
    nomination: Nomination
    score: float

    class ORM(Model):
        member = ForeignKeyField(Member.ORM, column_name="member", null=True)
        nomination = ForeignKeyField(Nomination.ORM, column_name="nomination")
        score = FloatField(column_name="score")

        class Meta:
            database = db
            table_name = "member_grades_nominations"
            primary_key = CompositeKey("member", "nomination")

        def to_domain(self) -> "CastVote":
            # noinspection PyTypeChecker
            return CastVote(member=self.member.to_domain() if self.member else None,
                            nomination=self.nomination.to_domain(),
                            score=self.score)

    def to_orm(self) -> "CastVote.ORM":
        return CastVote.ORM(member=self.member.to_orm() if self.member else None,
                            nomination=self.nomination.to_orm(),
                            score=self.score)


@dataclass
class NominationStats:
    nomination: Nomination
    avg_score: float | None
    ranking_place: int | None
    ranking_sequence: int | None

    class ORM(Model):
        nomination = ForeignKeyField(Nomination.ORM, column_name="nomination", primary_key=True)
        avg_score = FloatField(column_name="avg_score", null=True)
        ranking_place = IntegerField(column_name="ranking_place", null=True)
        ranking_sequence = IntegerField(column_name="ranking_sequence", unique=True, null=True)

        class Meta:
            database = db
            table_name = "stats_nominations"

        def to_domain(self) -> "NominationStats":
            # noinspection PyTypeChecker
            return NominationStats(nomination=self.nomination.to_domain(), avg_score=self.avg_score,
                                   ranking_place=self.ranking_place,
                                   ranking_sequence=self.ranking_sequence)

    def to_orm(self) -> "NominationStats.ORM":
        return NominationStats.ORM(nomination=self.nomination.to_orm(), avg_score=self.avg_score,
                                   ranking_place=self.ranking_place,
                                   ranking_sequence=self.ranking_sequence)
