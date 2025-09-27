from dataclasses import dataclass


@dataclass
class Nomination:
    id: str
    votes: list[float]


@dataclass
class Award:
    slug: str
    nominations: list[Nomination]


@dataclass
class TFA:
    awards: list[Award]


@dataclass
class StageTwoInput:
    tfa: TFA


@dataclass
class NominationStats:
    nomination_id: str
    avg_score: float
    ranking_place: int
    ranking_sequence: int


@dataclass
class StageTwoOutput:
    nomination_stats: list[NominationStats]
