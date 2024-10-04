export default function formatScore(score: number, decimalDigits: number): string {
    if (decimalDigits < 0)
        return NaN.toString()

    return Number.isInteger(score) ? score.toString() : score.toPrecision(decimalDigits + 1)
}