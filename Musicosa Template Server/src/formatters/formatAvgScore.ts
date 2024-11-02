export default function formatAvgScore(avgScore: number, decimalDigits: number): string {
    if (decimalDigits < 0)
        return NaN.toString()

    return Number.isInteger(avgScore) ? avgScore.toString() : avgScore.toPrecision(decimalDigits + 1)
}