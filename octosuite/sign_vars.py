from octosuite.colors import Color

'''
Attributes
*Even here, I couldn't think of a good name.*
The Attributes class holds the signs/symbols that show what a notification in OctoSuite might be all about.
This might not be very important or necessary in some cases, but I think it's better to know the severerity of the notifications you get in a program.
'''
class SignVar:
	prompt = f'{Color.white}[{Color.green} ? {Color.white}]{Color.reset}'
	warning = f'{Color.white}[{Color.red} ! {Color.white}]{Color.reset}'
	error = f'{Color.white}[{Color.red} x {Color.white}]{Color.reset}'
	positive = f'{Color.white}[{Color.green} + {Color.white}]{Color.reset}'
	negative = f'{Color.white}[{Color.red} - {Color.white}]{Color.reset}'
	info = f'{Color.white}[{Color.green} * {Color.white}]{Color.reset}'
