from common.custom_types import StageException
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.model.models import Contestant, Entry, ContestantStats, EntryStats
from stage_2_ranking.execute import execute
from stage_2_ranking.stage_input import load_musicosa_from_db

if __name__ == "__main__":

    # Data retrieval

    try:
        musicosa = load_musicosa_from_db()
    except Exception as err:
        print(f"[Stage 2 | Data retrieval] {err}")
        exit(1)

    # Stage execution

    try:
        result = execute(musicosa=musicosa)
    except StageException as err:
        print(f"[Stage 2 | Execution] {err}")
        exit(1)

    # Data persistence

    contestants_stats = result.contestants_stats
    entries_stats = result.entries_stats

    contestants = [contestant.to_domain() for contestant in Contestant.ORM.select()]
    contestants_by_name = dict([(contestant.name, contestant) for contestant in contestants])

    entries = [entry.to_domain() for entry in Entry.ORM.select()]
    entries_by_title = dict([(entry.title, entry) for entry in entries])

    try:
        with db.atomic():
            (ContestantStats.ORM
             .insert_many(bulk_pack(
                [ContestantStats(contestant=contestants_by_name[stat.contestant.contestant_name],
                                 avg_given_score=stat.avg_given_score,
                                 avg_received_score=stat.avg_received_score)
                 for stat in contestants_stats]))
             .execute())

            (EntryStats.ORM
             .insert_many(bulk_pack(
                [EntryStats(entry=entries_by_title[stat.entry.title],
                            avg_score=stat.avg_score,
                            ranking_place=stat.ranking_place,
                            ranking_sequence=stat.ranking_sequence)
                 for stat in entries_stats]))
             .execute())
    except Exception as err:
        print(f"[Stage 2 | Data persistence] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 2 SUMMARY | Musicosa Ranking]")
    print(f"  # Contestants loaded: {len(musicosa.contestants)}")
    print(f"  # Entries loaded: {len(musicosa.entries)}")
    print("")
    contestant_stats_display = [(stat.contestant.contestant_name, stat.avg_given_score, stat.avg_received_score) for
                                stat in
                                contestants_stats]
    print(f"  Contestant stats (name, avg_given_score, avg_received_score): {contestant_stats_display}")
    print(f"  # Ranked entries: {len(entries_stats)}")
