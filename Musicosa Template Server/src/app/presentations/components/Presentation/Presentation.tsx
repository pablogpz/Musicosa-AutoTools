import React from 'react'

import { ResolvedPresentationProps } from '@/app/presentations/common/withPresentationProps'

export type PresentationProps = ResolvedPresentationProps

export default function Presentation({ rankingPlace }: PresentationProps) {
    return (
        <div className="flex flex-row size-full justify-center items-center bg-black">
            <p className="text-[30rem] mb-16 font-black text-white">{rankingPlace}</p>
        </div>
    )
}