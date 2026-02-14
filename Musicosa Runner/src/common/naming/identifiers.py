from uuid import NAMESPACE_OID, UUID, uuid5

MEMBERS_NAMESPACE = NAMESPACE_OID
NOMINATIONS_NAMESPACE = NAMESPACE_OID


def generate_member_uuid5(member_name: str) -> UUID:
    if not member_name:
        raise ValueError("Member name cannot be empty")

    return uuid5(MEMBERS_NAMESPACE, member_name)


def generate_nomination_uuid5(game_title: str, nominee: str, award_slug: str) -> UUID:
    if not game_title:
        raise ValueError("Game title cannot be empty")

    if not award_slug:
        raise ValueError("Award slug cannot be empty")

    return uuid5(NOMINATIONS_NAMESPACE, f"{game_title}{nominee}{award_slug}")


def generate_nomination_uuid5_from_nomination_str(full_nomination_str: str, award_slug: str) -> UUID:
    nomination_bits = full_nomination_str.split(sep="|", maxsplit=1)

    if len(nomination_bits) == 1:
        game_title = nomination_bits[0].strip()
        nominee = ""
    else:
        game_title = nomination_bits[1].strip()
        nominee = nomination_bits[0].strip()

    return generate_nomination_uuid5(game_title, nominee, award_slug)
