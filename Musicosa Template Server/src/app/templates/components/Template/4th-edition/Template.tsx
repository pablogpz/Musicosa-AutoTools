import React from 'react'

import { Open_Sans } from 'next/font/google'

import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'

import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import { defaultResolvedAvatar } from '@/app/templates/common/withTemplateProps/defaults'
import Avatar from '@/app/templates/components/Avatar'
import VideoPlaceholder from '@/app/templates/components/VideoPlaceholder'
import { Contestant } from '@/db/schema'

export interface EditionProps {
    scoreMinValue: number,
    scoreMaxValue: number,
    sequenceNumberInAuthorEntries: [number, number],
    sequenceNumberInSpecialTopic: [number, number] | undefined,
    avgScoreDelta: number
}

export type TemplateProps = ResolvedTemplateProps & EditionProps

const open_sans = Open_Sans({
    subsets: ['latin'],
    display: 'swap',
    variable: '--font-open-sans'
})

const AvatarContainer = ({ contestant, context, children }: {
    contestant: Contestant,
    context: 'authorSpot' | 'contestantSpot'
} & React.PropsWithChildren) => {
    const customRulesEnabled = contestant.name === 'Cáster'

    const customRules =
        context === 'authorSpot' ? 'mr-[-50px]' :
            context === 'contestantSpot' ? 'mr-[-25px]' :
                ''

    return (
        <div className={`${customRulesEnabled ? customRules : ''} z-10`}>
            {children}
        </div>
    )
}

