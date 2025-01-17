import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'

export interface EditionProps {
    scoreMinValue: number,
    scoreMaxValue: number,
    sequenceNumberInSpecialTopic: [number, number] | undefined,
}

export type TemplateProps = ResolvedTemplateProps & EditionProps

export function Template(
    {
        rankingPlace,
        title,
        specialTopic,
        formattedAvgScore,
        avatarScale,
        authorAvatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        author,
        contestants,
        avatars,
        scores,
        scoreMinValue,
        scoreMaxValue,
        sequenceNumberInSpecialTopic
    }: TemplateProps) {
    return <></>
}