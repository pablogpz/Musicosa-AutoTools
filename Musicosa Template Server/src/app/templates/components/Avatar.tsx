import { defaultAvatar } from '@/db/defaults'

import { ResolvedAvatar } from '@/app/templates/common/withTemplateProps'

export interface AvatarProps {
    avatar: ResolvedAvatar,
    avatarScale?: number
    formattedScore: string,
}

export default function Avatar({ avatar, avatarScale = 1, formattedScore }: AvatarProps) {

    const {
        resolvedImageFilename,
        imageHeight,
        scoreBoxPositionTop,
        scoreBoxPositionLeft,
        scoreBoxFontScale,
        scoreBoxFontColor
    } = avatar

    const avatarContainerStyleProps = {
        height: `${imageHeight * avatarScale}px`,
        fontSize: `${imageHeight * avatarScale * scoreBoxFontScale}px`
    }

    const scoreBoxStyleProps = {
        top: `${scoreBoxPositionTop}%`,
        left: `${scoreBoxPositionLeft}%`,
        color: scoreBoxFontColor ?? defaultAvatar.scoreBoxFontColor!
    }

    return (
        <div className="relative inline-block" style={avatarContainerStyleProps}>
            <img className="h-full w-auto" src={`/avatars/${resolvedImageFilename}`} alt="avatar image"/>
            <p className='absolute translate-x-[-50%] translate-y-[-50%] m-0 text-[1em]' style={scoreBoxStyleProps}>
                {formattedScore}
            </p>
        </div>
    )
}