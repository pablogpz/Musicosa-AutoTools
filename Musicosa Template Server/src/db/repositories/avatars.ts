import db from '@/db/database'
import { Avatar } from '@/db/models'
import { avatars } from '@/db/schema'

export interface AvatarsRepository {
    getAvatars: () => Promise<Avatar[]>
}

let avatarsCache: Avatar[] = []

const getAvatars = async (): Promise<Avatar[]> => {
    const query = db.select().from(avatars)

    if (process.env.NODE_ENV === 'development') return query

    if (avatarsCache.length === 0) {
        const result = await query
        if (result) avatarsCache = result
    }

    return structuredClone(avatarsCache)
}

const avatarsRepository: AvatarsRepository = { getAvatars }

export default avatarsRepository
