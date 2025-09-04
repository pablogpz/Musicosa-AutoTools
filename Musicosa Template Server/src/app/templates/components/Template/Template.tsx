import React from 'react'
import { Open_Sans } from 'next/font/google'

import { ResolvedTemplateProps, TemplateSettingsProps } from '@/app/templates/common/withTemplateProps'
import Avatar from '@/app/templates/components/Avatar'
import VideoPlaceholder from '@/app/templates/components/VideoPlaceholder'

export type TemplateProps = TemplateSettingsProps & ResolvedTemplateProps

const open_sans = Open_Sans({
    subsets: ['latin'],
    display: 'swap',
    variable: '--font-open-sans'
})

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
        members,
        scoreMinValue,
        scoreMaxValue
    }: TemplateProps) {

    const sortedMembers = members.sort((a, b) => a.vote.score - b.vote.score)

    function innerLinearInterpolateScoreColor(score: number): string {
        return linearInterpolateScoreColor(score, scoreMinValue, scoreMaxValue)
    }

    const headerComponent =
        <div className="flex flex-row items-center justify-center mt-9">
            <div className={`bg-white ${open_sans.className} rounded-xl p-6 mr-10`}>
                <p className="text-4xl font-bold">{rankingPlace}º</p>
            </div>
            <p className="text-white text-5xl font-bold max-w-96">{award.designation}</p>
        </div>

    const nominationInfoComponent =
        <div className="flex flex-row items-center mt-20 mx-5">
            <div className="text-white mr-4">
                <p className={`text-5xl ${open_sans.className} font-black`}>{formattedAvgScore}</p>
            </div>
            <div className="h-full w-[0.25em] bg-white mr-4"/>
            <div className="flex flex-col justify-around size-full">
                {nominee && <p className="text-4xl font-semibold bg-white p-4 mb-4">{nominee}</p>}
                <p className={`${nominee ? 'text-2xl font-normal py-2' : 'text-4xl font-semibold py-4'} bg-white px-4`}>
                    {gameTitle}
                </p>
            </div>
        </div>

    return (
        <div className="grid grid-cols-[32%_68%] grid-rows-[72%_28%] w-full h-full p-7 overflow-clip bg-black">
            <div className="row-start-1 row-end-2 col-start-1 col-end-2 h-full">
                <div className="flex flex-col h-full">
                    {headerComponent}
                    {nominationInfoComponent}
                </div>
            </div>
            <div className="row-start-1 row-end-2 col-start-2 col-end-3 place-self-center">
                <VideoPlaceholder widthPx={videoBoxWidthPx} heightPx={videoBoxHeightPx}/>
            </div>
            <div className="row-start-2 row-end-3 col-start-1 col-end-3">
                <div className="flex flex-row content-center justify-evenly items-center h-full">
                    {sortedMembers.map((member, i) =>
                        <Avatar
                            key={i}
                            avatar={member.avatar}
                            avatarScale={avatarScale}
                            formattedScore={member.vote.formattedScore}
                            scoreColor={innerLinearInterpolateScoreColor(member.vote.score)}/>)}
                </div>
            </div>
        </div>
    )
}

type Color = { r: number, g: number, b: number }
type CSS_RGB_Color = string

const lowestGradeColor: Color = { r: 255, g: 0, b: 0 }
const highestGradeColor: Color = { r: 0, g: 230, b: 0 }

function linearInterpolateScoreColor(score: number, min: number, max: number): CSS_RGB_Color {
    const normalizedScore = (score - min) / (max - min)

    const interpolatedColor: Color = {
        r: lowestGradeColor.r * (1 - normalizedScore) + highestGradeColor.r * normalizedScore,
        g: lowestGradeColor.g * (1 - normalizedScore) + highestGradeColor.g * normalizedScore,
        b: lowestGradeColor.b * (1 - normalizedScore) + highestGradeColor.b * normalizedScore,
    }

    return `rgb(${interpolatedColor.r},${interpolatedColor.g},${interpolatedColor.b})`
}