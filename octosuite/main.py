import logging
from rich import print as xprint
from octosuite.sign_vars import SignVar
from octosuite.octosuite import Octosuite
from octosuite.log_roller import logRoller


def main():
    try:
        run = Octosuite()
        run.onStart()
        
    except KeyboardInterrupt:
        logging.warning(logRoller.Ctrl.format("Ctrl+C"))
        xprint(f"{SignVar.warning} {logRoller.Ctrl.format('Ctrl+C')}")

    except Exception as e:
        logging.error(logRoller.Error.format(e))
        xprint(f"{SignVar.error} {logRoller.Error.format(e)}")
