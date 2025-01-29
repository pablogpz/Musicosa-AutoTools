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
        authorAvatarScale,
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
        <div className="grid grid-cols-[31.5%_68.5%] grid-rows-[71.5%_28.5%] w-full h-full bg-black p-7 overflow-clip">
            <div className="row-start-1 row-end-2 col-start-1 col-end-2 h-full">
                <div className="flex flex-col h-full justify-evenly">
                    <p className="text-4xl p-2 bg-white rounded">
                        [{rankingPlace}º] {title} {specialTopic && `(${specialTopic})`}
                    </p>
                    <div className="flex flex-row justify-center">
                        <Avatar avatar={authorAvatar} avatarScale={authorAvatarScale}/>
                        <p className="text-xl text-white self-center">{authorScore}</p>
                        <p className="text-3xl text-white self-center">Media {formattedAvgScore}</p>
                    </div>
                </div>
            </div>
            <div className="row-start-1 row-end-2 col-start-2 col-end-3 place-self-center">
                <VideoPlaceholder widthPx={videoBoxWidthPx} heightPx={videoBoxHeightPx}/>
            </div>
            <div className="row-start-2 row-end-3 col-start-1 col-end-3">
                <div className="flex content-center justify-between">
                    {contestants.map((contestant, i) =>
                        <Avatar
                            key={i}
                            avatar={avatars.find(avatar => contestant.avatar === avatar.id) ?? defaultResolvedAvatar}
                            avatarScale={avatarScale}/>)}
                </div>
            </div>
        </div>
    )
}