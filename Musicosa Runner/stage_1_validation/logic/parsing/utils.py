def parse_score_str(score_str: str) -> float:
    try:
        return float(score_str)
    except ValueError:
        raise


def unquote(string: str) -> str:
    return string.strip()[1:-1] if len(string) > 2 else string
