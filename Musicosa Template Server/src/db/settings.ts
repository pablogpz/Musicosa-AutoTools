export enum SettingsGroups {
    templates = 'templates',
    ranking = 'ranking'
}

export enum TemplatesSettingsNames {
    totalWidthPx = 'total_width_px',
    totalHeightPx = 'total_height_px'
}

export enum RankingSettingsNames {
    significantDecimalDigits = 'significant_decimal_digits'
}

export type SettingsKey =
    `${SettingsGroups.templates}.${TemplatesSettingsNames}`
    | `${SettingsGroups.ranking}.${RankingSettingsNames}`