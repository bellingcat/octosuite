import typing as t

import questionary as q
from prompt_toolkit.styles import Style


class Prompts:
    def __init__(self):
        pass

    @staticmethod
    def prompt(message: str, instruction: t.Optional[str] = None) -> str:
        return q.text(
            message=message,
            instruction=instruction,
        ).ask()

    @staticmethod
    def pagination_params() -> dict:
        """Prompt user for pagination parameters."""
        try:
            page = q.text(message="Page", instruction="defaults to 1", qmark="#").ask()
            per_page = q.text(
                message="Per Page",
                instruction="default and max is 100",
                qmark="#",
            ).ask()

            return {
                "page": int(page) if page else 1,
                "per_page": min(int(per_page) if per_page else 100, 100),
            }

        except (ValueError, TypeError):
            print("Invalid input, using defaults (page=1, per_page=100)")
            return {"page": 1, "per_page": 100}

    @staticmethod
    def quit() -> bool:
        try:
            if q.confirm(
                "This will close the session, continue?",
                default=True,
                style=Style(
                    [
                        ("qmark", "fg:red bold"),
                        ("question", "fg:red bold"),
                    ]
                ),
            ).ask():
                return True
            return False
        except KeyboardInterrupt:
            return True
