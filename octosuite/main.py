import sys

from .tui.menus import Menus
from .tui.prompts import Prompts


def start():
    try:
        prompts = Prompts()
        menu = Menus(prompts=prompts)
        menu.main()
    except KeyboardInterrupt:
        sys.exit()
