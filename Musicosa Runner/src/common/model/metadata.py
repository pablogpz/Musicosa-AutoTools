from common.model.models import MetadataFields, Metadata


def get_metadata_by_field(field: MetadataFields) -> Metadata | None:
    if not field:
        return None

    metadata = Metadata.ORM.get(Metadata.ORM.field == field)

    return metadata.to_domain() if metadata else None
