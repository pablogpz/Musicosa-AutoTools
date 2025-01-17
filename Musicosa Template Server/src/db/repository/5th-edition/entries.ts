import { count, eq, sql } from 'drizzle-orm'

import db from '@/db/database'
import { entries, entriesStats } from '@/db/schema'

export interface EntriesRepository {
    getEntrySequenceNumberInSpecialTopic: (entryUUID: string) => Promise<[number, number] | undefined>,
}

const entrySequenceNumbersInSpecialTopics: Map<string, [number, number]> = new Map()

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

const entriesRepository: EntriesRepository = {
    getEntrySequenceNumberInSpecialTopic,
}

export default entriesRepository