from dataclasses import dataclass
from datetime import time
from enum import Enum
from typing import Literal

from peewee import Model, TextField, CompositeKey, AutoField, FloatField, ForeignKeyField, IntegerField

from common.db.database import db
from common.time_utils import parse_time


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
    TOPIC = "topic"
    ORGANISER = "organiser"
    START_DATE = "start_date"


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
        type = TextField(column_name="type", choices=["integer", "real", "string", "boolean"])

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
    class Insert:
        image_filename: str
        image_height: float
        score_box_position_top: float
        score_box_position_left: float
        score_box_font_scale: float
        score_box_font_color: str | None

        def to_orm(self) -> "Avatar.ORM":
            return Avatar.ORM(image_filename=self.image_filename,
                              image_height=self.image_height,
                              score_box_position_top=self.score_box_position_top,
                              score_box_position_left=self.score_box_position_left,
                              score_box_font_scale=self.score_box_font_scale,
                              score_box_font_color=self.score_box_font_color)


@dataclass
class Contestant:
    id: str
    name: str
    avatar: Avatar | None

    class ORM(Model):
        id = TextField(column_name="id", primary_key=True)
        name = TextField(column_name="name", unique=True)
        avatar = ForeignKeyField(Avatar.ORM, column_name="avatar", null=True)

        class Meta:
            database = db
            table_name = "contestants"

        def to_domain(self) -> "Contestant":
            # noinspection PyTypeChecker
            return Contestant(id=self.id, name=self.name, avatar=self.avatar.to_domain() if self.avatar else None)

    def to_orm(self) -> "Contestant.ORM":
        return Contestant.ORM(id=self.id, name=self.name, avatar=self.avatar.to_orm() if self.avatar else None)


@dataclass
class SpecialEntryTopic:
    designation: str

    class ORM(Model):
        designation = TextField(column_name="designation", primary_key=True)

        class Meta:
            database = db
            table_name = "special_entry_topics"

        def to_domain(self) -> "SpecialEntryTopic":
            # noinspection PyTypeChecker
            return SpecialEntryTopic(designation=self.designation)

    def to_orm(self) -> "SpecialEntryTopic.ORM":
        return SpecialEntryTopic.ORM(designation=self.designation)


@dataclass
class Entry:
    id: str
    title: str
    author: Contestant | None
    video_url: str | None
    special_topic: SpecialEntryTopic | None

    class ORM(Model):
        id = TextField(column_name="id", primary_key=True)
        title = TextField(column_name="title", unique=True)
        author = ForeignKeyField(Contestant.ORM, column_name="author", null=True)
        video_url = TextField(column_name="video_url", null=True)
        special_topic = ForeignKeyField(SpecialEntryTopic.ORM, column_name="special_topic", null=True)

        class Meta:
            database = db
            table_name = "entries"

        @dataclass
        class Create:
            title: str
            author: str
            video_url: str

        def to_domain(self) -> "Entry":
            # noinspection PyTypeChecker
            return Entry(id=self.id,
                         title=self.title,
                         author=self.author.to_domain() if self.author else None,
                         video_url=self.video_url,
                         special_topic=self.special_topic.to_domain() if self.special_topic else None)

    def to_orm(self) -> "Entry.ORM":
        return Entry.ORM(id=self.id,
                         title=self.title,
                         author=self.author.to_orm() if self.author else None,
                         video_url=self.video_url,
                         special_topic=self.special_topic.to_orm() if self.special_topic else None)


@dataclass
class Template:
    entry: Entry
    avatar_scale: float
    author_avatar_scale: float
    video_box_width_px: int
    video_box_height_px: int
    video_box_position_top_px: int
    video_box_position_left_px: int

    class ORM(Model):
        entry = ForeignKeyField(Entry.ORM, column_name="entry", primary_key=True)
        avatar_scale = FloatField(column_name="avatar_scale", default=1.0)
        author_avatar_scale = FloatField(column_name="author_avatar_scale", default=1.0)
        video_box_width_px = IntegerField(column_name="video_box_width_px")
        video_box_height_px = IntegerField(column_name="video_box_height_px")
        video_box_position_top_px = IntegerField(column_name="video_box_position_top_px")
        video_box_position_left_px = IntegerField(column_name="video_box_position_left_px")

        class Meta:
            database = db
            table_name = "templates"

        def to_domain(self) -> "Template":
            # noinspection PyTypeChecker
            return Template(entry=self.entry.to_domain(),
                            avatar_scale=self.avatar_scale,
                            author_avatar_scale=self.author_avatar_scale,
                            video_box_width_px=self.video_box_width_px,
                            video_box_height_px=self.video_box_height_px,
                            video_box_position_top_px=self.video_box_position_top_px,
                            video_box_position_left_px=self.video_box_position_left_px)

    def to_orm(self) -> "Template.ORM":
        return Template.ORM(entry=self.entry.to_orm(),
                            avatar_scale=self.avatar_scale,
                            author_avatar_scale=self.author_avatar_scale,
                            video_box_width_px=self.video_box_width_px,
                            video_box_height_px=self.video_box_height_px,
                            video_box_position_top_px=self.video_box_position_top_px,
                            video_box_position_left_px=self.video_box_position_left_px)


