import { count, eq, sql } from 'drizzle-orm'

import db from '@/db/database'
import { entries, entriesStats } from '@/db/schema'

export interface EntriesRepository {
    getEntrySequenceNumberInAuthorEntries: (entryUUID: string) => Promise<[number, number] | undefined>,
    getEntrySequenceNumberInSpecialTopic: (entryUUID: string) => Promise<[number, number] | undefined>,
    getAvgScoreDeltaWithPreviousEntry: (entryUUID: string) => Promise<number | undefined>
}

const entrySequenceNumbersInAuthorsEntries: Map<string, [number, number]> = new Map()
const entrySequenceNumbersInSpecialTopics: Map<string, [number, number]> = new Map()
const avgScoreDeltas: Map<string, number> = new Map()

async function getEntrySequenceNumberInAuthorEntries(entryUUID: string): Promise<[number, number] | undefined> {
    if (!entrySequenceNumbersInAuthorsEntries.has(entryUUID) || process.env.NODE_ENV === "development") {
        const entryAuthorResult = await db
            .select({ author: entries.author })
            .from(entries)
            .where(eq(entries.id, entryUUID))
        if (!entryAuthorResult.length || !entryAuthorResult[0].author)
            return undefined

        const entryAuthor = entryAuthorResult[0].author

        const sequenceNumbersResult = await db
            .select({
                id: entries.id,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`
            })
            .from(entries).innerJoin(entriesStats, eq(entries.id, entriesStats.entry))
            .where(eq(entries.author, entryAuthor))

        const totalCountResult = await db
            .select({ total: count() })
            .from(entries)
            .where(eq(entries.author, entryAuthor))
        const totalCount = totalCountResult[0].total

        for (const row of sequenceNumbersResult)
            entrySequenceNumbersInAuthorsEntries.set(row.id, [row.sequenceNumber, totalCount])
    }

    return entrySequenceNumbersInAuthorsEntries.get(entryUUID)
}

async function getEntrySequenceNumberInSpecialTopic(entryUUID: string): Promise<[number, number] | undefined> {
    if (!entrySequenceNumbersInSpecialTopics.has(entryUUID) || process.env.NODE_ENV === "development") {
        const entrySpecialTopicResult = await db
            .select({ specialTopic: entries.specialTopic })
            .from(entries)
            .where(eq(entries.id, entryUUID))
        if (!entrySpecialTopicResult.length || !entrySpecialTopicResult[0].specialTopic)
            return undefined

        const entrySpecialTopic = entrySpecialTopicResult[0].specialTopic

        const sequenceNumbersResult = await db
            .select({
                id: entries.id,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`
            })
            .from(entries).innerJoin(entriesStats, eq(entries.id, entriesStats.entry))
            .where(eq(entries.specialTopic, entrySpecialTopic))

        const totalCountResult = await db
            .select({ total: count() })
            .from(entries)
            .where(eq(entries.specialTopic, entrySpecialTopic))
        const totalCount = totalCountResult[0].total

        for (const row of sequenceNumbersResult)
            entrySequenceNumbersInSpecialTopics.set(row.id, [row.sequenceNumber, totalCount])
    }

    return entrySequenceNumbersInSpecialTopics.get(entryUUID)
}

async function getAvgScoreDeltaWithPreviousEntry(entryUUID: string): Promise<number | undefined> {
    if (!avgScoreDeltas.has(entryUUID) || process.env.NODE_ENV === "development") {
        const avgScoreDeltaResult = await db
            .select({
                id: entries.id,
                delta: sql<number>`${entriesStats.avgScore} - lag(${entriesStats.avgScore}, 1, ${entriesStats.avgScore}) OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`
            })
            .from(entries).innerJoin(entriesStats, eq(entries.id, entriesStats.entry))

        for (const row of avgScoreDeltaResult)
            avgScoreDeltas.set(row.id, row.delta)
    }

    return avgScoreDeltas.get(entryUUID)
}

const entriesRepository: EntriesRepository = {
    getEntrySequenceNumberInAuthorEntries,
    getEntrySequenceNumberInSpecialTopic,
    getAvgScoreDeltaWithPreviousEntry
}

export default entriesRepository