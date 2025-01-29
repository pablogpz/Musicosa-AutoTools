import { Montserrat } from 'next/font/google'

import { ResolvedAvatar, ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import { defaultResolvedAvatar } from '@/app/templates/common/withTemplateProps/defaults'
import Avatar from '@/app/templates/components/Avatar'
import VideoPlaceholder from '@/app/templates/components/VideoPlaceholder'

import {
    authorScoreBoxBgColors,
    contestantScoreGaugeGradients,
    entryScoreBoxBgColorGradients,
    scoreBoxFontColors,
    specialTopicDenominations,
    templateBgColorGradients
} from './constants'

export interface EditionProps {
    sequenceNumberInSpecialTopic: [number, number] | undefined,
}

export type TemplateProps = ResolvedTemplateProps & EditionProps

const montserrat = Montserrat({
    subsets: ['latin'],
    display: 'swap',
    variable: '--font-montserrat'
})

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
        sequenceNumberInSpecialTopic
    }: TemplateProps) {

    const authorAvatar =
        avatars.find(avatar => avatar.id === author.avatar) ?? defaultResolvedAvatar
    const authorFormattedName = author.name.toUpperCase()
    const authorFormattedScore =
        scores.find(score => score.contestant === author.id)!.formattedScore
    const authorScoreBoxBgColor = authorScoreBoxBgColorFactory(specialTopic)

    const maxAvatarHeight = avatars
        .toSorted((a, b) => b.imageHeight - a.imageHeight)!
        .at(0)!.imageHeight
    const targetAvatarHeight = avatars
        .toSorted((a, b) => b.imageHeight - a.imageHeight)!
        .at(1)!.imageHeight
    // Make Pablo's avatar 20% larger than the target
    const avatarHeightRule = (avatar: ResolvedAvatar): number => {
        const pabloAvatarId = 10
        const upscaleFactor = 1.20

        return avatar.id === pabloAvatarId ?
            targetAvatarHeight * upscaleFactor :
            targetAvatarHeight
    }

    const randomizedContestantScores = scores
        .filter(scoring => scoring.contestant !== author.id)
        .sort(() => Math.random() - 0.5)
    const sortedContestants = randomizedContestantScores.map(
        scoring => contestants.find(
            contestant => scoring.contestant === contestant.id))

    let specialTopicSequence, specialTopicSequenceOutOf
    if (specialTopic && sequenceNumberInSpecialTopic)
        [specialTopicSequence, specialTopicSequenceOutOf] = sequenceNumberInSpecialTopic

    const scoreBoxFontColor = scoreBoxFontColorFactory(specialTopic)

    const musicosaBannerComponent =
        <p className={`text-2xl font-medium text-white mb-8`}>MUSICOSA 5º EDICIÓN CANCIONES</p>

    const entryInfoComponent =
        <div className="flex flex-row items-center">
            <p className="font-bold text-8xl mr-4">{rankingPlace}</p>
            <div>
                <p className="font-normal text-4xl mb-2">{title}</p>
                <p className="font-normal text-3xl">{authorFormattedName}</p>
            </div>
        </div>

    const villancicosDecorationsComponent = specialTopic === specialTopicDenominations.villancicos &&
        <>
            <img src="/misc/acebo.png" className="absolute translate-x-[-50%] translate-y-[-50%]"
                 style={{ height: '200px', top: '-20%', left: '55%' }}/>
            <img src="/misc/baston-caramelo.png"
                 className="absolute translate-x-[-50%] translate-y-[-50%] rotate-12"
                 style={{ height: '100px', top: '65%', left: '45%' }}/>
        </>

    const authorDisplayComponent =
        <div>
            <div className="flex flex-row h-full ml-7">
                <div className="relative inline-block">
                    <div className="relative z-20">
                        <Avatar avatar={{ ...authorAvatar, imageHeight: maxAvatarHeight }}
                                avatarScale={authorAvatarScale}/>
                    </div>
                    <div className="absolute translate-y-[-50%] h-full w-1/2 z-10"
                         style={{
                             left: '50%',
                             top: '50%',
                             background: `linear-gradient(180deg,
                                  transparent 10%,
                                   ${authorScoreBoxBgColor.background} 10%,
                                    ${authorScoreBoxBgColor.background} 75%,
                                     transparent 75%)`
                         }}/>
                </div>
                <div className="relative inline-block z-10">
                    <div
                        className="flex items-center h-[66%] translate-y-[14%] px-7 font-medium text-4xl"
                        style={{ ...authorScoreBoxBgColor, ...scoreBoxFontColor }}>
                        {authorFormattedScore}
                    </div>
                </div>
            </div>
        </div>

    const specialTopicComponent = specialTopic &&
        <>
            <p className={`text-xl font-semibold mb-1`}>RONDA {specialTopic.toUpperCase()}</p>
            <p className={`text-xl font-semibold mb-2`}>
                {specialTopicSequenceOutOf! - specialTopicSequence! + 1}º
            </p>
        </>

    const entryResultsComponent =
        <div className="relative z-30">
            <div className="flex flex-col justify-center items-center w-1/2 h-32 mt-[-1em] text-white"
                 style={{ ...entryScoreBoxBgColorFactory(specialTopic) }}>
                {specialTopicComponent}
                <p className={`${specialTopic ? 'text-4xl' : 'text-7xl'} font-light`}>
                    {formattedAvgScore}
                </p>
            </div>
            {villancicosDecorationsComponent}
        </div>

    const infanciaDecorationComponent = specialTopic === specialTopicDenominations.infancia &&
        <img src="/misc/dinosaurio.png" className="absolute translate-x-[-50%] translate-y-[-50%] z-0"
             style={{ height: '70%', top: '50%', left: '30%' }}/>

    const scoreGaugeFactory =
        (avatar: ResolvedAvatar, score: number, formattedScore: string, orderIndex: number) => {
            const gaugeVariant =
                specialTopic === specialTopicDenominations.infancia ? contestantScoreGaugeGradients.infancia :
                    specialTopic === specialTopicDenominations.villancicos ? contestantScoreGaugeGradients.villancicos :
                        contestantScoreGaugeGradients.regular

            const backgroundStyle = {
                background: `linear-gradient(90deg, 
                                ${gaugeVariant[orderIndex % gaugeVariant.length].start},
                                ${gaugeVariant[orderIndex % gaugeVariant.length].stop})`
            }

            /* Quadratic scaling of score */
            const scoreToHeight = (score: number) => (score > 2 ? Math.pow(score, 2) : 20)

            return (
                <div className="flex flex-col justify-end h-[97%]" key={orderIndex}>
                    <div className="relative z-10 flex flex-col justify-end h-full">
                        <div className={`flex flex-row justify-center min-h-14 py-2 font-medium text-4xl`}
                             style={{ height: `${scoreToHeight(score)}%`, ...backgroundStyle, ...scoreBoxFontColor }}>
                            <p>{formattedScore}</p>
                        </div>
                    </div>
                    <div className="relative inline-block">
                        <div className="relative z-20 px-4 mb-[-0.5em]">
                            <Avatar avatar={{ ...avatar, imageHeight: avatarHeightRule(avatar) }}
                                    avatarScale={avatarScale}/>
                        </div>
                        <div className="absolute translate-y-[-100%] size-full z-10" style={{ ...backgroundStyle }}/>
                    </div>
                </div>
            )
        }

    return (
        <div className={`grid size-full overflow-clip ${montserrat.className}`}
             style={{
                 gridTemplateRows: `${videoBoxHeightPx}px auto`,
                 gridTemplateColumns: `auto ${videoBoxWidthPx}px`,
                 ...(templateBgColorFactory(specialTopic))
             }}>
            <div className="col-start-1 col-end-2 row-start-1 row-end-2">
                <div className="flex flex-col size-full justify-around">
                    <div className="flex flex-col ml-10 text-white">
                        {musicosaBannerComponent}
                        {entryInfoComponent}
                    </div>
                    <div>
                        {authorDisplayComponent}
                        {entryResultsComponent}
                    </div>
                </div>
            </div>
            <div className="col-start-2 col-end-3 row-start-1 row-end-2 justify-self-end">
                <VideoPlaceholder widthPx={videoBoxWidthPx} heightPx={videoBoxHeightPx}/>
            </div>
            <div className="col-start-1 col-end-3 row-start-2 row-end-3">
                <div className="flex flex-row size-full justify-evenly items-end">
                    {randomizedContestantScores.map((scoring, i) =>
                        scoreGaugeFactory(
                            avatars.find(avatar => sortedContestants[i]?.avatar === avatar.id) ?? defaultResolvedAvatar,
                            scoring.score,
                            scoring.formattedScore,
                            i)
                    )}
                </div>
            </div>
            {infanciaDecorationComponent}
        </div>
    )
}

