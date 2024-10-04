import React, { PropsWithChildren } from 'react'

export interface BaseTemplateContainerProps extends PropsWithChildren {
    width: number,
    height: number,
}

export default function BaseTemplateContainer({ width, height, children }: BaseTemplateContainerProps) {
    return (
        <div className="m-0 p-0 bg-white" style={{ width, height }}>
            {children}
        </div>
    )
}