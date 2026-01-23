"""Terminal user interface for octosuite."""

from .menus import Menus

__all__ = ["run", "Menus"]


def run():
    """Run the interactive TUI."""

    menu = Menus()
    menu.main()
