import React from 'react'

import settingsRepository from '@/db/repository/settings'
import { DEFAULT_DISPLAY_DECIMAL_DIGITS, DEFAULT_FRAME_HEIGHT, DEFAULT_FRAME_WIDTH } from '@/app/defaults'

import TemplateEditor from '@/app/templates/components/TemplateEditor'

export default async function Page() {
    const widthSetting = await settingsRepository.getSettingByKey<number>('frame.width_px')
    const width = widthSetting?.value ?? DEFAULT_FRAME_WIDTH

    const heightSetting = await settingsRepository.getSettingByKey<number>('frame.height_px')
    const height = heightSetting?.value ?? DEFAULT_FRAME_HEIGHT

    const displayDecimalDigitsSetting =
        await settingsRepository.getSettingByKey<number>('templates.display_decimal_digits')
    const displayDecimalDigits = displayDecimalDigitsSetting?.value ?? DEFAULT_DISPLAY_DECIMAL_DIGITS

    return <TemplateEditor templateWidth={width} templateHeight={height} displayDecimalDigits={displayDecimalDigits}/>
}
