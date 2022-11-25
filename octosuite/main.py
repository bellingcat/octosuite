import logging
from rich import print as xprint
from octosuite.octosuite import *
from octosuite.log_roller import LogRoller
from octosuite.message_prefixes import MessagePrefix


def octosuite():
    try:
        run = Octosuite()
        run.on_start()
        
    except KeyboardInterrupt:
        logging.warning(LogRoller.ctrl_c)
        xprint(f"{MessagePrefix.warning} {LogRoller.ctrl_c}")

    except Exception as e:
        logging.error(LogRoller.error.format(e))
        xprint(f"{MessagePrefix.error} {LogRoller.error.format(e)}")
