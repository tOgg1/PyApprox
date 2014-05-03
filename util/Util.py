import re

# Five colours should be enough
COLOR_NONE = 0
COLOR_BLUE = 1
COLOR_RED = 2
COLOR_GREEN = 3
COLOR_PURPLE = 4
COLOR_YELLOW = 5
COLOR_BLACK = 6

nonePattern = re.compile("[nN][oO]?[nN]?[eE]?")
bluePattern = re.compile("[bB][lL][uU]?[eE]?")
redPattern = re.compile("[rR][eE]?[dD]?")
greenPattern = re.compile("[gG][rR][eE]?[eE]?[nN]?")
purplePattern = re.compile("[pP][uU]?[rR]?[pP]?[lL]?[eE]?")
yellowPattern = re.compile("[yY][eE]?[lL]?[lL]?[eE]?[wW]?")
blackPattern = re.compile("[bB][lL][aA]?[cC]?[kK]?")

def getColor(color):
	if(nonePattern.match(color)):
		return COLOR_NONE
	elif(bluePattern.match(color)):
		return COLOR_BLUE
	elif(redPattern.match(color)):
		return COLOR_RED
	elif(greenPattern.match(color)):
		return COLOR_GREEN
	elif(purplePattern.match(color)):
		return COLOR_PURPLE
	elif(yellowPattern.match(color)):
		return COLOR_YELLOW
	elif(blackPattern.match(color)):
		return COLOR_BLACK
	return COLOR_NONE

def colorToString(color):
	if(color == COLOR_NONE):
		return "None"
	elif(color == COLOR_BLUE):
		return "Blue"
	elif(color == COLOR_RED):
		return "Red"
	elif(color == COLOR_GREEN):
		return "Green"
	elif(color == COLOR_PURPLE):
		return "Purple"
	elif(color == COLOR_YELLOW):
		return "Yellow"
	elif(color == COLOR_BLACK):
		return "Black"
	return "None"