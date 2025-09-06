import { count, eq, sql } from 'drizzle-orm'

import db from '@/db/database'
import { entries, entriesStats } from '@/db/schema'

export interface EntriesRepository {
    getSequenceNumberInAuthorEntries: (entryId: string) => Promise<[number, number] | undefined>
    getSequenceNumberInSpecialTopic: (entryId: string) => Promise<[number, number] | undefined>
    getAvgScoreDeltaFromPreviousEntry: (entryId: string) => Promise<number | undefined>
}

const sequenceNumbersInAuthorEntries: Map<string, [number, number]> = new Map()
const sequenceNumbersInSpecialTopic: Map<string, [number, number]> = new Map()
const avgScoreDeltas: Map<string, number> = new Map()

async function getSequenceNumberInAuthorEntries(entryId: string): Promise<[number, number] | undefined> {
    if (!sequenceNumbersInAuthorEntries.has(entryId) || process.env.NODE_ENV === 'development') {
        const authorResult = await db.select({ author: entries.author }).from(entries).where(eq(entries.id, entryId))
        if (authorResult.length == 0 || !authorResult[0].author) return undefined
        const authorId = authorResult[0].author

        const sequenceNumbersResult = await db
            .select({
                entryId: entries.id,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`,
            })
            .from(entries)
            .innerJoin(entriesStats, eq(entries.id, entriesStats.entry))
            .where(eq(entries.author, authorId))

        const entriesCountResult = await db.select({ count: count() }).from(entries).where(eq(entries.author, authorId))
        const entriesCount = entriesCountResult[0].count

        for (const row of sequenceNumbersResult)
            sequenceNumbersInAuthorEntries.set(row.entryId, [row.sequenceNumber, entriesCount])
    }

    return sequenceNumbersInAuthorEntries.get(entryId)
}

async function getSequenceNumberInSpecialTopic(entryId: string): Promise<[number, number] | undefined> {
    if (!sequenceNumbersInSpecialTopic.has(entryId) || process.env.NODE_ENV === 'development') {
        const specialTopicResult = await db
            .select({ specialTopic: entries.specialTopic })
            .from(entries)
            .where(eq(entries.id, entryId))
        if (specialTopicResult.length == 0 || !specialTopicResult[0].specialTopic) return undefined
        const specialTopic = specialTopicResult[0].specialTopic

        const sequenceNumbersResult = await db
            .select({
                entryId: entries.id,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`,
            })
            .from(entries)
            .innerJoin(entriesStats, eq(entries.id, entriesStats.entry))
            .where(eq(entries.specialTopic, specialTopic))

        const entriesCountResult = await db
            .select({ count: count() })
            .from(entries)
            .where(eq(entries.specialTopic, specialTopic))
        const entriesCount = entriesCountResult[0].count

        for (const row of sequenceNumbersResult)
            sequenceNumbersInSpecialTopic.set(row.entryId, [row.sequenceNumber, entriesCount])
    }

    return sequenceNumbersInSpecialTopic.get(entryId)
}

async function getAvgScoreDeltaFromPreviousEntry(entryId: string): Promise<number | undefined> {
    if (!avgScoreDeltas.has(entryId) || process.env.NODE_ENV === 'development') {
        const avgScoreDeltaResult = await db
            .select({
                entryId: entries.id,
                delta: sql<number>`${entriesStats.avgScore} - lag(${entriesStats.avgScore}, 1, ${entriesStats.avgScore}) OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`,
            })
            .from(entries)
            .innerJoin(entriesStats, eq(entries.id, entriesStats.entry))

        for (const row of avgScoreDeltaResult) avgScoreDeltas.set(row.entryId, row.delta)
    }

    return avgScoreDeltas.get(entryId)
}

const entriesRepository: EntriesRepository = {
    getSequenceNumberInAuthorEntries,
    getSequenceNumberInSpecialTopic,
    getAvgScoreDeltaFromPreviousEntry,
}

export default entriesRepository
