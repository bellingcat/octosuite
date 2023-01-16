# import everything from the octosuite.py file
from octosuite.octosuite import *  # I drifted away from the 'pythonic way' here


def octosuite():
    try:
        run = Octosuite()
        path_finder()
        configure_logging()
        check_updates()
        if args.method:
            """
            Iterate over the argument_map and check if the passed command line argument matches any argument in it [argument_map],
            if there's a match, we return its method. If no match is found, we do nothing (which will return the usage).
            """
            for argument, method in run.argument_map:
                if args.method == argument:
                    method()
                    print("\n")
                else:
                    pass
        else:
            """
            Main loop keeps octosuite running, this will break if Octosuite detects a KeyboardInterrupt (Ctrl+C)
            or if the 'exit' command is entered.
            """
            xprint(banner()[0], banner()[1])
            while True:
                command_input = Prompt.ask(f"{white}┌──({red}{getpass.getuser()}{white}@{red}octosuite{white})\n├──[~{green}{os.getcwd()}{white}]\n└╼{reset}")
                """
                Iterate over the command_map and check if the user input matches any command in it [command_map],
                if there's a match, we return its method. If no match is found, we ignore it.
                """
                if command_input[:2] == 'cd':
                    os.chdir(command_input[3:])
                elif command_input[:2] == 'ls':
                    os.system(f'dir {command_input[3:]}' if os.name == 'nt' else f'ls {command_input[3:]}')
                else:
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
