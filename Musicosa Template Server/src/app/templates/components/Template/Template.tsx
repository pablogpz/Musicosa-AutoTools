import React from 'react'

import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import Avatar from '@/app/templates/components/Avatar'
import VideoPlaceholder from '@/app/templates/components/VideoPlaceholder'

export type TemplateProps = ResolvedTemplateProps

// SAMPLE TEMPLATE

export function Template(
    {
        gameTitle,
        nominee,
        rankingPlace,
        formattedAvgScore,
        avatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        award,
        members
    }: TemplateProps) {

    return (
        <div className="grid grid-cols-[31.5%_68.5%] grid-rows-[71.5%_28.5%] w-full h-full bg-black p-7 overflow-clip">
            <div className="row-start-1 row-end-2 col-start-1 col-end-2 h-full">
                <div className="flex flex-col h-full justify-evenly">
                    <p className="text-5xl p-2 bg-white rounded">
                        {award.designation}
                    </p>
                    <p className="text-4xl p-2 bg-white rounded">
                        [{rankingPlace}º] {gameTitle} {nominee && ` (${nominee})`}
                    </p>
                    <div className="flex flex-row justify-center">
                        <p className="text-3xl text-white self-center">Media {formattedAvgScore}</p>
                    </div>
                </div>
            </div>
            <div className="row-start-1 row-end-2 col-start-2 col-end-3 place-self-center">
                <VideoPlaceholder widthPx={videoBoxWidthPx} heightPx={videoBoxHeightPx}/>
            </div>
            <div className="row-start-2 row-end-3 col-start-1 col-end-3">
                <div className="flex content-center justify-between">
                    {members.map((member, i) =>
                        <Avatar
                            key={i}
                            avatar={member.avatar}
                            avatarScale={avatarScale}
                            formattedScore={member.vote.formattedScore}/>)}
                </div>
            </div>
        </div>
    )
}