from dataclasses import dataclass
from datetime import time
from enum import StrEnum
from typing import Literal, Any

from peewee import Model as PeeweeModel, TextField, CompositeKey, AutoField, FloatField, ForeignKeyField, IntegerField

from common.db.database import db
from common.time.utils import parse_time


class DomainModel:
    def to_orm(self) -> Any:
        pass


class DatabaseModel:
    def to_domain(self) -> Any:
        pass


class MetadataFields(StrEnum):
    EDITION = "edition"


type MetadataField = Literal["edition"]


@dataclass
class Metadata(DomainModel):
    field: MetadataField
    value: str

    class ORM(PeeweeModel, DatabaseModel):
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


class SettingValueTypes(StrEnum):
    INTEGER = "integer"
    REAL = "real"
    STRING = "string"
    BOOLEAN = "boolean"


type SettingValueType = Literal["integer", "real", "string", "boolean"]
type SettingValueTypeSpec = int | float | str | bool | None


class SettingGroupKeys(StrEnum):
    VALIDATION = "validation"
    RANKING = "ranking"
    FRAME = "frame"


class ValidationSettingNames(StrEnum):
    SCORE_MIN_VALUE = "score_min_value"
    SCORE_MAX_VALUE = "score_max_value"


class RankingSettingNames(StrEnum):
    SIGNIFICANT_DECIMAL_DIGITS = "significant_decimal_digits"


class FrameSettingNames(StrEnum):
    WIDTH_PX = "width_px"
    HEIGHT_PX = "height_px"


SETTING_KEY_SEPARATOR = "."


class SettingKeys(StrEnum):
    VALIDATION_SCORE_MIN_VALUE = \
        f"{SettingGroupKeys.VALIDATION}{SETTING_KEY_SEPARATOR}{ValidationSettingNames.SCORE_MIN_VALUE}"
    VALIDATION_SCORE_MAX_VALUE = \
        f"{SettingGroupKeys.VALIDATION}{SETTING_KEY_SEPARATOR}{ValidationSettingNames.SCORE_MAX_VALUE}"
    RANKING_SIGNIFICANT_DECIMAL_DIGITS = \
        f"{SettingGroupKeys.RANKING}{SETTING_KEY_SEPARATOR}{RankingSettingNames.SIGNIFICANT_DECIMAL_DIGITS}"
    FRAME_WIDTH_PX = \
        f"{SettingGroupKeys.FRAME}{SETTING_KEY_SEPARATOR}{FrameSettingNames.WIDTH_PX}"
    FRAME_HEIGHT_PX = \
        f"{SettingGroupKeys.FRAME}{SETTING_KEY_SEPARATOR}{FrameSettingNames.HEIGHT_PX}"


@dataclass
class Setting(DomainModel):
    group_key: str
    setting: str
    type: SettingValueType
    value: SettingValueTypeSpec

    class ORM(PeeweeModel, DatabaseModel):
        group_key = TextField(column_name="group_key")
        setting = TextField(column_name="setting")
        value = TextField(column_name="value", null=True)
        type = TextField(column_name="type", choices=[t.value for t in SettingValueTypes],
                         default=SettingValueTypes.STRING)

        class Meta:
            database = db
            table_name = "settings"
            primary_key = CompositeKey("group_key", "setting")

        def to_domain(self) -> "Setting":
            # noinspection PyTypeChecker
            return Setting(group_key=self.group_key, setting=self.setting, type=self.type,
                           value=Setting.parse_setting_value(value=self.value, type_str=self.type))

    @staticmethod
    def parse_setting_value(value: str, type_str: SettingValueTypes) -> SettingValueTypeSpec:
        if not value or not value.strip():
            parsed_value = None
        elif type_str == SettingValueTypes.INTEGER:
            parsed_value = int(value)
        elif type_str == SettingValueTypes.REAL:
            parsed_value = float(value)
        elif type_str == SettingValueTypes.BOOLEAN:
            parsed_value = value.lower() == "true"
        else:
            parsed_value = value

        return parsed_value

    def to_orm(self) -> ORM:
        return Setting.ORM(group_key=self.group_key, setting=self.setting, type=self.type, value=str(self.value))


@dataclass
class Avatar(DomainModel):
    id: int
    image_filename: str
    image_height: float
    score_box_position_top: float
    score_box_position_left: float
    score_box_font_scale: float
    score_box_font_color: str | None

    class ORM(PeeweeModel, DatabaseModel):
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
class Member(DomainModel):
    id: str
    name: str
    avatar: Avatar | None

    class ORM(PeeweeModel, DatabaseModel):
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
class Award(DomainModel):
    slug: str
    designation: str

    class ORM(PeeweeModel, DatabaseModel):
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
class Nomination(DomainModel):
    id: str
    game_title: str
    nominee: str | None
    award: Award

    class ORM(PeeweeModel, DatabaseModel):
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
class Template(DomainModel):
    nomination: Nomination
    avatar_scale: float
    video_box_width_px: int
    video_box_height_px: int
    video_box_position_top_px: int
    video_box_position_left_px: int

    class ORM(PeeweeModel, DatabaseModel):
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
class Videoclip(DomainModel):
    id: int
    url: str

    class ORM(PeeweeModel, DatabaseModel):
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
class VideoOptions(DomainModel):
    nomination: Nomination
    videoclip: Videoclip
    timestamp_start: time
    timestamp_end: time

    class ORM(PeeweeModel, DatabaseModel):
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
class CastVote(DomainModel):
    member: Member | None
    nomination: Nomination
    score: float

    class ORM(PeeweeModel, DatabaseModel):
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
class NominationStats(DomainModel):
    nomination: Nomination
    avg_score: float | None
    ranking_place: int | None
    ranking_sequence: int | None

    class ORM(PeeweeModel, DatabaseModel):
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
