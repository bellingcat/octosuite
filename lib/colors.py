import sys

# Colors will be unavailable on non-linux machines
colors = True
machine = sys.platform
if machine.lower().startswith(("os", "win", "darwin")): 
    colors = False

if not colors:
	reset = red = white = green  = ""

else:                                                 
    white = "\033[97m"
    red = "\033[91m"    
    reset = "\033[0m"
    green = "\033[92m"
