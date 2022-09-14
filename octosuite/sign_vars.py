from octosuite.colors import red, white, green, reset

"""
SignVar *Even here, I couldn't think of a good name.* The Attributes class holds the signs/symbols that show what 
a notification in OctoSuite might be all about. This might not be very important or necessary in some cases, 
but I think it's better to know the severity of the notifications you get in a program. 
"""
class SignVar:
    prompt = f"{white}[{green} ? {white}]{reset}"
    warning = f"{white}[{red} ! {white}]{reset}"
    error = f"{white}[{red} x {white}]{reset}"
    positive = f"{white}[{green} + {white}]{reset}"
    negative = f"{white}[{red} - {white}]{reset}"
    info = f"{white}[{green} * {white}]{reset}"
