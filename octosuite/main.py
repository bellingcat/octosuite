# import everything from the octosuite.py file
from octosuite.octosuite import * # I drifted away from the 'pythonic way' here


def octosuite():
    try:
        run = Octosuite()
        run.path_finder()
        run.clear_screen()
        run.configure_logging()
        run.check_updates()
        xprint(ascii_banner()[1], ascii_banner()[0])
              
        """
        Main loop keeps octosuite running, this will break if Octosuite detects a KeyboardInterrupt (Ctrl+C)
        or if the 'exit' command is entered.
        """
        while True:
            xprint(f"{white}┌──({red}{getpass.getuser()}{white}@{red}octosuite{white})\n├──[~{green}{os.getcwd()}{white}]\n└╼ {reset}",end="")
            command_input = input().lower()
            print("\n")
            """
            Iterate over the command_map and check if the user input matches any command in it [command_map],
            if there's a match, we return its method. If no match is found, we ignore it.
            """
            for command, method in run.command_map:
                if command_input == command:
                    method()
                    print("\n")
                else:
                    pass
        
    except KeyboardInterrupt:
        logging.warning(ctrl_c)
        xprint(f"\n{WARNING} {ctrl_c}")

    except Exception as e:
        logging.error(error.format(e))
        xprint(f"{ERROR} {error.format(e)}")
