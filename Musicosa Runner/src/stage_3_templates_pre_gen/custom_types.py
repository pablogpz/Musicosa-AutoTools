from dataclasses import dataclass

from common.model.models import Avatar, Contestant, Entry, Setting, Template, VideoOptions


@dataclass
class AvatarPairing:
    contestant: Contestant
    avatar: Avatar | Avatar.Insert


@dataclass
class Musicosa:
    unfulfilled_contestants: list[Contestant]
    avatars: list[Avatar]
    entries_index_unfulfilled_templates: dict[int, Entry]
    entries_index_unfulfilled_video_options: dict[int, Entry]


@dataclass
class StageThreeInput:
    musicosa: Musicosa


@dataclass
class StageThreeOutput:
    avatar_pairings: list[AvatarPairing]
    frame_settings: list[Setting]
    templates: list[Template]
    generation_settings: list[Setting]
    video_options: list[VideoOptions]
