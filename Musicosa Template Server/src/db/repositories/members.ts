import db from '@/db/database'
import { Member } from '@/db/models'
import { members } from '@/db/schema'

export interface MembersRepository {
    getMembers: () => Promise<Member[]>
}

let membersCache: Member[] = []

const getMembers = async () => {
    const query = db.select().from(members)

    if (process.env.NODE_ENV === 'development') return query

    if (membersCache.length === 0) {
        const result = await query
        if (result) membersCache = result
    }

    return structuredClone(membersCache)
}

const membersRepository: MembersRepository = { getMembers }

export default membersRepository