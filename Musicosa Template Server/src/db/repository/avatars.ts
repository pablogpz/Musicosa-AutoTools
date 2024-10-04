import db from '@/db/database'
import { Avatar, avatars } from '@/db/schema'

export interface AvatarsRepository {
    getAvatars: () => Promise<Avatar[]>
}

let avatarsCache: Avatar[] = []

const getAvatars = async () => {
    const databaseQuery = db.select().from(avatars)

    if (process.env.NODE_ENV === "development")
        return databaseQuery

    if (avatarsCache.length === 0) {
        const allAvatars = await databaseQuery
        if (allAvatars)
            avatarsCache = allAvatars
    }

    return avatarsCache.map(v => ({ ...v })) // Careful: Shallow copy
}

const avatarsRepository: AvatarsRepository = { getAvatars }

export default avatarsRepository