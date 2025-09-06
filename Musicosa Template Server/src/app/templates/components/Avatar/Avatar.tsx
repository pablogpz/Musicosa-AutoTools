import { Caveat } from 'next/font/google'

import { ResolvedAvatar } from '@/app/templates/common/withTemplateProps'

export interface AvatarProps {
    avatar: ResolvedAvatar
    avatarScale?: number
    formattedScore: string
    scoreColor?: string
}

const caveat = Caveat({
    subsets: ['latin'],
    display: 'swap',
    weight: '600',
    variable: '--font-caveat',
})

export default function Avatar({ avatar, avatarScale = 1, formattedScore, scoreColor }: AvatarProps) {
    const {
        resolvedImageFilename,
        imageHeight,
        scoreBoxPositionTop,
        scoreBoxPositionLeft,
        scoreBoxFontScale,
        scoreBoxFontColor,
    } = avatar

    const avatarContainerStyleProps = {
        height: `${imageHeight * avatarScale}px`,
        fontSize: `${imageHeight * avatarScale * scoreBoxFontScale}px`,
    }

    const scoreBoxStyleProps = {
        ...caveat.style,
        top: `${scoreBoxPositionTop}%`,
        left: `${scoreBoxPositionLeft}%`,
        color: scoreColor ?? scoreBoxFontColor,
    }

    return (
        <div
            className='relative inline-block'
            style={avatarContainerStyleProps}
        >
            <img
                className='h-full w-auto'
                src={`/avatars/${resolvedImageFilename}`}
                alt='avatar image'
            />
            <p
                className='absolute translate-x-[-50%] translate-y-[-50%] text-[1em]'
                style={scoreBoxStyleProps}
            >
                {formattedScore}
            </p>
        </div>
    )
}