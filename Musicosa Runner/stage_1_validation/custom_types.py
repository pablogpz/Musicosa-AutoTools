from dataclasses import dataclass


@dataclass
class CastVote:
    nomination: str
    score: float


@dataclass
class MemberSubmission:
    name: str
    cast_votes: list[CastVote]


@dataclass
class AwardForm:
    award_slug: str
    submissions: list[MemberSubmission]


@dataclass
class StageOneInput:
    award_forms: list[AwardForm]
    valid_award_slugs: list[str]
    award_count: int
    member_count: int


@dataclass
class StageOneOutput:
    validation_errors: list[str]
