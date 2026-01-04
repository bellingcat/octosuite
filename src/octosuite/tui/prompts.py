import typing as t

import questionary as q
from questionary import Style

__all__ = ["Prompts"]


class Prompts:
    """Provides interactive prompts for user input collection."""

    def __init__(self):
        """Initialise the Prompts class."""
        pass

    @staticmethod
    def prompt(
        message: str,
        instruction: t.Optional[str] = None,
        style: t.Optional[Style] = None,
        qmark: t.Optional[str] = "?",
    ) -> str:
        """
        Display a text input prompt and validate non-empty input.

        :param message: The prompt message to display.
        :param instruction: Optional instruction text to guide the user.
        :param style: Optional questionary Style object for custom styling.
        :param qmark: Optional custom question mark character or string.
        :return: The user's input string.
        :raises KeyboardInterrupt: If the user cancels the prompt with CTRL+C.
        """

        result = q.text(
            message=message,
            instruction=instruction,
            style=style,
            qmark=qmark,
            validate=lambda text: len(text.strip()) > 0
            or None
            or "Input cannot be empty",
        ).ask()

        if result is None:
            raise KeyboardInterrupt

        return result

    @staticmethod
    def pagination_params() -> dict:
        """
        Prompt the user for pagination parameters.

        :return: Dictionary containing 'page' and 'per_page' integer values.
        """

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
