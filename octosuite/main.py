import sys

from . import console, __pkg__, __version__
from .tui.menus import Menus


def start():
    try:
        console.set_window_title(title=f"{__pkg__.title()} v{__version__}")
        menu = Menus()
        menu.main()
    except KeyboardInterrupt:
        sys.exit()
