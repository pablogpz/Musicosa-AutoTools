import db from '@/db/database'
import { contestants } from '@/db/schema'
import { Contestant } from '@/db/models'

export interface ContestantsRepository {
    getContestants: () => Promise<Contestant[]>
}

let contestantsCache: Contestant[] = []

const getContestants = async (): Promise<Contestant[]> => {
    const query = db.select().from(contestants)

    if (process.env.NODE_ENV === "development")
        return query

    if (contestantsCache.length === 0) {
        const result = await query
        if (result)
            contestantsCache = result
    }

    return structuredClone(contestantsCache)
}

const contestantsRepository: ContestantsRepository = { getContestants }

export default contestantsRepository