from common.model.models import Contestant, Scoring, Entry
from stage_2_ranking.custom_types import Musicosa, Contestant as S2_Contestant, Score as S2_Score, Entry as S2_Entry


def load_musicosa_from_db() -> Musicosa:
    contestants: list[Contestant] = [contestant.to_domain() for contestant in Contestant.ORM.select()]
    s2_contestants: list[S2_Contestant] = []

    for contestant in contestants:
        scoring_entries: list[Scoring] = [
            scoring.to_domain() for scoring in Scoring.ORM.select().where(Scoring.ORM.contestant == contestant.id)
        ]
        s2_scores: list[S2_Score] = [S2_Score(scoring.entry.title, scoring.score) for scoring in scoring_entries]

        s2_contestants.append(S2_Contestant(contestant.name, s2_scores))

    entries: list[Entry] = [entry.to_domain() for entry in Entry.ORM.select()]
    s2_entries: list[S2_Entry] = [S2_Entry(entry.title, entry.author.name if entry.author else "") for entry in entries]

    return Musicosa(s2_contestants, s2_entries)
