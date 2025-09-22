const DECIMAL_SEPARATOR = '.'

export default function formatNumberToDecimalPrecision(n: number, decimalDigits: number): string {
    if (decimalDigits < 0) throw new TypeError('Number of decimal digits argument must be a positive integer')

    if (Number.isInteger(n)) return n.toString()

    const [integerPart, decimalPart] = n.toString().split('.')
    return `${integerPart}${DECIMAL_SEPARATOR}${(decimalPart ?? '').substring(0, decimalDigits)}`
}
