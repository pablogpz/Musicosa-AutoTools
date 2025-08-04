import React, { PropsWithChildren } from 'react'

export interface BaseFrameContainerProps extends PropsWithChildren {
    width: number,
    height: number,
}

export default function BaseFrameContainer({ width, height, children }: BaseFrameContainerProps) {
    return (
        <div className="m-0 p-0 bg-white" style={{ width, height }}>
            {children}
        </div>
    )
}