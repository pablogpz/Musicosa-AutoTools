export default function formatNumberToDecimalPrecision(n: number, decimalDigits: number): string {
    const decimalSeparator = ','

    if (decimalDigits < 0)
        throw new TypeError('"decimalDigits" argument must be a positive integer')

    if (Number.isInteger(n)) return `${n.toString()}${decimalSeparator}${"".padEnd(decimalDigits, '0')}`

    const [integerPart, decimalPart] = n.toString().split('.')
    return `${integerPart}${decimalSeparator}${decimalPart.substring(0, decimalDigits).padEnd(decimalDigits, '0')}`
}