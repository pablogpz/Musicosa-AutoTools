import React from 'react'

import { Open_Sans } from 'next/font/google'

import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'
import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import Avatar from '@/app/templates/components/Avatar'
import VideoPlaceholder from '@/app/templates/components/VideoPlaceholder'

export interface EditionProps {
    scoreMinValue: number,
    scoreMaxValue: number,
    sequenceNumberInAuthorEntries: [number, number],
    avgScoreDelta: number
}

export type TemplateProps = ResolvedTemplateProps & EditionProps

const open_sans = Open_Sans({
    subsets: ['latin'],
    display: 'swap',
    variable: '--font-open-sans'
})

// Musicosa 7th Edition Template

export function Template(
    {
        title,
        rankingPlace,
        formattedAvgScore,
        avatarScale,
        authorAvatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        author,
        contestants,
        scoreMinValue,
        scoreMaxValue,
        sequenceNumberInAuthorEntries,
        avgScoreDelta
    }: TemplateProps) {

    const [songTitle, workTitle] = getTitleBits(title)
    const [sequence, sequenceOutOf] = sequenceNumberInAuthorEntries
    const formattedAvgScoreDelta = formatNumberToDecimalPrecision(avgScoreDelta, 4)

    const sortedContestantsByScore = contestants
        .sort((a, b) => a.scoring.score - b.scoring.score)
    const lowestScoreGroup = sortedContestantsByScore
        .slice(0, sortedContestantsByScore.findLastIndex(contestant =>
            contestant.scoring.score === sortedContestantsByScore[0].scoring.score) + 1)
        .sort(() => Math.random() - 0.5)
    const highestScoreGroup = sortedContestantsByScore
        .slice(sortedContestantsByScore.findIndex(contestant =>
            contestant.scoring.score === sortedContestantsByScore.at(-1)?.scoring.score))
        .sort(() => Math.random() - 0.5)
    const middleScoreGroup = sortedContestantsByScore
        .slice(lowestScoreGroup.length, sortedContestantsByScore.length - highestScoreGroup.length)

    function innerLinearInterpolateScoreColor(score: number): string {
        return linearInterpolateScoreColor(score, scoreMinValue, scoreMaxValue)
    }

    const rankingPlaceComponent =
        <p className={`${rankingPlace! >= 100 ?
            'text-4xl' : rankingPlace! >= 10 ?
                'text-5xl' :
                'text-6xl'} 
            ${open_sans.className} font-black`}>
            {rankingPlace}
        </p>

    const authorDetailsComponent =
        <div>
            <Avatar avatar={author.avatar} avatarScale={authorAvatarScale}
                    formattedScore={author.scoring.formattedScore}
                    scoreColor={innerLinearInterpolateScoreColor(author.scoring.score)}/>
            <p className={`text-2xl ${open_sans.className} font-semibold text-white text-center mt-3 mb-0.5`}>
                {author.name}
            </p>
            <p className={`text-lg ${open_sans.className} font-bold text-white text-center`}>
                <span className="font-normal mr-1">{sequence} de {sequenceOutOf}</span> {' '}
                <span className="px-1 font-bold border-2 border-white rounded">
                    {sequenceOutOf - sequence + 1}º
                </span>

            </p>
        </div>

    const avgScorePillComponent =
        <div className="flex flex-col justify-center items-center p-5 bg-white rounded-[2em]">
            <p className={`text-7xl text-center ${open_sans.className} font-bold`}>
                {formattedAvgScore}
            </p>
            <p className={`text-2xl text-center ${open_sans.className} font-thin`}>
                (+{formattedAvgScoreDelta})
            </p>
        </div>

    const tieBadge = <p className="size-fit mt-0.5 text-xl font-semibold py-0.5 px-1 bg-white rounded">EMPATE</p>

    const contestantsDisplayComponent =
        <>
            {lowestScoreGroup.map((contestant, i) =>
                <div key={`lowest-${i}`} className="z-10 flex flex-col justify-center items-center">
                    <Avatar
                        key={`lowest-${i}-avatar`}
                        avatar={contestant.avatar}
                        avatarScale={avatarScale}
                        formattedScore={contestant.scoring.formattedScore}
                        scoreColor={innerLinearInterpolateScoreColor(contestant.scoring.score)}/>
                    {lowestScoreGroup.length > 1 && tieBadge}
                </div>
            )}
            {middleScoreGroup.map((contestant, i) =>
                <Avatar
                    key={`sorted-${i}`}
                    avatar={contestant.avatar}
                    avatarScale={avatarScale}
                    formattedScore={contestant.scoring.formattedScore}
                    scoreColor={innerLinearInterpolateScoreColor(contestant.scoring.score)}/>
            )}
            {highestScoreGroup.map((contestant, i) =>
                <div key={`highest-${i}`} className="z-10 flex flex-col justify-center items-center">
                    <Avatar
                        key={`highest-${i}-avatar`}
                        avatar={contestant.avatar}
                        avatarScale={avatarScale}
                        formattedScore={contestant.scoring.formattedScore}
                        scoreColor={innerLinearInterpolateScoreColor(contestant.scoring.score)}/>
                    {highestScoreGroup.length > 1 && tieBadge}
                </div>
            )}
        </>

    return (
        <div className="grid grid-cols-[1fr_2fr] grid-rows-[4fr_2fr] size-full bg-black p-7 overflow-clip">
            <div className="row-start-1 row-end-2 col-start-1 col-end-2 h-full">
                <div className="flex flex-col h-full justify-between">
                    <div className="flex flex-col items-end">
                        <div className="grid grid-cols-[1fr_4fr] grid-rows-[auto_auto] gap-x-4 gap-y-4
                            justify-stretch content-start w-full">
                            <div className="row-start-1 row-end-3 col-start-1 col-end-2 size-full
                                 flex justify-center items-center
                                 bg-white rounded-tl-[2rem] rounded-bl-[2rem]">
                                {rankingPlaceComponent}
                            </div>
                            <div className="row-start-1 row-end-2 col-start-2 col-end-2 size-full
                                 flex justify-center items-center
                                 bg-white rounded-tr-[2rem]">
                                <p className={`text-3xl text-center p-2 ${open_sans.className}`}>
                                    {songTitle}
                                </p>
                            </div>
                            <div className="row-start-2 row-end-3 col-start-2 col-end-2 size-full
                                 flex justify-center items-center
                                 bg-white rounded-br-[2rem]">
                                <p className={`text-2xl text-center p-2 ${open_sans.className} font-thin`}>
                                    {workTitle}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className="flex h-full justify-around items-center">
                        {authorDetailsComponent}
                        {avgScorePillComponent}
                    </div>
                </div>
            </div>
            <div className="row-start-1 row-end-2 col-start-2 col-end-3 justify-self-end self-start">
                <VideoPlaceholder widthPx={videoBoxWidthPx} heightPx={videoBoxHeightPx}/>
            </div>
            <div className="row-start-2 row-end-3 col-start-1 col-end-3">
                <div className="h-full flex flex-row justify-evenly items-start mt-10">
                    {contestantsDisplayComponent}
                </div>
            </div>
        </div>
    )
}

function getTitleBits(title: string): [string, string] {
    const [songTitle, workTitle] = title.split(' - ').map(s => s.trim())
    return [songTitle, workTitle]
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