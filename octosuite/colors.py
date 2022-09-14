import platform
from datetime import datetime

# This file is responsible for enabling/disabling colors in OctoSuite
# This file gets called first at start up before any other file gets called
# colors.py is the reason why users get to choose whether to enable/disable colors
system_info = [("Processor",platform.processor),
                 ("Node", platform.node),
                 ("Release", platform.release),
                 ("Architecture", platform.architecture),
                 ("Version", platform.version)]
banner = f"""
            OCTOSUITE © 2022 Richard Mwewa
            {datetime.now().strftime('%A %d %B %Y, %H:%M:%S%p')}
         
         """

print(banner)
print(f"\t{platform.system()}")
for key, value in system_info:
    print(f"\t├─ {key}: {value()}")
print("\n")
while True:
    try:
        color_chooser = input(f"[ ? ] Welcome, would you like to enable colors for this session? (Y/n) ").lower()
        if color_chooser == "y":
            header_title = "bold white"
            red = "[red]"
            white = "[white]"
            green = "[green]"
            red_bold = "[white bold]"
            white_bold = "[white bold]"
            green_bold = "[green bold]"
            reset = "[/]"
            break
        elif color_chooser == "n":
            header_title = red = white = green = red_bold = white_bold = green_bold = reset = ""
            break
        else:
            print(f"\n[ ! ] Your response '{color_chooser}' is invalid (expected y or n)")

    except KeyboardInterrupt:
        exit(f"[ ! ] Process interrupted with [Ctrl+C].")
