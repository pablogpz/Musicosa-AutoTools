import { Open_Sans } from 'next/font/google'

import { ResolvedPresentationProps } from '@/app/presentations/common/withPresentationProps'

export type PresentationProps = ResolvedPresentationProps

const open_sans = Open_Sans({
    subsets: ['latin'],
    display: 'swap',
    variable: '--font-open-sans',
})

export default function Presentation({ rankingPlace, sequenceNumberInTie }: PresentationProps) {
    return (
        <div className='flex flex-row size-full justify-center items-center bg-black'>
            <p className='text-[35rem] mb-16 font-black text-white'>{rankingPlace}</p>
            {sequenceNumberInTie && (
                <>
                    <div className='h-[30rem] w-2 bg-white mx-14 rounded' />
                    <p className='text-7xl font-light p-8 bg-white rounded-xl'>
                        EMPATE
                        <span className='font-bold border-black border-3 px-5 rounded mx-5'>
                            {sequenceNumberInTie[1]}
                        </span>
                        <span className={`${open_sans.className} text-4xl relative bottom-4`}>
                            {sequenceNumberInTie[0]} de {sequenceNumberInTie[1]}
                        </span>
                    </p>
                </>
            )}
        </div>
    )
}
