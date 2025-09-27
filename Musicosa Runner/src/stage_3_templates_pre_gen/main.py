from common.custom_types import StageException
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.model.models import Setting, Template
from stage_3_templates_pre_gen.custom_types import StageThreeInput
from stage_3_templates_pre_gen.execute import execute
from stage_3_templates_pre_gen.stage_input import load_tfa_from_db
from stage_3_templates_pre_gen.summary import stage_summary

if __name__ == "__main__":

    # Data retrieval

    try:
        tfa = load_tfa_from_db()
    except Exception as err:
        print(f"[Stage 3 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(StageThreeInput(tfa))
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

    # Stage execution summary

    print(stage_summary(result))
