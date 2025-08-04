import React, { PropsWithChildren } from 'react'

import settingsRepository from '@/db/repository/settings'
import { DEFAULT_FRAME_HEIGHT, DEFAULT_FRAME_WIDTH } from '@/app/defaults'

import BaseFrameContainer from './BaseFrameContainer'

export default async function FrameContainer({ children }: PropsWithChildren) {
    const widthSetting = await settingsRepository.getSettingByKey<number>('frame.width_px')
    const width = widthSetting?.value ?? DEFAULT_FRAME_WIDTH

    const heightSetting = await settingsRepository.getSettingByKey<number>('frame.height_px')
    const height = heightSetting?.value ?? DEFAULT_FRAME_HEIGHT

    return (
        <BaseFrameContainer width={width} height={height}>
            {children}
        </BaseFrameContainer>
    )
}