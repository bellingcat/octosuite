import getpass
from octosuite.config import red, white, green, reset, Tree


# banner.py
# This file holds the program's banner and version tag
version_tag = "3.1.0"


def banner():
    banner_tree = Tree(getpass.getuser())
    banner_tree.add(f"use ‘{green}help{reset}’ command for usage")
    banner_tree.add(f"commands are case insensitive\n")
    return f"""
  _______        __          _______         __ __         
 |       |.----.|  |_.-----.|     __|.--.--.|__|  |_.-----.
 |   -   ||  __||   _|  _  ||__     ||  |  ||  |   _|  -__|
 |_______||____||____|_____||_______||_____||__|____|_____|
                                                 v{version_tag}
                          {white}— Advanced Github {red}OSINT{white} Framework


""", banner_tree
