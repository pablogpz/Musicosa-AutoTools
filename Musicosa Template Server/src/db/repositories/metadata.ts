import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { Metadata, MetadataFields } from '@/db/models'
import { metadata } from '@/db/schema'

export interface MetadataRepository {
    getMetadataByField: (field: MetadataFields) => Promise<Metadata | undefined>
}

const metadataCache: Map<MetadataFields, Metadata> = new Map()

const getMetadataByField = async (field: MetadataFields): Promise<Metadata | undefined> => {
    if (process.env.NODE_ENV === 'development' || !metadataCache.has(field)) {
        const result = await db.select().from(metadata).where(eq(metadata.field, field))

        if (result.length == 0) return undefined

        metadataCache.set(field, result[0])
    }

    return structuredClone(metadataCache.get(field))
}

const metadataRepository: MetadataRepository = { getMetadataByField }

export default metadataRepository
