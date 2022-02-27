import sys

colors = True
machine = sys.platform # Detecting the os
if machine.lower().startswith(("os", "win", "darwin","ios")): 
    colors = False # Colors will not be displayed

if not colors:
	reset = red = white = green  = ""

else:                                                 
    white = "\033[97m"
    red = "\033[91m"    
    reset = "\033[0m"
    green = "\033[92m"
