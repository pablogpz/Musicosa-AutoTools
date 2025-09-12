from dataclasses import dataclass

from common.model.models import Contestant, Avatar, Template, Setting, Entry, VideoOptions


@dataclass
class AvatarPairing:
    contestant: Contestant
    avatar: Avatar | Avatar.Insert


@dataclass
class Musicosa:
    unfulfilled_contestants: list[Contestant]
    available_avatars: list[Avatar]
    entries_index_of_unfulfilled_templates: dict[int, Entry]
    entries_index_of_unfulfilled_video_options: dict[int, Entry]


@dataclass
class StageThreeInput:
    musicosa: Musicosa


@dataclass
class StageThreeOutput:
    avatar_pairings: list[AvatarPairing] | None
    frame_settings: list[Setting] | None
    templates: list[Template] | None
    generation_settings: list[Setting] | None
    video_options: list[VideoOptions] | None
