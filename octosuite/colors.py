import sys
import platform
from datetime import datetime

# The Color class is responsible for enabling/disabling colors in OctoSuite
# This class gets called first at start up before any other class/method gets called (makes one think why this is not the firstBlood class)
# Color class is the reason why users get to choose whether to enable/disable colors
# Unfortunately for our friends the 'non-Linux' users, they will not yet have the opportunity to see what OctoSuite looks like with colors enabled lol
class Color:
	colors = True
	# Colors will be unavailable on non-linux machines
	if sys.platform.lower().startswith(("os", "win", "darwin","ios")):
	    colors = False
	    
	if not colors:
	    reset = red = white = green = red_bg = ""
	    
	else:
	    # Printing system information was completely unnecessary (just like most things in this program :D)
	    # But at least users will get to know things they did not know about their machines ;)
	    date_time = datetime.now()
	    sys_info = [("Processor",platform.processor),
	                ("Node", platform.node),
	                ("Release", platform.release),
	                ("Architecture", platform.architecture),
	                ("Version", platform.version)]
	                        
	    banner = f"""
	            OCTOSUITE © 2022 Richard Mwewa
	            {date_time.strftime('%A %d %B %Y, %H:%M:%S%p')}
	            
	            
	            
	{platform.system()}"""
	    print(banner)
	    for key, value in sys_info:
	        print(f"\t├─ {key}: {value()}")
	    print("\n")
	    while True:
	        try:
	            color_chooser = input(f"[ ? ] Welcome, would you like to enable colors for this session? (Y/n) ")
	            if color_chooser.lower() == "y":
	                white = "\033[97m"
	                red = "\033[91m"
	                reset = "\033[0m"
	                green = "\033[92m"
	                break
	            elif color_chooser.lower() == "n":
	                red = white = green = red_bg = reset = ""
	                break
	            else:
	                print(f"\n[ ! ] Your response ({color_chooser}) is invalid (expected y or n) ")
	                
	        except KeyboardInterrupt:
	            exit(f"[ ! ] Process interrupted with [Ctrl+C].")
