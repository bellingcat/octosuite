import os
from lib.colors import red, white, green, red_bg,reset

version = 'v1.9.0'
banner = f'''{red}
       ▒█████   ▄████▄  ▄▄▄█████▓ ▒█████    ██████  █    ██  ██▓▄▄▄█████▓▓█████ 
      ▒██▒  ██▒▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒▒██    ▒  ██  ▓██▒▓██▒▓  ██▒ ▓▒▓█   ▀ 
      ▒██░  ██▒▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒░ ▓██▄   ▓██  ▒██░▒██▒▒ ▓██░ ▒░▒███   
      ▒██   ██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░  ▒   ██▒▓▓█  ░██░░██░░ ▓██▓ ░ ▒▓█  ▄ 
      ░ ████▓▒░▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░▒██████▒▒▒█████▓ ░██░  ▒██▒ ░ ░▒████▒
      ░ ▒░▒░▒░ ░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▓    ▒ ░░   ░░ ▒░ ░
        ░ ▒ ▒░   ░  ▒       ░      ░ ▒ ▒░ ░ ░▒  ░ ░░░▒░ ░ ░  ▒ ░    ░     ░ ░  ░
      ░ ░ ░ ▒  ░          ░      ░ ░ ░ ▒  ░  ░  ░   ░░░ ░ ░  ▒ {red_bg} {version} {reset}{red}
          ░ ░  ░ ░                   ░ ░        ░     ░      ░              ░  ░
               ░                              {white}— Advanced Github {red}OSINT{white} Framework{reset}



> {white}Current user: {green}{os.getlogin()}{reset}
> {white}Use {green}help{reset}{white} command for usage{reset}
> {white}Commands are case sensitive{reset}
  {'-'*27}


'''
