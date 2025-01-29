'use client'

import React, { ChangeEvent, ChangeEventHandler, HTMLInputTypeAttribute, useState } from 'react'

import formatNumberToDecimalPrecision from '@/formatters/formatNumberToDecimalPrecision'

import { defaultEntry, defaultEntryStats, defaultScoring, defaultTemplate } from '@/db/defaults'
import { Contestant } from '@/db/schema'
import BaseTemplateContainer from '@/app/templates/components/TemplateContainer/BaseTemplateContainer'
import { defaultEditionProps } from '@/app/templates/components/Template/5th-edition/defaults'
import { Template, TemplateProps } from '@/app/templates/components/Template/5th-edition/Template'
import { ResolvedAvatar, ResolvedScoring } from '@/app/templates/common/withTemplateProps'

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
                   className="px-2 py-1 text-md font-light outline-none rounded border-b-2 border-solid border-black
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

    const avatars: Partial<ResolvedAvatar>[] = [
        {
            id: 1,
            resolvedImageFilename: 'mock/Ana.png',
            imageHeight: 482,
        }, {
            id: 2,
            resolvedImageFilename: 'mock/Arancha.png',
            imageHeight: 399,
        }, {
            id: 3,
            resolvedImageFilename: 'mock/Bea.png',
            imageHeight: 390,
        }, {
            id: 4,
            resolvedImageFilename: 'mock/Carmen.png',
            imageHeight: 398,
        }, {
            id: 5,
            resolvedImageFilename: 'mock/Caster.png',
            imageHeight: 432,
        }, {
            id: 6,
            resolvedImageFilename: 'mock/Celia.png',
            imageHeight: 394,
        }, {
            id: 7,
            resolvedImageFilename: 'mock/Jorge.png',
            imageHeight: 404,
        }, {
            id: 8,
            resolvedImageFilename: 'mock/Jose.png',
            imageHeight: 380,
        }, {
            id: 9,
            resolvedImageFilename: 'mock/Laura.png',
            imageHeight: 401,
        }, {
            id: 10,
            resolvedImageFilename: 'mock/Pablo.png',
            imageHeight: 522,
        }
    ]

    const contestants: Contestant[] = [
        { id: 'Ana', name: 'Ana', avatar: 1 },
        { id: 'Arancha', name: 'Arancha', avatar: 2 },
        { id: 'Bea', name: 'Arancha', avatar: 3 },
        { id: 'Carmen', name: 'Carmen', avatar: 4 },
        { id: 'Cáster', name: 'Cáster', avatar: 5 },
        { id: 'Celia', name: 'Celia', avatar: 6 },
        { id: 'Jorge', name: 'Sara', avatar: 7 },
        { id: 'Jose', name: 'Jose', avatar: 8 },
        { id: 'Laura', name: 'Laura', avatar: 9 },
        { id: 'Pablo', name: 'Pablo', avatar: 10 },
    ]

    const defaultAuthor = contestants[0]

    const [contestantCount, setContestantCount] = useState<number>(INITIAL_CONTESTANT_COUNT)
    const [title, setTitle] = useState<string>(defaultEntry.title)
    const [specialTopic, setSpecialTopic] = useState<string>(defaultEntry.specialTopic!)
    const [rankingPlace, setRankingPlace] = useState<number>(defaultEntryStats.rankingPlace!)
    const [authorName, setAuthorName] = useState<string>(defaultAuthor.name)
    const [avgScore, setAvgScore] = useState<number>(defaultEntryStats.avgScore!)
    const [score, setScore] = useState<number>(defaultScoring.score)
    const [avatarScale, setAvatarScale] = useState<number>(defaultTemplate.avatarScale)
    const [authorAvatarScale, setAuthorAvatarScale] = useState<number>(defaultTemplate.authorAvatarScale)
    const [videoBoxWidthPx, setVideoBoxWidthPx] = useState<number>(defaultTemplate.videoBoxWidthPx)
    const [videoBoxHeightPx, setVideoBoxHeightPx] = useState<number>(defaultTemplate.videoBoxHeightPx)
    const [SNSTEntries, setSNSTEntries] = useState<number>(defaultEditionProps.sequenceNumberInSpecialTopic![0])
    const [SNSTEntriesOutOf, setSNSTEntriesOutOf] = useState<number>(defaultEditionProps.sequenceNumberInSpecialTopic![1])

    const scores = contestants.map<Partial<ResolvedScoring>>(c => {
        return ({
            contestant: c.id,
            score,
            formattedScore: formatNumberToDecimalPrecision(score, displayDecimalDigits)
        })
    })

    const templateProps: TemplateProps = {
        title,
        specialTopic,
        rankingPlace,
        formattedAvgScore: formatNumberToDecimalPrecision(avgScore, displayDecimalDigits),
        avatarScale,
        authorAvatarScale,
        videoBoxWidthPx,
        videoBoxHeightPx,
        author: contestants.find(c => c.name === authorName) ?? defaultAuthor,
        contestants: contestants.filter(c => c.name !== authorName),
        avatars: avatars as ResolvedAvatar[],
        scores: scores as ResolvedScoring[],
        sequenceNumberInSpecialTopic: [SNSTEntries, SNSTEntriesOutOf],
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
        inputFactory('author-name', 'Author name', authorName, 'text', "Author's name ...",
            onChangeFactory(v => setAuthorName(v))),
        inputFactory('snst-entries', 'Special topic ranking (Lower bound)', SNSTEntries, 'number', 'Lower bound ...',
            onChangeFactory(v => setSNSTEntries(parseInt(v)))),
        inputFactory('snst-entries-out-of', 'Special topic ranking (Upper bound)', SNSTEntriesOutOf, 'number', 'Upper bound ...',
            onChangeFactory(v => setSNSTEntriesOutOf(parseInt(v)))),
        inputFactory('avg-score', 'Avg. score', avgScore, 'number', 'Average score ...',
            onChangeFactory(v => setAvgScore(v ? parseFloat(v) : 0))),
        inputFactory('scores', 'Scores', score, 'number', 'Score of all contestants ...',
            onChangeFactory(v => setScore(v ? parseFloat(v) : 0))),
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