'use client'

import React, { ChangeEvent, ChangeEventHandler, HTMLInputTypeAttribute, useState } from 'react'

import { BaseFrameContainer } from '@/app/components/FrameContainer/BaseFrameContainer'
import { ResolvedScoring } from '@/app/templates/common/withTemplateProps'
import {
    defaultAvgScoreDelta,
    defaultResolvedAuthor,
    defaultSequenceNumberInAuthorEntries,
    defaultSequenceNumberInTopic,
    defaultTemplateSettingsProps,
} from '@/app/templates/common/withTemplateProps/defaults'
import Template, { TemplateProps } from '@/app/templates/components/Template/Template'
import { defaultAuthor, defaultEntry, defaultEntryStats, defaultScoring, defaultTemplate } from '@/db/defaults'
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
    placeholder: string | number,
    onChange: ChangeEventHandler<HTMLInputElement>
): React.JSX.Element {
    return (
        <div
            key={id}
            className='flex flex-col-reverse h-fit'
        >
            <input
                id={id}
                className='px-2 py-1 text-md font-light outline-none rounded border-b-2 border-solid border-black
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
    const INITIAL_CONTESTANT_COUNT = 7

    const [contestantCount, setContestantCount] = useState<number>(INITIAL_CONTESTANT_COUNT)
    const [title, setTitle] = useState<string>(defaultEntry.title)
    const [topic, setTopic] = useState<string>(defaultEntry.topic!)
    const [rankingPlace, setRankingPlace] = useState<number>(defaultEntryStats.rankingPlace!)
    const [authorName, setAuthorName] = useState<string>(defaultAuthor.name)
    const [avgScore, setAvgScore] = useState<number>(defaultEntryStats.avgScore!)
    const [defaultScore, setDefaultScore] = useState<number>(defaultScoring.score)
    const [scoresString, setScoresString] = useState<string>(defaultScoring.score.toString())
    const [scores, setScores] = useState<{ [key: string]: number }>({})
    const [avatarScale, setAvatarScale] = useState<number>(defaultTemplate.avatarScale)
    const [authorAvatarScale, setAuthorAvatarScale] = useState<number>(defaultTemplate.authorAvatarScale)
    const [videoBoxWidthPx, setVideoBoxWidthPx] = useState<number>(defaultTemplate.videoBoxWidthPx)
    const [videoBoxHeightPx, setVideoBoxHeightPx] = useState<number>(defaultTemplate.videoBoxHeightPx)
    const [SNAEntries, setSNAEntries] = useState<number>(defaultSequenceNumberInAuthorEntries[0])
    const [SNAEntriesOutOf, setSNAEntriesOutOf] = useState<number>(defaultSequenceNumberInAuthorEntries[1])
    const [SNTEntries, setSNTEntries] = useState<number>(defaultSequenceNumberInTopic![0])
    const [SNTEntriesOutOf, setSNTEntriesOutOf] = useState<number>(defaultSequenceNumberInTopic![1])
    const [avgScoreDelta, setAvgScoreDelta] = useState<number>(defaultAvgScoreDelta)

    const resolvedScoreForContestant = (contestant: string): ResolvedScoring => {
        const score = scores[contestant] ?? defaultScore
        return {
            score: score,
            formattedScore: formatNumberToDecimalPrecision(score, displayDecimalDigits),
        }
    }

    const avatarDefaults = {
        scoreBoxPositionTop: 14,
        scoreBoxPositionLeft: 45,
        scoreBoxFontScale: 0.15,
        scoreBoxFontColor: 'black',
    }

    const contestants = [
        {
            id: 'Ana',
            name: 'Ana',
            avatar: {
                ...avatarDefaults,
                id: 1,
                resolvedImageFilename: 'ANA MINI.png',
                imageHeight: 836,
            },
            scoring: resolvedScoreForContestant('Ana'),
        },
        {
            id: 'Carmen',
            name: 'Carmen',
            avatar: {
                ...avatarDefaults,
                id: 2,
                resolvedImageFilename: 'CARMEN MINI.png',
                imageHeight: 845,
            },
            scoring: resolvedScoreForContestant('Carmen'),
        },
        {
            id: 'Caster',
            name: 'Cáster',
            avatar: {
                ...avatarDefaults,
                id: 3,
                resolvedImageFilename: 'CASTER MINI.png',
                imageHeight: 874,
            },
            scoring: resolvedScoreForContestant('Caster'),
        },
        {
            id: 'Jorge',
            name: 'Jorge',
            avatar: {
                ...avatarDefaults,
                id: 4,
                resolvedImageFilename: 'JORGE MINI.png',
                imageHeight: 841,
            },
            scoring: resolvedScoreForContestant('Jorge'),
        },
        {
            id: 'Jose',
            name: 'José',
            avatar: {
                ...avatarDefaults,
                id: 5,
                resolvedImageFilename: 'JOSE MINI.png',
                imageHeight: 832,
            },
            scoring: resolvedScoreForContestant('Jose'),
        },
        {
            id: 'Pablo',
            name: 'Pablo',
            avatar: {
                ...avatarDefaults,
                id: 6,
                resolvedImageFilename: 'PABLO MINI.png',
                imageHeight: 836,
            },
            scoring: resolvedScoreForContestant('Pablo'),
        },
        {
            id: 'Sergio',
            name: 'Pichoncito',
            avatar: {
                ...avatarDefaults,
                id: 7,
                resolvedImageFilename: 'SERGIO MINI.png',
                imageHeight: 837,
            },
            scoring: resolvedScoreForContestant('Sergio'),
        },
    ]

    const templateProps: TemplateProps = {
        title,
        topic,
        rankingPlace,
        formattedAvgScore: formatNumberToDecimalPrecision(avgScore, displayDecimalDigits),
        avgScoreDelta,
        avatarScale,
        authorAvatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        author: contestants.find((c) => c.name === authorName) ?? defaultResolvedAuthor,
        sequenceNumberInAuthorEntries: [SNAEntries, SNAEntriesOutOf],
        sequenceNumberInTopic: SNTEntries && SNTEntriesOutOf ? [SNTEntries, SNTEntriesOutOf] : undefined,
        contestants: contestants.filter((c) => c.name !== authorName),
        scoreMinValue: defaultTemplateSettingsProps.scoreMinValue,
        scoreMaxValue: defaultTemplateSettingsProps.scoreMaxValue,
    }

    const templateParamInputs = [
        inputFactory(
            'contestant-count',
            'Contestant count',
            contestantCount,
            'number',
            'Including the author ...',
            onChangeFactory((v) => setContestantCount(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'title',
            'Entry title',
            title,
            'text',
            'Entry title ...',
            onChangeFactory((v) => setTitle(v))
        ),
        inputFactory(
            'entry-topic',
            'Entry topic',
            topic,
            'text',
            'Entry topic ...',
            onChangeFactory((v) => setTopic(v))
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
            'author-name',
            'Author name',
            authorName,
            'text',
            "Author's name ...",
            onChangeFactory((v) => setAuthorName(v))
        ),
        inputFactory(
            'sna-entries',
            'Personal ranking (Lower bound)',
            SNAEntries,
            'number',
            'Lower bound ...',
            onChangeFactory((v) => setSNAEntries(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'sna-entries-out-of',
            'Personal ranking (Upper bound)',
            SNAEntriesOutOf,
            'number',
            'Upper bound ...',
            onChangeFactory((v) => setSNAEntriesOutOf(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'snt-entries',
            'Topic ranking (Lower bound)',
            SNTEntries,
            'number',
            'Lower bound ...',
            onChangeFactory((v) => setSNTEntries(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'snt-entries-out-of',
            'Topic ranking (Upper bound)',
            SNTEntriesOutOf,
            'number',
            'Upper bound ...',
            onChangeFactory((v) => setSNTEntriesOutOf(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'avg-score',
            'Avg. score',
            avgScore,
            'number',
            'Average score ...',
            onChangeFactory((v) => setAvgScore(v ? parseFloat(v) : 0))
        ),
        inputFactory(
            'avg-score-delta',
            'Avg. score delta',
            avgScoreDelta,
            'number',
            'Average score delta ...',
            onChangeFactory((v) => setAvgScoreDelta(v ? parseFloat(v) : 0))
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
            'author-avatar-scale',
            'Author avatar scale',
            authorAvatarScale,
            'number',
            'Author avatar scale factor ...',
            onChangeFactory((v) => setAuthorAvatarScale(v ? parseFloat(v) : 0))
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
