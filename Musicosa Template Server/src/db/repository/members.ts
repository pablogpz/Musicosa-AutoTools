import db from '@/db/database'
import { Member, members } from '@/db/schema'

export interface MembersRepository {
    getMembers: () => Promise<Member[]>
}

let membersCache: Member[] = []

const getMembers = async () => {
    const databaseQuery = db.select().from(members)

    if (process.env.NODE_ENV === "development")
        return databaseQuery

    if (membersCache.length === 0) {
        const allMembers = await databaseQuery
        if (allMembers)
            membersCache = allMembers
    }

    return membersCache.map(v => ({ ...v })) // Careful: Shallow copy
}

const membersRepository: MembersRepository = { getMembers }

export default membersRepository