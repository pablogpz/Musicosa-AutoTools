import React from 'react'

import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import { defaultResolvedAvatar } from '@/app/templates/common/withTemplateProps/defaults'
import Avatar from '@/app/templates/components/Avatar'
import VideoPlaceholder from '@/app/templates/components/VideoPlaceholder'

export type TemplateProps = ResolvedTemplateProps

// SAMPLE TEMPLATE

export function Template(
    {
        rankingPlace,
        title,
        specialTopic,
        formattedAvgScore,
        avatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        author,
        contestants,
        avatars,
        scores
    }: TemplateProps) {

    const authorAvatar = avatars.find(avatar => avatar.id === author.avatar) ?? defaultResolvedAvatar
    const authorScore = scores.find(score => score.contestant === author.id)!.formattedScore

    return (
        <div className="flex flex-col flex-wrap place-content-center content-around w-full h-full bg-black">
            <div className="flex flex-row">
                <div className="flex flex-col justify-around mr-16">
                    <div>
                        <p className="text-4xl p-2 bg-white rounded w-fit">
                            {title} {specialTopic && `(${specialTopic})`}
                        </p>
                        <p className="text-3xl text-white mt-5">{rankingPlace}º</p>
                    </div>
                    <div className="flex flex-row bg-gray-500 rounded">
                        <Avatar avatar={authorAvatar} avatarScale={avatarScale} formattedScore={authorScore}/>
                        <p className="text-3xl text-white self-center pr-10">Nota media {formattedAvgScore}</p>
                    </div>
                </div>
                <VideoPlaceholder widthPx={videoBoxWidthPx} heightPx={videoBoxHeightPx}/>
            </div>
            <div className="mt-10 flex content-center justify-between">
                {contestants.map((contestant, i) =>
                    <Avatar
                        key={i}
                        avatar={avatars.find(avatar => contestant.avatar === avatar.id) ?? defaultResolvedAvatar}
                        avatarScale={avatarScale}
                        formattedScore={scores.find(score => score.contestant === contestant.id)!.formattedScore}/>)}
            </div>
        </div>
    )
}