from datetime import datetime

from prompt_toolkit.shortcuts import button_dialog, message_dialog

LICENSE_NOTICE = f"""Copyright (c) {datetime.now().year} Bellingcat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

__all__ = ["Dialogs"]


class Dialogs:
    """Provides interactive dialogue boxes for user confirmations and information display."""

    def __init__(self):
        """Initialise the Dialogs class."""
        ...

    @staticmethod
    def _boolean(title: str, text: str) -> bool:
        """
        Display a Yes/No dialogue and return the user's choice.

        :param title: The title of the dialogue box.
        :param text: The message text to display.
        :return: True if user selects Yes, False if No or cancelled.
        """

        try:
            result = button_dialog(
                title=title,
                text=text,
                buttons=[("Yes", True), ("No", False)],
            ).run()
            return result if result is not None else False
        except KeyboardInterrupt:
            return True

    def quit(self) -> bool:
        """
        Display a confirmation dialogue for quitting the application.

        :return: True if user confirms quit, False otherwise.
        """

        return self._boolean(
            title="Quit", text="This will close the session, continue?"
        )

    def clear_cache(self) -> bool:
        """
        Display a confirmation dialogue for clearing the cache.

        :return: True if user confirms cache clearing, False otherwise.
        """

        return self._boolean(
            title="Clear Cache",
            text="This will clear all octosuite caches, continue?",
        )

    @staticmethod
    def license():
        """Display the MIT license notice in a dialogue box."""
        message_dialog(title="MIT License", text=LICENSE_NOTICE).run()
