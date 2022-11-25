import random
import getpass
from rich.tree import Tree
from octosuite.colors import red, white, green, reset


# banners.py
# This file holds the program's banners and version tag
version_tag = "3.0.0"


def ascii_banner():
    banner_tree = Tree(getpass.getuser())
    banner_tree.add(f"use ‘{green}help{reset}’ command for usage")
    banner_tree.add(f"commands are case insensitive\n")
    ascii_banners = [
        """
  _______        __          _______         __ __         
 |       |.----.|  |_.-----.|     __|.--.--.|__|  |_.-----.
 |   -   ||  __||   _|  _  ||__     ||  |  ||  |   _|  -__|
 |_______||____||____|_____||_______||_____||__|____|_____|
                                                    """,
        """
╔═╗┌─┐┌┬┐┌─┐╔═╗┬ ┬┬┌┬┐┌─┐
║ ║│   │ │ │╚═╗│ ││ │ ├┤ 
╚═╝└─┘ ┴ └─┘╚═╝└─┘┴ ┴ └─┘
                      """,
        """
░▒█▀▀▀█░█▀▄░▀█▀░▄▀▀▄░▒█▀▀▀█░█░▒█░░▀░░▀█▀░█▀▀
░▒█░░▒█░█░░░░█░░█░░█░░▀▀▀▄▄░█░▒█░░█▀░░█░░█▀▀
░▒█▄▄▄█░▀▀▀░░▀░░░▀▀░░▒█▄▄▄█░░▀▀▀░▀▀▀░░▀░░▀▀▀
                                         """,
        """
 ▄▀▄ ▄▀▀ ▀█▀ ▄▀▄ ▄▀▀ █ █ █ ▀█▀ ██▀
 ▀▄▀ ▀▄▄  █  ▀▄▀ ▄██ ▀▄█ █  █  █▄▄
                              """]
    ascii_banner = random.choice(ascii_banners)
    return banner_tree, f"""{ascii_banner} v{version_tag}
                          {white}— Advanced Github {red}OSINT{white} Framework



"""

