from .menus import Menus

__all__ = ["run_tui", "Menus"]


def run_tui():
    """Run the interactive TUI."""

    menu = Menus()
    menu.main()
