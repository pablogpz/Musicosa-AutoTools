'use client'

import React, { ChangeEvent, ChangeEventHandler, HTMLInputTypeAttribute, useState } from 'react'

import { BaseFrameContainer } from '@/app/components/FrameContainer/BaseFrameContainer'
import { ResolvedCastVote, ResolvedMember } from '@/app/templates/common/withTemplateProps'
import Template, { TemplateProps } from '@/app/templates/components/Template/Template'
import {
    defaultAward,
    defaultCastVote,
    defaultNomination,
    defaultNominationStats,
    defaultTemplate,
} from '@/db/defaults'
import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'

function onChangeFactory(onChange: (value: string) => void): ChangeEventHandler<HTMLInputElement> {
    return (e: ChangeEvent<HTMLInputElement>): void => {
        onChange(e.target.value)
        e.stopPropagation()
    }
}

function inputFactory(
    id: string,
    title: string,
    value: string | number,
    inputType: HTMLInputTypeAttribute,
    placeholder: string | number | undefined,
    onChange: ChangeEventHandler<HTMLInputElement>
): React.JSX.Element {
    return (
        <div
            key={id}
            className='flex flex-col-reverse h-fit'
        >
            <input
                id={id}
                className='w-44 px-2 py-1 text-md font-light outline-none rounded border-b-2 border-solid border-black
                            placeholder:text-zinc-400 placeholder:italic placeholder:font-normal
                            focus:border-purple-500 focus:bg-purple-50 peer'
                type={inputType}
                value={value}
                placeholder={`${placeholder}`}
                onChange={onChange}
            />
            <label
                htmlFor={id}
                className='mr-3 pl-1 text-sm font-bold select-none peer-focus:text-purple-500'
            >
                {title}
            </label>
        </div>
    )
}

export interface TemplateEditorProps {
    templateWidth: number
    templateHeight: number
    displayDecimalDigits: number
}

