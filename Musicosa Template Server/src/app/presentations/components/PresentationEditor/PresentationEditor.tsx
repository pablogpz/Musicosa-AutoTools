'use client'

import React, { ChangeEvent, ChangeEventHandler, HTMLInputTypeAttribute, useState } from 'react'

import { BaseFrameContainer } from '@/app/components/FrameContainer/BaseFrameContainer'
import { defaultSequenceNumberInTie } from '@/app/presentations/common/withPresentationProps/defaults'
import Presentation, { PresentationProps } from '@/app/presentations/components/Presentation/Presentation'
import { defaultEntryStats } from '@/db/defaults'

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

export interface PresentationEditorProps {
    width: number
    height: number
}

export default function PresentationEditor({ width, height }: PresentationEditorProps) {
    const [rankingPlace, setRankingPlace] = useState<number>(defaultEntryStats.rankingPlace!)
    const [SNTie, setSNTie] = useState<number>(defaultSequenceNumberInTie![0])
    const [SNTieOutOf, setSNTieOutOf] = useState<number>(defaultSequenceNumberInTie![1])

    const presentationProps: PresentationProps = {
        rankingPlace,
        sequenceNumberInTie: SNTie && SNTieOutOf ? [SNTie, SNTieOutOf] : undefined,
    }

    const presentationParamInputs = [
        inputFactory(
            'ranking-place',
            'Ranking place',
            rankingPlace,
            'number',
            'Numeric ranking place ...',
            onChangeFactory((v) => setRankingPlace(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'sn-tie',
            'Tie position',
            SNTie,
            'number',
            'Current tie position ...',
            onChangeFactory((v) => setSNTie(v ? parseInt(v) : 0))
        ),
        inputFactory(
            'sn-tie-out-of',
            'Tie group size',
            SNTieOutOf,
            'number',
            'Tie group size ...',
            onChangeFactory((v) => setSNTieOutOf(v ? parseInt(v) : 0))
        ),
    ]

    return (
        <>
            <BaseFrameContainer
                width={width}
                height={height}
            >
                <Presentation {...presentationProps} />
            </BaseFrameContainer>
            <div
                className='flex items-center mt-7 select-none'
                style={{ width: width }}
            >
                <div className='flex flex-col justify-center mx-5 h-fit select-none'>
                    <h1 className='text-2xl font-bold select-none'>CONTROLS</h1>
                    <h2 className='text-sm select-none self-center'>PRESENTATION EDITOR</h2>
                </div>
                <div className='flex flex-wrap justify-around w-full select-none'>{presentationParamInputs}</div>
            </div>
        </>
    )
}
