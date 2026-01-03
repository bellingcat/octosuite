import typing as t

import questionary as q
from questionary import Style


class Prompts:
    def __init__(self):
        pass

    @staticmethod
    def prompt(
        message: str,
        instruction: t.Optional[str] = None,
        style: t.Optional[Style] = None,
        qmark: t.Optional[str] = "?",
    ) -> str:
        return q.text(
            message=message,
            instruction=instruction,
            style=style,
            qmark=qmark,
            validate=lambda text: len(text.strip()) > 0 or "Input cannot be empty",
        ).ask()

    @staticmethod
    def pagination_params() -> dict:
        """Prompt user for pagination parameters."""
        try:
            page = q.text(message="Page", default="1", qmark="n").ask()
            per_page = q.text(
                message="Per Page",
                default="100",
                qmark="n",
            ).ask()

            return {
                "page": int(page) if page else 1,
                "per_page": min(int(per_page) if per_page else 100, 100),
            }

        except (ValueError, TypeError):
            print("Invalid input, using defaults (page=1, per_page=100)")
            return {"page": 1, "per_page": 100}
