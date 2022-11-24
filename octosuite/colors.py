import psutil
import platform
from datetime import datetime


# This file is responsible for enabling/disabling colors in OctoSuite
# This file gets called first at start up before any other file gets called
# colors.py is the reason why users get to choose whether to enable/disable colors
# delete this file, the entire program breaks
system_info = [("RAM", f"{str(round(psutil.virtual_memory().total / (1024.0 **3)))}GB"),
               ("Node", platform.node),
               ("Release", platform.release),
               ("Version", platform.version),
               ("Processor",platform.processor),
               ("Architecture", platform.architecture)
               ]
start_banner = f"""
            OCTOSUITE © 2023 Richard Mwewa
            {datetime.now().strftime('%A %d %B %Y, %H:%M:%S%p')}
         
         """

print(start_banner)
print(f"{platform.system()}")
for system_key, system_value in system_info:
    print(f"├─ {system_key}: {system_value()}")
print("\n")
while True:
    try:
        color_chooser = input(f"[?] Welcome, would you like to enable colors for this session? (yes/no) ").lower()
        if color_chooser == "yes":
            header_title = "bold white"
            red = "[red]"
            white = "[white]"
            green = "[green]"
            red_bold = "[white bold]"
            white_bold = "[white bold]"
            green_bold = "[green bold]"
            reset = "[/]"
            break
        elif color_chooser == "no":
            header_title = red = white = green = red_bold = white_bold = green_bold = reset = ""
            break
        else:
            print(f"\n[!] Your response '{color_chooser}' is invalid (expected yes or no)")

    except KeyboardInterrupt:
        exit(f"[!] Process interrupted with Ctrl+C.")
