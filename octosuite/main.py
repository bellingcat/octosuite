# import everything from the octosuite.py file
from octosuite.octosuite import * # I drifted away from the 'pythonic way' here


def octosuite():
    try:
        run = Octosuite()
        run.on_start()
        
    except KeyboardInterrupt:
        logging.warning(ctrl_c)
        xprint(f"\n{WARNING} {ctrl_c}")

    except Exception as e:
        logging.error(error.format(e))
        xprint(f"{ERROR} {error.format(e)}")
