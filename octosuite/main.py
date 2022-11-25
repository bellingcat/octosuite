from octosuite.octosuite import *


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
