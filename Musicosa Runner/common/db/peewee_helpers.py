from typing import Iterable, Any


def bulk_pack(collection: Iterable) -> list[dict[Any, Any]]:
    """
    Create a collection of ORM entities in the format of the input of a Peewee bulk operation
    :param collection: Collection of ORM entities
    :return: A list of dictionaries with the data of the ORM entities compatible with Peewee bulk operations
    """
    bulk_data = []

    for item in collection:
        if not callable(getattr(item, 'to_orm', None)):
            raise TypeError(f"Collection contains an item '{item}' that isn't an ORM entity ('to_orm' method missing)")

        orm_entity = item.to_orm()

        if not getattr(orm_entity, '__data__', None):
            # Fucked around and found out (:
            raise TypeError(f"ORM entity '{orm_entity}' doesn't have a '__data__' attribute")

        bulk_data.append(item.to_orm().__data__)

    return bulk_data
