import { ResolvedAvatar } from '@/app/templates/common/withTemplateProps'

export interface AvatarProps {
    avatar: ResolvedAvatar,
    avatarScale?: number
}

export default function Avatar({ avatar, avatarScale = 1 }: AvatarProps) {

    const {
        resolvedImageFilename,
        imageHeight
    } = avatar

    const avatarContainerStyleProps = {
        height: `${imageHeight * avatarScale}px`,
    }

    return (
        <div className="relative inline-block" style={avatarContainerStyleProps}>
            <img className="h-full w-auto" src={`/avatars/${resolvedImageFilename}`} alt="avatar image"/>
        </div>
    )
}