@dataclass
class VideoOptions:
    entry: Entry
    timestamp_start: time | None
    timestamp_end: time | None

    class ORM(Model):
        entry = ForeignKeyField(Entry.ORM, column_name="entry", primary_key=True)
        timestamp_start = TextField(column_name="timestamp_start", null=True)
        timestamp_end = TextField(column_name="timestamp_end", null=True)

        class Meta:
            database = db
            table_name = "video_options"

        def to_domain(self) -> "VideoOptions":
            # noinspection PyTypeChecker
            return VideoOptions(entry=self.entry.to_domain(),
                                timestamp_start=parse_time(self.timestamp_start),
                                timestamp_end=parse_time(self.timestamp_end))

    def to_orm(self) -> "VideoOptions.ORM":
        return VideoOptions.ORM(entry=self.entry.to_orm(),
                                timestamp_start=str(self.timestamp_start),
                                timestamp_end=str(self.timestamp_end))


@dataclass
class Scoring:
    contestant: Contestant
    entry: Entry
    score: float

    class ORM(Model):
        contestant = ForeignKeyField(Contestant.ORM, column_name="contestant", null=True)
        entry = ForeignKeyField(Entry.ORM, column_name="entry")
        score = FloatField(column_name="score")

        class Meta:
            database = db
            table_name = "contestant_grades_entries"
            primary_key = CompositeKey("contestant", "entry")

        def to_domain(self) -> "Scoring":
            # noinspection PyTypeChecker
            return Scoring(contestant=self.contestant.to_domain(),
                           entry=self.entry.to_domain(),
                           score=self.score)

    def to_orm(self) -> "Scoring.ORM":
        return Scoring.ORM(contestant=self.contestant.to_orm(),
                           entry=self.entry.to_orm(),
                           score=self.score)


@dataclass
class ContestantStats:
    contestant: Contestant
    avg_score: float | None

    class ORM(Model):
        contestant = ForeignKeyField(Contestant.ORM, column_name="contestant", primary_key=True)
        avg_score = FloatField(column_name="avg_score", null=True)

        class Meta:
            database = db
            table_name = "stats_contestants"

        def to_domain(self) -> "ContestantStats":
            # noinspection PyTypeChecker
            return ContestantStats(contestant=self.contestant.to_domain(), avg_score=self.avg_score)

    def to_orm(self) -> "ContestantStats.ORM":
        return ContestantStats.ORM(contestant=self.contestant.to_orm(), avg_score=self.avg_score)


@dataclass
class EntryStats:
    entry: Entry
    avg_score: float | None
    ranking_place: int | None
    ranking_sequence: int | None

    class ORM(Model):
        entry = ForeignKeyField(Entry.ORM, column_name="entry", primary_key=True)
        avg_score = FloatField(column_name="avg_score", null=True)
        ranking_place = IntegerField(column_name="ranking_place", null=True)
        ranking_sequence = IntegerField(column_name="ranking_sequence", unique=True, null=True)

        class Meta:
            database = db
            table_name = "stats_entries"

        def to_domain(self) -> "EntryStats":
            # noinspection PyTypeChecker
            return EntryStats(entry=self.entry.to_domain(), avg_score=self.avg_score, ranking_place=self.ranking_place,
                              ranking_sequence=self.ranking_sequence)

    def to_orm(self) -> "EntryStats.ORM":
        return EntryStats.ORM(entry=self.entry.to_orm(), avg_score=self.avg_score, ranking_place=self.ranking_place,
                              ranking_sequence=self.ranking_sequence)


@dataclass
class EntryExtraInfo:
    entry: Entry
    saga: str

    class ORM(Model):
        entry = ForeignKeyField(Entry.ORM, column_name="entry", primary_key=True)
        saga = TextField(column_name="saga", null=False)

        class Meta:
            database = db
            table_name = "entries_extra_info"

        def to_domain(self) -> "EntryExtraInfo":
            # noinspection PyTypeChecker
            return EntryExtraInfo(entry=self.entry.to_domain(), saga=self.saga)

    def to_orm(self) -> "EntryExtraInfo.ORM":
        return EntryExtraInfo.ORM(entry=self.entry.to_orm(), saga=self.saga)


# MODEL PARSERS

def parse_setting_value(type_str: SettingType, value: str) -> SettingValueType:
    if not value or not value.strip():
        parsed_value = None
    elif type_str == "integer":
        parsed_value = int(value)
    elif type_str == "real":
        parsed_value = float(value)
    elif type_str == "boolean":
        parsed_value = value.lower() == "true"
    else:
        parsed_value = value

    return parsed_value
