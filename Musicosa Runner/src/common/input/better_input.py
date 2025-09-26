from typing import Callable

from common.formatting.tabulate import tab


def better_input(user_message: str,
                 validate: Callable[[str], bool] | None = None,
                 /, *,
                 default: str = "",
                 error_message: str | Callable[[str], str] | None = None,
                 indent_level: int = 0) -> str:
    def prompt() -> str:
        user_input = input(tab(indent_level, f"-> {user_message}{f" [{default}]" if default else ""}> "))
        return user_input.strip() if user_input else default

    def format_error(error_value: str) -> str:
        if callable(error_message):
            return error_message(error_value)
        else:
            return f"{error_message or "Invalid input"} (got '{error_value}')"

    user_input = prompt()

    if validate is None:
        return user_input

    while not validate(user_input):
        print(tab(indent_level, f"{format_error(user_input)}"))
        user_input = prompt()

    return user_input
