from typing import Any, Iterable

from common.model.models import DomainModel


def bulk_pack(collection: Iterable) -> list[dict[Any, Any]]:
    """
    Create a collection of ORM entities in the format of the input of a Peewee bulk operation
    :param collection: Collection of ORM entities
    :return: A list of dictionaries with the data of the ORM entities compatible with Peewee bulk operations
    """
    bulk_data = []

    for item in collection:
        if not isinstance(item, DomainModel):
            raise TypeError(f"Collection contains an item that isn't a domain model ('{item}')")

        orm_entity = item.to_orm()

        if not getattr(orm_entity, "__data__", None):
            # Fucked around and found out (:
            raise TypeError(f"ORM entity '{orm_entity}' doesn't store its data in '__data__'")

        bulk_data.append(orm_entity.__data__)

    return bulk_data
