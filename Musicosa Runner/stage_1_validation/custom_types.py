from dataclasses import dataclass

from common.model.models import SpecialEntryTopic


@dataclass
class ContestantSubmissionEntry:
    title: str
    score: float
    is_author: bool
    video_url: str | None
    video_timestamp: str | None
    special_topic: str | None


@dataclass
class ContestantSubmission:
    name: str
    entries: list[ContestantSubmissionEntry]


@dataclass
class StageOneInput:
    submissions: list[ContestantSubmission]
    valid_titles: list[str]
    special_entry_topics: list[SpecialEntryTopic] | None


@dataclass
class StageOneOutput:
    validation_errors: list[str] | None
