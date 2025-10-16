'use client'

import React, { useLayoutEffect, useRef, useState } from 'react'

interface FlexibleContainer {
    widthPx: number
    heightPx: number
}

interface PositionMeasurementProps {
    positionTopPx: number
    positionLeftPx: number
}

const withPositionMeasurement = <P extends FlexibleContainer>(
    Component: React.ComponentType<P & PositionMeasurementProps>,
    displayName: string
): React.ComponentType<P> => {
    return (props: P) => {
        const [position, setPosition] = useState({ top: 0, left: 0 })
        const measurementElementRef = useRef<HTMLDivElement>(null)

        useLayoutEffect(() => {
            const measuredRect = measurementElementRef.current!.getBoundingClientRect()
            let measuredPosition

            setPosition(
                (measuredPosition = {
                    top: Math.round(measuredRect.top + window.scrollY),
                    left: Math.round(measuredRect.left + window.scrollX),
                })
            )

            console.log(
                `[${displayName}] position in viewport ` +
                    `{ top: ${measuredPosition.left}px, left: ${measuredPosition.top}px }`
            )
        }, [props.widthPx, props.heightPx])

        return (
            <div
                ref={measurementElementRef}
                className='size-fit'
            >
                <Component
                    positionTopPx={position.top}
                    positionLeftPx={position.left}
                    {...props}
                />
            </div>
        )
    }
}

type VideoPlaceholderProps = PositionMeasurementProps & FlexibleContainer

function BaseVideoPlaceholder({ widthPx, heightPx, positionTopPx, positionLeftPx }: VideoPlaceholderProps) {
    return (
        <div
            className='w-full h-full flex items-center justify-center relative z-50
             bg-[repeating-linear-gradient(45deg,_black_0px,_black_10px,_yellow_10px,_yellow_20px)]'
            style={{ width: `${widthPx}px`, height: `${heightPx}px` }}
        >
            <p className='font-bold text-lg p-5 bg-white w-fit'>
                {`(top: ${positionTopPx}px), (left: ${positionLeftPx}px)`}
            </p>
        </div>
    )
}

const VideoPlaceholder = withPositionMeasurement(BaseVideoPlaceholder, 'VideoPlaceholder')

export default VideoPlaceholder
