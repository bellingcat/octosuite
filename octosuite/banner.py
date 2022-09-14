import getpass
from octosuite.colors import red, white, green, reset

"""
banner.py
This file holds the program's banner logo and version tag
"""
version_tag = "2.2.3"
name_logo = f"""{white}
  _______        __          _______         __ __         
 |       |.----.|  |_.-----.|     __|.--.--.|__|  |_.-----.
 |   -   ||  __||   _|  _  ||__     ||  |  ||  |   _|  -__|
 |_______||____||____|_____||_______||_____||__|____|_____|
                                                     v{version_tag}
                          {white}— Advanced Github {red}OSINT{white} Framework



.:{getpass.getuser()}:.
├─ use ‘{green}help{reset}{white}’ command for usage
└╼ commands are case insensitive{reset}
"""
