import { Open_Sans } from 'next/font/google'

import { ResolvedTemplateProps } from '@/app/templates/common/withTemplateProps'
import Avatar from '@/app/templates/components/Avatar'
import VideoPlaceholder from '@/app/templates/components/VideoPlaceholder'

export interface TemplateOuterProps {
    disableVideoPlaceholder?: boolean
}

export type TemplateProps = ResolvedTemplateProps & TemplateOuterProps

const open_sans = Open_Sans({
    subsets: ['latin'],
    display: 'swap',
    variable: '--font-open-sans',
})

// TFA 3º Edition (2026) Template

export default function Template({
    gameTitle,
    nominee,
    rankingPlace,
    formattedAvgScore,
    avatarScale,
    videoBoxWidthPx,
    videoBoxHeightPx,
    award,
    members,
    disableVideoPlaceholder = false,
}: TemplateProps) {
    const sortedMembers = members.sort((a, b) => a.vote.score - b.vote.score)

    const headerComponent = (
        <div className='flex flex-row items-center justify-center mt-9'>
            <div className={`bg-white ${open_sans.className} rounded-xl p-6 mr-10`}>
                <p className='text-4xl font-bold'>{rankingPlace}º</p>
            </div>
            <p className='text-white text-5xl font-bold max-w-96'>{award.designation}</p>
        </div>
    )

    const nominationInfoComponent = (
        <div className='flex flex-row items-center mt-20 mx-5'>
            <div className='text-white mr-4'>
                <p className={`text-5xl ${open_sans.className} font-black`}>{formattedAvgScore}</p>
            </div>
            <div className='h-full w-[0.25em] bg-white mr-4' />
            <div className='flex flex-col justify-around size-full'>
                {nominee && <p className='text-4xl font-semibold bg-white p-4 mb-4'>{nominee}</p>}
                <p className={`text-${nominee ? '2xl font-light py-2' : '4xl font-semibold py-4'} bg-white px-4`}>
                    {gameTitle}
                </p>
            </div>
        </div>
    )

    return (
        /* ! IMPORTANT: Make sure every background image is in PNG format */
        <div
            className='grid grid-cols-[32%_68%] grid-rows-[72%_28%] w-full h-full p-7 overflow-clip'
            style={{
                backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), url("/bg/${award.slug}.png")`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}
        >
            <div className='row-start-1 row-end-2 col-start-1 col-end-2 h-full'>
                <div className='flex flex-col h-full'>
                    {headerComponent}
                    {nominationInfoComponent}
                </div>
            </div>
            <div className='row-start-1 row-end-2 col-start-2 col-end-3 place-self-center mb-14'>
                {!disableVideoPlaceholder && (
                    <VideoPlaceholder
                        widthPx={videoBoxWidthPx}
                        heightPx={videoBoxHeightPx}
                    />
                )}
            </div>
            <div className='row-start-2 row-end-3 col-start-1 col-end-3'>
                <div className='flex flex-row content-center justify-evenly items-end h-full'>
                    {sortedMembers.map((member, i) => (
                        <Avatar
                            key={i}
                            avatar={member.avatar}
                            avatarScale={avatarScale}
                            formattedScore={member.vote.formattedScore}
                        />
                    ))}
                </div>
            </div>
        </div>
    )
}
