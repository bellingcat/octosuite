import os
import sys
import platform
from datetime import datetime

colors = True
machine = sys.platform	
# Colors will be unavailable on non-linux machines
if machine.lower().startswith(("os", "win", "darwin","ios")): 
    colors = False

if not colors:
	reset = red = white = green  = green_bg = white_bg = red_bg = ""

else:
    date_time = datetime.now()
    print(f"\n\t OCTOSUITE © 2022 Richard Mwewa\n\t{date_time.strftime('%A %d %B %Y, %H:%M:%S%p')}\n\n\nOS: {platform.system()}\nProcessor: {platform.processor()}\nNode: {platform.node()}\nRelease: {platform.release()}\nArchitecture: {platform.architecture()}\nVersion: {platform.version()}\n\n")
    while True:
    	try:
    		color_chooser = input(f"[ ? ] Welcome {os.getlogin()}, would you like to enable colors for this session? (y/n) ")
    		if color_chooser.lower() == "y":
    			white = "\033[97m"
    			white_bg = "\033[47;30m"
    			red = "\033[91m"
    			reset = "\033[0m"
    			green = "\033[92m"
    			green_bg = "\033[42;37m"
    			red_bg = "\033[41;37m"
    			break
    		elif color_chooser.lower() == "n":
    		    red = white = green = green_bg = white_bg = red_bg = reset = ""
    		    break
    		else:
    			print(f"\n[ ! ] Your response ({color_chooser}) is invalid (expected y or n)")
    			
    	except KeyboardInterrupt:
    		exit(f"[ ! ] Process interrupted with Ctrl+C")
