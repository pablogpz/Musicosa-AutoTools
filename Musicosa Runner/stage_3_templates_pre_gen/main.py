from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.model.models import Setting, Template
from common.type_definitions import StageException
from stage_3_templates_pre_gen.execute import execute
from stage_3_templates_pre_gen.stage_input import load_tfa_from_db

if __name__ == "__main__":

    # Data retrieval

    try:
        tfa = load_tfa_from_db()
    except Exception as err:
        print(f"[Stage 3 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(tfa=tfa)
    except StageException as err:
        print(f"[Stage 3 | Execution] {err}")
        exit(1)

    # Data persistence

    try:
        if result.frame_settings:
            with db.atomic():
                Setting.ORM.replace_many(bulk_pack(result.frame_settings)).execute()

        if result.templates:
            with db.atomic():
                Template.ORM.insert_many(bulk_pack(result.templates)).execute()
    except Exception as err:
        print(f"[Stage 3 | Data persistence] {err}")
        exit(1)

    # Execution feedback

    print("")
    print("[STAGE 3 SUMMARY | Templates Pre-Generation]")
    print("")
    print(f"  # Frame settings set: {len(result.frame_settings) if result.frame_settings else 0}")
    print(f"  # Entry templates fulfilled: {len(result.templates) if result.templates else 0}")
