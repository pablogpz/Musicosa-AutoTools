from typing import Callable


def better_input(user_message: str,
                 validate: Callable[[str], bool] | None = None,
                 error_message: str | Callable[[str], str] | None = None,
                 /, *,
                 default: str = "",
                 indentation_level: int = 0) -> str:
    indentation = " " * indentation_level

    def prompt() -> str:
        inner_user_input = input(f"{indentation}-> {user_message}{f" [{default}]" if default else ""}> ")
        return inner_user_input.strip() if inner_user_input else default

    if validate is None:
        return prompt()

    def format_error(error_value: str) -> str:
        if callable(error_message):
            return error_message(error_value)
        else:
            return f"{error_message or "Invalid input"} (got '{error_value}')"

    user_input = prompt()
    while not validate(user_input):
        print(f"{indentation}{format_error(user_input)}")
        user_input = prompt()

    return user_input
