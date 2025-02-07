'use client'

import React, { ChangeEvent, ChangeEventHandler, HTMLInputTypeAttribute, useState } from 'react'

import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'

import { defaultEntry, defaultEntryStats, defaultScoring, defaultTemplate } from '@/db/defaults'
import {
    defaultResolvedAuthor,
    defaultResolvedContestant,
    defaultResolvedScoring
} from '@/app/templates/common/withTemplateProps/defaults'
import BaseTemplateContainer from '@/app/templates/components/TemplateContainer/BaseTemplateContainer'
import { Template, TemplateProps } from '@/app/templates/components/Template'

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
    onChange: ChangeEventHandler<HTMLInputElement>): React.JSX.Element {

    return (
        <div key={id} className="flex flex-col-reverse h-fit">
            <input id={id}
                   className="w-44 px-2 py-1 text-md font-light outline-none rounded border-b-2 border-solid border-black
                            placeholder:text-zinc-400 placeholder:italic placeholder:font-normal
                            focus:border-purple-500 focus:bg-purple-50 peer"
                   type={inputType} value={value} placeholder={`${placeholder}`}
                   onChange={onChange}/>
            <label htmlFor={id} className="mr-3 pl-1 text-sm font-bold select-none peer-focus:text-purple-500">
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
    const INITIAL_CONTESTANT_COUNT = 5

    const [contestantCount, setContestantCount] = useState<number>(INITIAL_CONTESTANT_COUNT)
    const [score, setScore] = useState<number>(defaultScoring.score)
    const [title, setTitle] = useState<string>(defaultEntry.title)
    const [specialTopic, setSpecialTopic] = useState<string>(defaultEntry.specialTopic!)
    const [rankingPlace, setRankingPlace] = useState<number>(defaultEntryStats.rankingPlace!)
    const [avgScore, setAvgScore] = useState<number>(defaultEntryStats.avgScore!)
    const [avatarScale, setAvatarScale] = useState<number>(defaultTemplate.avatarScale)
    const [authorAvatarScale, setAuthorAvatarScale] = useState<number>(defaultTemplate.authorAvatarScale)
    const [videoBoxWidthPx, setVideoBoxWidthPx] = useState<number>(defaultTemplate.videoBoxWidthPx)
    const [videoBoxHeightPx, setVideoBoxHeightPx] = useState<number>(defaultTemplate.videoBoxHeightPx)

    const templateProps: TemplateProps = {
        title,
        specialTopic,
        rankingPlace,
        formattedAvgScore: formatNumberToDecimalPrecision(avgScore, displayDecimalDigits),
        avatarScale,
        authorAvatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        author: {
            ...defaultResolvedAuthor,
            scoring: {
                ...defaultResolvedScoring,
                score,
                formattedScore: formatNumberToDecimalPrecision(score, displayDecimalDigits)
            }
        },
        contestants: Array.from({ length: contestantCount - 1 }, () => ({
            ...defaultResolvedContestant,
            scoring: {
                ...defaultResolvedScoring,
                score,
                formattedScore: formatNumberToDecimalPrecision(score, displayDecimalDigits)
            }
        }))
    }

    const templateParamInputs = [
        inputFactory('contestant-count', 'Contestant count', contestantCount, 'number', 'Including the author ...',
            onChangeFactory(v => setContestantCount(parseInt(v)))),
        inputFactory('title', 'Entry title', title, 'text', 'Entry title ...',
            onChangeFactory(v => setTitle(v))),
        inputFactory('special-topic', 'Special entry topic', specialTopic, 'text', 'Entry topic ...',
            onChangeFactory(v => setSpecialTopic(v))),
        inputFactory('ranking-place', 'Ranking place', rankingPlace, 'number', 'Numeric ranking place ...',
            onChangeFactory(v => setRankingPlace(parseInt(v)))),
        inputFactory('avg-score', 'Avg score', avgScore, 'number', 'Average score ...',
            onChangeFactory(v => setAvgScore(parseFloat(v)))),
        inputFactory('scores', 'Scores', score, 'number', 'Score of all contestants ...',
            onChangeFactory(v => setScore(parseFloat(v)))),
        inputFactory('avatar-scale', 'Avatar scale', avatarScale, 'number', 'Avatar scale factor ...',
            onChangeFactory(v => setAvatarScale(parseFloat(v)))),
        inputFactory('author-avatar-scale', 'Author avatar scale', authorAvatarScale, 'number', 'Author avatar scale factor ...',
            onChangeFactory(v => setAuthorAvatarScale(parseFloat(v)))),
        inputFactory('video-box-width', 'Video width', videoBoxWidthPx, 'number', 'Video box width (px) ...',
            onChangeFactory(v => setVideoBoxWidthPx(parseInt(v)))),
        inputFactory('video-box-height', 'Video height', videoBoxHeightPx, 'number', 'Video box height (px) ...',
            onChangeFactory(v => setVideoBoxHeightPx(parseInt(v))))
    ]

    return (
        <>
            <BaseTemplateContainer width={templateWidth} height={templateHeight}>
                <Template {...templateProps} />
            </BaseTemplateContainer>
            <div className="flex items-center mt-7 select-none" style={{ width: templateWidth }}>
                <div className="flex flex-col justify-center mx-5 h-fit select-none">
                    <h1 className="text-2xl font-bold select-none">CONTROLS</h1>
                    <h2 className="text-sm select-none self-center">TEMPLATE EDITOR</h2>
                </div>
                <div className="flex flex-wrap justify-around w-full select-none">
                    {templateParamInputs}
                </div>
            </div>
        </>
    )
}