export default function TemplateEditor({ templateWidth, templateHeight, displayDecimalDigits }: TemplateEditorProps) {
    const INITIAL_MEMBERS_COUNT = 3

    const [membersCount, setMembersCount] = useState<number>(INITIAL_MEMBERS_COUNT)
    const [defaultScore, setDefaultScore] = useState<number>(defaultCastVote.score)
    const [scoresString, setScoresString] = useState<string>(defaultCastVote.score.toString())
    const [scores, setScores] = useState<{ [key: string]: number }>({})
    const [gameTitle, setGameTitle] = useState<string>(defaultNomination.gameTitle)
    const [nominee, setNominee] = useState<string>(defaultNomination.nominee!)
    const [rankingPlace, setRankingPlace] = useState<number>(defaultNominationStats.rankingPlace!)
    const [avgScore, setAvgScore] = useState<number>(defaultNominationStats.avgScore!)
    const [avatarScale, setAvatarScale] = useState<number>(defaultTemplate.avatarScale)
    const [videoBoxWidthPx, setVideoBoxWidthPx] = useState<number>(defaultTemplate.videoBoxWidthPx)
    const [videoBoxHeightPx, setVideoBoxHeightPx] = useState<number>(defaultTemplate.videoBoxHeightPx)
    const [awardSlug, setAwardSlug] = useState<string>(defaultAward.slug)
    const [awardDesignation, setAwardDesignation] = useState<string>(defaultAward.designation)
    const [disableVideoPlaceholder, setDisableVideoPlaceholder] = useState<boolean>(false)

    const resolvedScoreForMember = (member: string): ResolvedCastVote => {
        const score = scores[member] ?? defaultScore
        return {
            score: score,
            formattedScore: formatNumberToDecimalPrecision(score, displayDecimalDigits),
        }
    }

    const members: ResolvedMember[] = [
        {
            id: 'Cáster',
            name: 'Cáster',
            avatar: {
                id: 1,
                resolvedImageFilename: 'Caster.png',
                imageHeight: 1644,
                scoreBoxPositionTop: 16,
                scoreBoxPositionLeft: 79,
                scoreBoxFontScale: 0.175,
                scoreBoxFontColor: 'black',
            },
            vote: resolvedScoreForMember('Cáster'),
        },
        {
            id: 'Ana',
            name: 'Ana',
            avatar: {
                id: 2,
                resolvedImageFilename: 'Ana.png',
                imageHeight: 1607,
                scoreBoxPositionTop: 16,
                scoreBoxPositionLeft: 79.5,
                scoreBoxFontScale: 0.175,
                scoreBoxFontColor: 'black',
            },
            vote: resolvedScoreForMember('Ana'),
        },
        {
            id: 'Pablo',
            name: 'Pablo',
            avatar: {
                id: 3,
                resolvedImageFilename: 'Pablo.png',
                imageHeight: 1646,
                scoreBoxPositionTop: 16,
                scoreBoxPositionLeft: 78,
                scoreBoxFontScale: 0.175,
                scoreBoxFontColor: 'black',
            },
            vote: resolvedScoreForMember('Pablo'),
        },
    ]

    const templateProps: TemplateProps = {
        gameTitle: gameTitle,
        nominee: nominee,
        rankingPlace,
        formattedAvgScore: formatNumberToDecimalPrecision(avgScore, displayDecimalDigits),
        avatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        award: { slug: awardSlug, designation: awardDesignation },
        members,
        disableVideoPlaceholder,
    }

    const templateParamInputs = [
        inputFactory(
            'members-count',
            'Members count',
            membersCount,
            'number',
            'Members count ...',
            onChangeFactory((v) => setMembersCount(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'game-title',
            'Game title',
            gameTitle,
            'text',
            'Nominated game title ...',
            onChangeFactory((v) => setGameTitle(v))
        ),
        inputFactory(
            'nominee',
            'Nominee',
            nominee,
            'text',
            'Nominee ...',
            onChangeFactory((v) => setNominee(v))
        ),
        inputFactory(
            'ranking-place',
            'Ranking place',
            rankingPlace,
            'number',
            'Numeric ranking place ...',
            onChangeFactory((v) => setRankingPlace(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'avg-score',
            'Avg score',
            avgScore,
            'number',
            'Average score ...',
            onChangeFactory((v) => setAvgScore(v ? parseFloat(v) : 0))
        ),
        inputFactory(
            'scores',
            'Scores',
            scoresString,
            'text',
            '[Alice: 9.5, Bob: 8.0, 7.0] or 8.5 ...',
            onChangeFactory((v: string): void => {
                v = v ? v.trim() : ''

                const scorePairs: { [key: string]: number } = {}
                let rawDefaultScore: string | undefined = ''

                const numberRegex = '\\d+[.,]?\\d*?'
                const scorePairRegex = `^.+\\s*:\\s*${numberRegex}$`

                if (v.startsWith('[') && v.endsWith(']')) {
                    const rawScorePairs = v
                        .slice(1, -1)
                        .split(',')
                        .map((x) => x.trim())
                        .filter((x) => !!x)

                    rawScorePairs
                        .filter((x) => !!x.match(scorePairRegex))
                        .forEach((pair) => {
                            const [name, scoreString] = pair.split(':').map((x) => x.trim())
                            scorePairs[name] = parseFloat(scoreString.replace(',', '.'))
                        })

                    rawDefaultScore = !rawScorePairs.at(-1)?.includes(':') ? rawScorePairs.at(-1) : ''
                } else if (!v.startsWith('[') && !v.endsWith(']')) {
                    rawDefaultScore = !!v.match(`^${numberRegex}$`) ? v : ''
                }

                setScoresString(v)
                setScores(scorePairs)
                setDefaultScore(rawDefaultScore ? parseFloat(rawDefaultScore.replace(',', '.')) : 0)
            })
        ),
        inputFactory(
            'avatar-scale',
            'Avatar scale',
            avatarScale,
            'number',
            'Avatar scale factor ...',
            onChangeFactory((v) => setAvatarScale(v ? parseFloat(v) : 0))
        ),
        inputFactory(
            'video-box-width',
            'Video width',
            videoBoxWidthPx,
            'number',
            'Video box width (px) ...',
            onChangeFactory((v) => setVideoBoxWidthPx(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'video-box-height',
            'Video height',
            videoBoxHeightPx,
            'number',
            'Video box height (px) ...',
            onChangeFactory((v) => setVideoBoxHeightPx(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'award-slug',
            'Award slug',
            awardSlug,
            'text',
            'Award slug ...',
            onChangeFactory((v) => setAwardSlug(v))
        ),
        inputFactory(
            'award-designation',
            'Award designation',
            awardDesignation,
            'text',
            'Award designation ...',
            onChangeFactory((v) => setAwardDesignation(v))
        ),
        inputFactory(
            'disable-video-placeholder',
            'Disable video placeholder',
            disableVideoPlaceholder.toString(),
            'checkbox',
            undefined,
            (e) => {
                setDisableVideoPlaceholder(e.target.checked)
                e.stopPropagation()
            }
        ),
    ]

    return (
        <>
            <BaseFrameContainer
                width={templateWidth}
                height={templateHeight}
            >
                <Template {...templateProps} />
            </BaseFrameContainer>
            <div
                className='flex items-center mt-7 select-none'
                style={{ width: templateWidth }}
            >
                <div className='flex flex-col justify-center mx-5 h-fit select-none'>
                    <h1 className='text-2xl font-bold select-none'>CONTROLS</h1>
                    <h2 className='text-sm select-none self-center'>TEMPLATE EDITOR</h2>
                </div>
                <div className='flex flex-wrap justify-around w-full select-none'>{templateParamInputs}</div>
            </div>
        </>
    )
}
