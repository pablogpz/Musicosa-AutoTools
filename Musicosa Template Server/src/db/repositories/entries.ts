import { count, eq, sql } from 'drizzle-orm'

import db from '@/db/database'
import { entries, entriesStats } from '@/db/schema'

export interface EntriesRepository {
    getSequenceNumberInAuthorEntries: (entryId: string) => Promise<[number, number] | undefined>
    getSequenceNumberInSpecialTopic: (entryId: string) => Promise<[number, number] | undefined>
    getSequenceNumberInTie: (entryId: string) => Promise<[number, number] | undefined>
    getAvgScoreDeltaFromPreviousEntry: (entryId: string) => Promise<number | undefined>
}

const sequenceNumbersInAuthorEntries: Map<string, [number, number]> = new Map()
const sequenceNumbersInSpecialTopic: Map<string, [number, number]> = new Map()
const sequenceNumbersInTie: Map<string, [number, number]> = new Map()
const avgScoreDeltas: Map<string, number> = new Map()

async function getSequenceNumberInAuthorEntries(entryId: string): Promise<[number, number] | undefined> {
    if (process.env.NODE_ENV === 'development' || !sequenceNumbersInAuthorEntries.has(entryId)) {
        const sq = db.select({ authorId: entries.author }).from(entries).where(eq(entries.id, entryId)).as('sq')

        const sequenceNumbersResult = await db
            .select({
                entryId: entries.id,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`,
            })
            .from(entries)
            .innerJoin(entriesStats, eq(entries.id, entriesStats.entry))
            .innerJoin(sq, eq(entries.author, sq.authorId))

        const entriesCountResult = await db
            .select({ count: count() })
            .from(entries)
            .innerJoin(sq, eq(entries.author, sq.authorId))
        const entriesCount = entriesCountResult[0].count

        for (const row of sequenceNumbersResult)
            sequenceNumbersInAuthorEntries.set(row.entryId, [row.sequenceNumber, entriesCount])
    }

    return sequenceNumbersInAuthorEntries.get(entryId)
}

async function getSequenceNumberInSpecialTopic(entryId: string): Promise<[number, number] | undefined> {
    if (process.env.NODE_ENV === 'development' || !sequenceNumbersInSpecialTopic.has(entryId)) {
        const sq = db
            .select({ specialTopic: entries.specialTopic })
            .from(entries)
            .where(eq(entries.id, entryId))
            .as('sq')

        const sequenceNumbersResult = await db
            .select({
                entryId: entries.id,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`,
            })
            .from(entries)
            .innerJoin(entriesStats, eq(entries.id, entriesStats.entry))
            .innerJoin(sq, eq(entries.specialTopic, sq.specialTopic))

        const entriesCountResult = await db
            .select({ count: count() })
            .from(entries)
            .innerJoin(sq, eq(entries.specialTopic, sq.specialTopic))
        const entriesCount = entriesCountResult[0].count

        for (const row of sequenceNumbersResult)
            sequenceNumbersInSpecialTopic.set(row.entryId, [row.sequenceNumber, entriesCount])
    }

    return sequenceNumbersInSpecialTopic.get(entryId)
}

async function getSequenceNumberInTie(entryId: string): Promise<[number, number] | undefined> {
    if (process.env.NODE_ENV === 'development' || !sequenceNumbersInTie.has(entryId)) {
        const sq = db
            .select({ rankingPlace: entriesStats.rankingPlace })
            .from(entriesStats)
            .where(eq(entriesStats.entry, entryId))
            .as('sq')

        const tieResult = await db
            .select({
                entryId: entriesStats.entry,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${entriesStats.rankingSequence} DESC)`,
            })
            .from(entriesStats)
            .innerJoin(sq, eq(entriesStats.rankingPlace, sq.rankingPlace))

        if (tieResult.length <= 1) return undefined // Entries that don't exist and ties of 1 are not considered ties

        for (const row of tieResult) sequenceNumbersInTie.set(row.entryId, [row.sequenceNumber, tieResult.length])
    }

    return sequenceNumbersInTie.get(entryId)
}

async function getAvgScoreDeltaFromPreviousEntry(entryId: string): Promise<number | undefined> {
    if (process.env.NODE_ENV === 'development' || !avgScoreDeltas.has(entryId)) {
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
    getSequenceNumberInTie,
    getAvgScoreDeltaFromPreviousEntry,
}

export default entriesRepository
