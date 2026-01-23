import sys

from ._lib import console, __pkg__, __version__
from .core.cache import cache


def start():
    """Entry point for octosuite."""

    try:
        console.set_window_title(title=f"{__pkg__.title()} CLI v{__version__}")

        from ._cli import run

        run()

    except KeyboardInterrupt:
        sys.exit()
    finally:
        cache.clear()
