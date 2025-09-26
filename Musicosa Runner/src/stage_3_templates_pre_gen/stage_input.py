from peewee import JOIN

from common.model.models import Contestant, Entry, Avatar, EntryStats, Template, VideoOptions
from stage_3_templates_pre_gen.custom_types import Musicosa


def load_avatars_from_db() -> list[Avatar]:
    return [avatar.to_domain() for avatar in Avatar.ORM.select()]


def load_unfulfilled_contestants_from_db() -> list[Contestant]:
    return [contestant.to_domain() for contestant in Contestant.ORM.select().where(Contestant.ORM.avatar.is_null())]


def load_entries_index_of_unfulfilled_templates_from_db() -> dict[int, Entry]:
    return dict(
        [
            (result.orm.ranking_sequence, result.orm.entry.to_domain())
            for result in Entry.ORM.select(EntryStats.ORM.ranking_sequence, EntryStats.ORM.entry)
            .join(EntryStats.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == EntryStats.ORM.entry))
            .join(Template.ORM, join_type=JOIN.LEFT_OUTER, on=(Entry.ORM.id == Template.ORM.entry))
            .where(Template.ORM.entry.is_null())
        ]
    )


def load_entries_index_of_unfulfilled_video_options_from_db() -> dict[int, Entry]:
    return dict(
        [
            (result.orm.ranking_sequence, result.orm.entry.to_domain())
            for result in Entry.ORM.select(EntryStats.ORM.ranking_sequence, EntryStats.ORM.entry)
            .join(EntryStats.ORM, join_type=JOIN.INNER, on=(Entry.ORM.id == EntryStats.ORM.entry))
            .join(VideoOptions.ORM, join_type=JOIN.LEFT_OUTER, on=(Entry.ORM.id == VideoOptions.ORM.entry))
            .where(VideoOptions.ORM.entry.is_null())
        ]
    )


def load_musicosa_from_db() -> Musicosa:
    return Musicosa(
        load_unfulfilled_contestants_from_db(),
        load_avatars_from_db(),
        load_entries_index_of_unfulfilled_templates_from_db(),
        load_entries_index_of_unfulfilled_video_options_from_db(),
    )
