import db from '@/db/database'
import { Contestant, contestants } from '@/db/schema'

export interface ContestantsRepository {
    getContestants: () => Promise<Contestant[]>
}

let contestantsCache: Contestant[] = []

const getContestants = async () => {
    const databaseQuery = db.select().from(contestants)

    if (process.env.NODE_ENV === "development")
        return databaseQuery

    if (contestantsCache.length === 0) {
        const allContestants = await databaseQuery
        if (allContestants)
            contestantsCache = allContestants
    }

    return contestantsCache.map(v => ({...v})) // Careful: Shallow copy
}

const contestantsRepository: ContestantsRepository = { getContestants }

export default contestantsRepository