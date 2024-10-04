import { defaultAvatar } from '@/db/defaults'

import { ResolvedAvatar } from './resolveTemplateProps'

export const defaultResolvedAvatar: ResolvedAvatar = {
    ...defaultAvatar,
    resolvedImageFilename: defaultAvatar.imageFilename
}