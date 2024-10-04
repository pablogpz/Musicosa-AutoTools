from dataclasses import dataclass


@dataclass
class Score:
    entry_title: str
    score_value: float


@dataclass
class Entry:
    title: str
    author_name: str


@dataclass
class Contestant:
    contestant_name: str
    scores: list[Score]


@dataclass
class Musicosa:
    contestants: list[Contestant]
    entries: list[Entry]


@dataclass
class ContestantStats:
    contestant: Contestant
    avg_score: float | None


@dataclass
class EntryStats:
    entry: Entry
    avg_score: float | None
    ranking_place: int | None
    ranking_sequence: int | None


@dataclass
class StageTwoInput:
    musicosa: Musicosa


@dataclass
class StageTwoOutput:
    contestants_stats: list[ContestantStats]
    entries_stats: list[EntryStats]
