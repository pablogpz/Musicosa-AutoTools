/**
 * @see https://prettier.io/docs/configuration
 * @type {import("prettier").Config}
 */
const config = {
    printWidth: 120,
    tabWidth: 4,
    useTabs: false,
    semi: false,
    singleQuote: true,
    quoteProps: 'as-needed',
    jsxSingleQuote: true,
    trailingComma: 'es5',
    bracketSpacing: true,
    objectWrap: 'preserve',
    bracketSameLine: false,
    arrowParens: 'always',
    proseWrap: 'always',
    htmlWhitespaceSensitivity: 'strict',
    endOfLine: 'auto',
    embeddedLanguageFormatting: 'auto',
    singleAttributePerLine: true,
}

export default config
