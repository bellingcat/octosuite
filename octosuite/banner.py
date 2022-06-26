import getpass
from octosuite.colors import Color

'''
Banner
This class holds the program's banner logo and version tag
'''
class Banner:
    versionTag = '2.1.1'
    nameLogo = f'''{Color.white}
  _______        __          _______         __ __         
 |       |.----.|  |_.-----.|     __|.--.--.|__|  |_.-----.
 |   -   ||  __||   _|  _  ||__     ||  |  ||  |   _|  -__|
 |_______||____||____|_____||_______||_____||__|____|_____|
                                                     v{versionTag}
                          {Color.white}— Advanced Github {Color.red}OSINT{Color.white} Framework{Color.reset}



.:{getpass.getuser()}:.
{Color.white}├─ use {Color.green}help{Color.reset}{Color.white} command for usage{Color.reset}
{Color.white}└╼ commands are case insensitive{Color.reset}
'''
