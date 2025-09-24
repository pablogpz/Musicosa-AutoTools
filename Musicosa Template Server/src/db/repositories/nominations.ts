import { and, eq, sql } from 'drizzle-orm'

import db from '@/db/database'
import { nominationStats, nominations } from '@/db/schema'

export interface NominationsRepository {
    getSequenceNumberInTie(nominationId: string): Promise<[number, number] | undefined>
}

const sequenceNumbersInTie: Map<string, [number, number]> = new Map()

async function getSequenceNumberInTie(nominationId: string): Promise<[number, number] | undefined> {
    if (process.env.NODE_ENV === 'development' || !sequenceNumbersInTie.has(nominationId)) {
        const sq = db
            .select({
                awardSlug: nominations.award,
                rankingPlace: nominationStats.rankingPlace,
            })
            .from(nominations)
            .innerJoin(nominationStats, eq(nominations.id, nominationStats.nomination))
            .where(eq(nominations.id, nominationId))
            .as('sq')

        const tieResult = await db
            .select({
                nominationId: nominations.id,
                sequenceNumber: sql<number>`row_number() OVER (ORDER BY ${nominationStats.rankingSequence} DESC)`,
            })
            .from(nominations)
            .innerJoin(nominationStats, eq(nominations.id, nominationStats.nomination))
            .innerJoin(sq, and(eq(nominations.award, sq.awardSlug), eq(nominationStats.rankingPlace, sq.rankingPlace)))

        if (tieResult.length <= 1) return undefined // Entries that don't exist and ties of 1 are not considered ties

        for (const row of tieResult) sequenceNumbersInTie.set(row.nominationId, [row.sequenceNumber, tieResult.length])
    }

    return sequenceNumbersInTie.get(nominationId)
}

const nominationsRepository: NominationsRepository = {
    getSequenceNumberInTie,
}

export default nominationsRepository