// Musicosa 4th Edition Template

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
        sequenceNumberInAuthorEntries,
        sequenceNumberInSpecialTopic,
        avgScoreDelta
    }: TemplateProps) {

    const [songTitle, workTitle] = getTitleBits(title)

    const authorScore = scores.find(score => score.contestant === author.id)!.score
    const authorFormattedScore = scores.find(score => score.contestant === author.id)!.formattedScore
    const authorAvatar = avatars.find(avatar => avatar.id === author.avatar) ?? defaultResolvedAvatar
    const [sequence, sequenceOutOf] = sequenceNumberInAuthorEntries

    let specialTopicSequence, specialTopicSequenceOutOf
    if (specialTopic && sequenceNumberInSpecialTopic)
        [specialTopicSequence, specialTopicSequenceOutOf] = sequenceNumberInSpecialTopic

    const formattedAvgScoreDelta = formatNumberToDecimalPrecision(avgScoreDelta, 4)

    const sortedContestantScores = scores
        .filter(scoring => scoring.contestant !== author.id)
        .sort((a, b) => a.score - b.score)
    const lowerScoreGroup = sortedContestantScores
        .splice(0, sortedContestantScores.findLastIndex(scoring => scoring.score === sortedContestantScores[0].score) + 1)
        .sort(() => Math.random() - 0.5)
        .map(scoring => contestants.find(contestant => contestant.id === scoring.contestant))
        .filter(scoring => scoring !== undefined)
    const highestScoreGroup = sortedContestantScores
        .splice(sortedContestantScores.findIndex(scoring => scoring.score === sortedContestantScores.at(-1)?.score))
        .sort(() => Math.random() - 0.5)
        .map(scoring => contestants.find(contestant => contestant.id === scoring.contestant))
        .filter(scoring => scoring !== undefined)
    const sortedContestantsGroup = sortedContestantScores
        .map(scoring => contestants.find(contestant => contestant.id === scoring.contestant))
        .filter(scoring => scoring !== undefined)

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

    const specialTopicPillComponent = specialTopic &&
        <p className={`text-2xl ${open_sans.className} font-thin p-2 mt-4 mr-7 bg-white rounded`}>
            {specialTopic.toUpperCase()} {' '}
            <span className={`${open_sans.className} text-lg font-normal relative bottom-0.5 mr-1`}>
                {specialTopicSequence} de {specialTopicSequenceOutOf} {' '}
            </span>
            <span className="px-1 text-2xl font-semibold border-black border-2 rounded">
                {specialTopicSequenceOutOf! - specialTopicSequence! + 1}º
            </span>
        </p>

    const authorDetailsComponent =
        <div>
            <AvatarContainer contestant={author} context='authorSpot'>
                <Avatar avatar={authorAvatar} avatarScale={authorAvatarScale}
                        formattedScore={authorFormattedScore}
                        scoreColor={innerLinearInterpolateScoreColor(authorScore)}/>
            </AvatarContainer>
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

    const tieBadge = <p className="size-fit mt-1 text-xl font-semibold py-0.5 px-1 bg-white rounded">EMPATE</p>

    const lowestScoreTie = lowerScoreGroup.length > 1
    const lowestScoreContestant = lowerScoreGroup.shift()
    const lowestScoreContestantComponent =
        <>
            <Avatar
                avatar={avatars.find(avatar => lowestScoreContestant?.avatar === avatar.id) ?? defaultResolvedAvatar}
                avatarScale={avatarScale}
                formattedScore={scores.find(score => score.contestant === lowestScoreContestant?.id)!.formattedScore}
                scoreColor={innerLinearInterpolateScoreColor(
                    scores.find(score => score.contestant === lowestScoreContestant?.id)!.score)}/>
            {lowestScoreTie && tieBadge}
        </>
    const contestantsDisplayComponent =
        <>
            {lowerScoreGroup.map((contestant, i) => {
                return <div key={`lowest-${i}`} className="z-10 flex flex-col justify-center items-center">
                    <AvatarContainer key={`lowest-${i}`} contestant={contestant} context='contestantSpot'>
                        <Avatar
                            key={`lowest-${i}`}
                            avatar={avatars.find(avatar => contestant.avatar === avatar.id) ?? defaultResolvedAvatar}
                            avatarScale={avatarScale}
                            formattedScore={scores.find(score => score.contestant === contestant.id)!.formattedScore}
                            scoreColor={innerLinearInterpolateScoreColor(
                                scores.find(score => score.contestant === contestant.id)!.score)}/>
                    </AvatarContainer>
                    {lowestScoreTie && tieBadge}
                </div>
            })}
            {sortedContestantsGroup.map((contestant, i) =>
                <AvatarContainer key={`sorted-${i}`} contestant={contestant} context='contestantSpot'>
                    <Avatar
                        key={`sorted-${i}`}
                        avatar={avatars.find(avatar => contestant.avatar === avatar.id) ?? defaultResolvedAvatar}
                        avatarScale={avatarScale}
                        formattedScore={scores.find(score => score.contestant === contestant.id)!.formattedScore}
                        scoreColor={innerLinearInterpolateScoreColor(
                            scores.find(score => score.contestant === contestant.id)!.score)}/>
                </AvatarContainer>)}
            {highestScoreGroup.map((contestant, i) =>
                <div key={`highest-${i}`} className="z-10 flex flex-col justify-center items-center">
                    <AvatarContainer key={`highest-${i}`} contestant={contestant} context='contestantSpot'>
                        <Avatar
                            key={`highest-${i}`}
                            avatar={avatars.find(avatar => contestant.avatar === avatar.id) ?? defaultResolvedAvatar}
                            avatarScale={avatarScale}
                            formattedScore={scores.find(score => score.contestant === contestant.id)!.formattedScore}
                            scoreColor={innerLinearInterpolateScoreColor(
                                scores.find(score => score.contestant === contestant.id)!.score)}/>
                    </AvatarContainer>
                    {highestScoreGroup.length > 1 && tieBadge}
                </div>)}
        </>

    const shaiHuludSpecialTopicInfancia = <img className="w-full h-auto absolute inline-block"
                                               style={{ width: '1591px', top: '749px', left: '301.5px' }}
                                               src="/Shai_Hulud_INFANCIA.png" alt="Shai Hulud (INFANCIA)"/>

    const shaiHuludRegular = <img className="w-full h-auto absolute inline-block"
                                  style={{ width: '1591px', top: '775px', left: '301.5px' }}
                                  src="/Shai_Hulud.png" alt="Shai Hulud"/>

    const shaiHuludComponent = specialTopic ? shaiHuludSpecialTopicInfancia : shaiHuludRegular

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
                                <p className={`text-3xl text-center p-2 ${open_sans.className}`}>{songTitle}</p>
                            </div>
                            <div className="row-start-2 row-end-3 col-start-2 col-end-2 size-full
                                 flex justify-center items-center
                                 bg-white rounded-br-[2rem]">
                                <p className={`text-2xl text-center p-2 ${open_sans.className} font-thin`}>
                                    {workTitle}
                                </p>
                            </div>
                        </div>
                        {specialTopicPillComponent}
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
                <div className="absolute w-[275px] h-[343px] flex flex-col justify-end items-center">
                    {lowestScoreContestantComponent}
                </div>
                <div className="relative top-3 left-[350px] w-[1225px] flex flex-row justify-between items-start">
                    {contestantsDisplayComponent}
                </div>
                {shaiHuludComponent}
            </div>
        </div>
    )
}

function getTitleBits(title: string): [string, string] {
    const [workTitle, ...songTitle] = title.split('-').map(s => s.trim()).reverse()
    return [songTitle.reverse().join(' - '), workTitle]
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