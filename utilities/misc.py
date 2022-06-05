
import getpass
from utilities.colors import Color

'''
Banner
This class holds the program's banner logo and version tag
'''
class Banner:
    '''
    This is experimental,  i might remove it later
    If the username is mine (lol), current username string will be set to Admin
    '''
    if getpass.getuser() == 'rly0nheart':
        currentUser = f'🛡️ {Color.red}Admin{Color.reset}'
    else:
        currentUser = getpass.getuser()
        
    versionTag = '2.0.1-alpha'
    nameLogo = f'''{Color.white}
 _______        __          _______         __ __         
|       |.----.|  |_.-----.|     __|.--.--.|__|  |_.-----.
|   -   ||  __||   _|  _  ||__     ||  |  ||  |   _|  -__|
|_______||____||____|_____||_______||_____||__|____|_____|
                                              v{versionTag}
                         {Color.white}— Advanced Github {Color.red}OSINT{Color.white} Framework{Color.reset}



.:{Color.green}{currentUser}{Color.reset}:.    
- {Color.white}use {Color.green}help{Color.reset}{Color.white} command for usage{Color.reset}
- {Color.white}commands are case insensitive{Color.reset}
  {'-'*29}
'''
