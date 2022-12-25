from octosuite.config import red, white, green, yellow, reset

"""
message prefixes that show what 
a notification in OctoSuite might be all about. This might not be very important or necessary in some cases, 
but I think it's better to know the severity of the notifications you get in a program.
"""
PROMPT = f"{white}[{green}PROMPT{white}]{reset}"
WARNING = f"{white}[{yellow}WARNING{white}]{reset}"
ERROR = f"{white}[{red}ERROR{white}]{reset}"
POSITIVE = f"{white}[{green}POSITIVE{white}]{reset}"
NEGATIVE = f"{white}[{red}NEGATIVE{white}]{reset}"
INFO = f"{white}[{green}INFO{white}]{reset}"