function templateBgColorFactory(specialTopic: string | undefined | null): { background: string } {
    switch (specialTopic) {
        case specialTopicDenominations.infancia:
            return {
                background: `linear-gradient(
            ${templateBgColorGradients.infancia.angle}deg,
             ${templateBgColorGradients.infancia.start},
              ${templateBgColorGradients.infancia.stop})`
            }
        case specialTopicDenominations.villancicos:
            return {
                background: `linear-gradient(
            ${templateBgColorGradients.villancicos.angle}deg,
             ${templateBgColorGradients.villancicos.start},
              ${templateBgColorGradients.villancicos.stop})`
            }
    }

    return {
        background: `linear-gradient(
            ${templateBgColorGradients.regular.angle}deg,
             ${templateBgColorGradients.regular.start},
              ${templateBgColorGradients.regular.stop})`
    }
}

function authorScoreBoxBgColorFactory(specialTopic: string | undefined | null): { background: string } {
    switch (specialTopic) {
        case specialTopicDenominations.infancia:
            return { background: authorScoreBoxBgColors.infancia }
        case specialTopicDenominations.villancicos:
            return { background: authorScoreBoxBgColors.villancicos }
    }

    return { background: authorScoreBoxBgColors.regular }
}

function entryScoreBoxBgColorFactory(specialTopic: string | undefined | null): { background: string } {
    switch (specialTopic) {
        case specialTopicDenominations.infancia:
            return {
                background: `linear-gradient(
            ${entryScoreBoxBgColorGradients.infancia.angle}deg,
             ${entryScoreBoxBgColorGradients.infancia.start},
              ${entryScoreBoxBgColorGradients.infancia.stop})`
            }
        case specialTopicDenominations.villancicos:
            return {
                background: `linear-gradient(
            ${entryScoreBoxBgColorGradients.villancicos.angle}deg,
             ${entryScoreBoxBgColorGradients.villancicos.start},
              ${entryScoreBoxBgColorGradients.villancicos.stop})`
            }
    }

    return {
        background: `linear-gradient(
            ${entryScoreBoxBgColorGradients.regular.angle}deg,
             ${entryScoreBoxBgColorGradients.regular.start},
              ${entryScoreBoxBgColorGradients.regular.stop})`
    }
}

function scoreBoxFontColorFactory(specialTopic: string | undefined | null): { color: string } {
    switch (specialTopic) {
        case specialTopicDenominations.infancia:
            return { color: scoreBoxFontColors.infancia }
        case specialTopicDenominations.villancicos:
            return { color: scoreBoxFontColors.villancicos }
    }

    return { color: scoreBoxFontColors.regular }
}