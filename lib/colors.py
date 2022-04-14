import os
import sys

colors = True
machine = sys.platform	
# Colors will be unavailable on non-linux machines
if machine.lower().startswith(("os", "win", "darwin","ios")): 
    colors = False

if not colors:
	reset = red = white = green  = green_bg = white_bg = red_bg = ""

else:
    try:
    	color_chooser = input(f"[ ? ] Welcome {os.getlogin()}, would you like to enable colors for this session? [Y/n] ")
    	if color_chooser.lower() == "y":
    		white = "\033[97m"
    		white_bg = "\033[47;30m"
    		red = "\033[91m"
    		reset = "\033[0m"
    		green = "\033[92m"
    		green_bg = "\033[42;37m"
    		red_bg = "\033[41;37m"
    	else:
    		red = white = green = green_bg = white_bg = red_bg = reset = ""
    		
    except KeyboardInterrupt:
    	exit(f"[ ! ] Process interrupted with Ctrl+C")
