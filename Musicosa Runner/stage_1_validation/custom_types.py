from dataclasses import dataclass

from common.model.models import EntryTopic


@dataclass
class ContestantSubmissionEntry:
    title: str
    score: float
    is_author: bool
    video_url: str | None
    video_timestamp: str | None
    topic: str | None


@dataclass
class ContestantSubmission:
    name: str
    entries: list[ContestantSubmissionEntry]


@dataclass
class StageOneInput:
    submissions: list[ContestantSubmission]
    valid_titles: list[str]
    entry_topics: list[EntryTopic] | None


@dataclass
class StageOneOutput:
    validation_errors: list[str] | None
