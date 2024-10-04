from common.models import Contestant, Scoring, Entry
from stage_2_sub_processing.type_definitions import Musicosa, Contestant as S2Contestant, Score as S2Score, \
    Entry as S2Entry


def load_musicosa_from_db() -> Musicosa:
    contestants: list[Contestant] = [contestant.to_domain() for contestant in Contestant.ORM.select()]
    s2_contestants: list[S2Contestant] = []

    for contestant in contestants:
        scoring_entries: list[Scoring] = [scoring.to_domain() for scoring in
                                          Scoring.ORM.select().where(Scoring.ORM.contestant == contestant.id)]
        s2_scores: list[S2Score] = [S2Score(entry_title=scoring.entry.title, score_value=scoring.score)
                                    for scoring in scoring_entries]

        s2_contestants.append(S2Contestant(contestant_name=contestant.name, scores=s2_scores))

    entries: list[Entry] = [entry.to_domain() for entry in Entry.ORM.select()]
    s2_entries: list[S2Entry] = [S2Entry(title=entry.title, author_name=entry.author.name) for entry in entries]

    return Musicosa(contestants=s2_contestants, entries=s2_entries)
