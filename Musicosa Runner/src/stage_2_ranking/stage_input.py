from common.model.models import Award, CastVote, Nomination
from stage_2_ranking.custom_types import TFA
from stage_2_ranking.custom_types import Award as S2_Award
from stage_2_ranking.custom_types import Nomination as S2_Nomination


def load_tfa_from_db() -> TFA:
    awards: list[Award] = [r.to_domain() for r in Award.ORM.select()]
    s2_awards: list[S2_Award] = []

    for award in awards:
        nominations: list[Nomination] = [
            r.to_domain() for r in Nomination.ORM.select().where(Nomination.ORM.award == award.slug)
        ]
        s2_nominations: list[S2_Nomination] = []

        for nomination in nominations:
            votes: list[CastVote] = [
                r.to_domain() for r in CastVote.ORM.select().where(CastVote.ORM.nomination == nomination.id)
            ]
            s2_nominations.append(S2_Nomination(nomination.id, [vote.score for vote in votes]))

        s2_awards.append(S2_Award(award.slug, s2_nominations))

    return TFA(s2_awards)
