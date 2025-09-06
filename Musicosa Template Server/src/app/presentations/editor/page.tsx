import settingsRepository from '@/db/repositories/settings'
import { DEFAULT_FRAME_HEIGHT, DEFAULT_FRAME_WIDTH } from '@/app/defaults'

import PresentationEditor from '@/app/presentations/components/PresentationEditor'

export default async function Page() {
    const widthSetting = await settingsRepository.getSettingByKey<number>('frame.width_px')
    const width = widthSetting?.value ?? DEFAULT_FRAME_WIDTH

    const heightSetting = await settingsRepository.getSettingByKey<number>('frame.height_px')
    const height = heightSetting?.value ?? DEFAULT_FRAME_HEIGHT

    return <PresentationEditor width={width} height={height}/>
}
