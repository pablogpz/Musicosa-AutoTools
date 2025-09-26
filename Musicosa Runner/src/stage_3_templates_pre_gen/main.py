from common.custom_types import StageException
from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.model.models import Avatar, Contestant, Setting, Template, VideoOptions
from stage_3_templates_pre_gen.custom_types import StageThreeInput
from stage_3_templates_pre_gen.execute import execute
from stage_3_templates_pre_gen.stage_input import load_musicosa_from_db
from stage_3_templates_pre_gen.summary import stage_summary

if __name__ == "__main__":
    # Data retrieval

    try:
        musicosa = load_musicosa_from_db()
    except Exception as err:
        print(f"[Stage 3 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(StageThreeInput(musicosa))
    except StageException as err:
        print(f"[Stage 3 | Execution] {err}")
        exit(1)

    # Data persistence

    try:
        if result.avatar_pairings:
            with db.atomic():
                for pairing in result.avatar_pairings:
                    if isinstance(pairing.avatar, Avatar.Insert):
                        paired_avatar_entity = Avatar.ORM.create(**(vars(pairing.avatar)))
                    else:
                        paired_avatar_entity = pairing.avatar.to_orm()

                    (
                        Contestant.ORM.update(avatar=paired_avatar_entity)
                        .where(Contestant.ORM.id == pairing.contestant.id)
                        .execute()
                    )

        if result.frame_settings:
            with db.atomic():
                Setting.ORM.replace_many(bulk_pack(result.frame_settings)).execute()

        if result.templates:
            with db.atomic():
                Template.ORM.insert_many(bulk_pack(result.templates)).execute()

        if result.generation_settings:
            with db.atomic():
                Setting.ORM.replace_many(bulk_pack(result.generation_settings)).execute()

        if result.video_options:
            with db.atomic():
                VideoOptions.ORM.insert_many(bulk_pack(result.video_options)).execute()
    except Exception as err:
        print(f"[Stage 3 | Data persistence] {err}")
        exit(1)

    # Stage execution summary

    print(stage_summary(result))
