import getpass
from utilities.colors import Color

class Banner:
    versionTag = '2.0.1-alpha'
    nameLogo = f'''{Color.white}
 _______        __          _______         __ __         
|       |.----.|  |_.-----.|     __|.--.--.|__|  |_.-----.
|   -   ||  __||   _|  _  ||__     ||  |  ||  |   _|  -__|
|_______||____||____|_____||_______||_____||__|____|_____|
                                                    v{versionTag}
                         {Color.white}— Advanced Github {Color.red}OSINT{Color.white} Framework{Color.reset}


.:{Color.white}{Color.green}{getpass.getuser()}{Color.reset}:.    

- {Color.white}Use {Color.green}help{Color.reset}{Color.white} command for usage{Color.reset}
- {Color.white}Commands are case insensitive{Color.reset}
{'-'*32}
'''
