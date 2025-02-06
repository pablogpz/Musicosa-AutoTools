from common.db.database import db
from common.model.models import NominationStats
from common.type_definitions import StageException
from stage_2_sub_processing.execute import execute
from stage_2_sub_processing.stage_input import load_tfa_from_db

if __name__ == "__main__":

    # Data retrieval

    try:
        tfa = load_tfa_from_db()
    except Exception as err:
        print(f"[Stage 2 | Data retrieval] {err}")
        exit(1)

    # Stage execution

    try:
        result = execute(tfa=tfa)
    except StageException as err:
        print(f"[Stage 2 | Execution] {err}")
        exit(1)

    # Data persistence

    raw_nominations_stats: list[NominationStats.ORM] = []
    for stat in result.nomination_stats:
        raw_nominations_stats.append(
            NominationStats.ORM(nomination=stat.nomination_id,
                                avg_score=stat.avg_score,
                                ranking_place=stat.ranking_place,
                                ranking_sequence=stat.ranking_sequence))

    try:
        with db.atomic():
            NominationStats.ORM.insert_many([stat.__data__ for stat in raw_nominations_stats]).execute()  # CAREFUL !
    except Exception as err:
        print(f"[Stage 2 | Data persistence] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 2 SUMMARY | Awards Processing]")
    print(f"  # Awards loaded: {len(tfa.awards)}")
    print("")
    print(f"  # Ranked nominations: {len(result.nomination_stats)}")
