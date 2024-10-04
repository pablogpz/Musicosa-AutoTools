import { eq } from 'drizzle-orm'

import db from '@/db/database'
import { metadata, Metadata } from '@/db/schema'
import { MetadataFields } from '@/db/metadata'

export interface MetadataRepository {
    getMetadataByField: (field: MetadataFields) => Promise<Metadata | undefined>
    getMetadataCollection: () => Promise<Metadata[]>
}

let metadataCollectionCache: Metadata[] = []

const getMetadataByField = async (field: string) => {
    const databaseQuery = db.select().from(metadata).where(eq(metadata.field, field))
    let databaseResult

    if (process.env.NODE_ENV === "development") {
        databaseResult = await databaseQuery
        return databaseResult.length > 0 ? databaseResult[0] : undefined
    }

    let metadataCacheResult
    if ((metadataCacheResult = metadataCollectionCache.find(metadata => metadata.field === field)))
        return { ...metadataCacheResult } // Careful: Shallow copy

    databaseResult = await databaseQuery

    let metadataDatabaseResult
    if (databaseResult.length > 0)
        metadataCollectionCache.push((metadataDatabaseResult = databaseResult[0]))

    return metadataDatabaseResult
}

const getMetadataCollection = async () => {
    const databaseQuery = db.select().from(metadata)

    if (process.env.NODE_ENV === "development")
        return databaseQuery

    if (metadataCollectionCache.length === 0) {
        const metadataCollectionResult = await databaseQuery
        if (metadataCollectionResult)
            metadataCollectionCache = metadataCollectionResult
    }

    return metadataCollectionCache.map(v => ({ ...v })) // Careful: Shallow copy
}

const metadataRepository: MetadataRepository = { getMetadataByField, getMetadataCollection }

export default metadataRepository