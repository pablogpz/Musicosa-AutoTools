from common.db.database import db
from common.db.peewee_helpers import bulk_pack
from common.models import Avatar, Contestant, Setting, Template, VideoOptions
from common.type_definitions import StageException
from stage_3_pre_templates_gen.execute import execute
from stage_3_pre_templates_gen.stage_input import load_musicosa_from_db

if __name__ == "__main__":

    # Data retrieval

    try:
        musicosa = load_musicosa_from_db()
    except Exception as err:
        print(f"[Stage 3 | Data retrieval] {err}")
        exit(1)

    # Execution

    try:
        result = execute(musicosa=musicosa)
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

                    (Contestant.ORM
                     .update(avatar=paired_avatar_entity)
                     .where(Contestant.ORM.id == pairing.contestant.id)
                     .execute())

        if result.templates_settings:
            with db.atomic():
                Setting.ORM.replace_many(bulk_pack(result.templates_settings)).execute()

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

    # Execution feedback

    print("")
    print("[STAGE 3 SUMMARY | Pre-templates Generation]")
    print("")
    print(f"  # Paired contestants to avatars: {len(result.avatar_pairings) if result.avatar_pairings else 0}")
    print(f"  # Templates general settings set: {len(result.templates_settings) if result.templates_settings else 0}")
    print(f"  # Entry templates fulfilled: {len(result.templates) if result.templates else 0}")
    print(f"  # Generation general settings set: "
          f"{len(result.generation_settings) if result.generation_settings else 0}")
    print(f"  # Entry video options fulfilled: {len(result.video_options) if result.video_options else 0}")
