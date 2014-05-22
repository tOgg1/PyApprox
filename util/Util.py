import re

## COLOR INFORMATION

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


## GENERAL REGEX-PATTERNS FOR PARSING

idPattern = re.compile("[iI][dD]?")
weightPattern = re.compile("[wW][eE]?[iI]?[gG]?[hH]?[tT]?")
positionPattern = re.compile("[pP][oO][sS][iI][tT][iI][oO][nN]")
colorPattern = re.compile("[cC][oO][lL][oO][rR]")

v1Pattern = re.compile("([vV][1])|([vV][eE][rR]?[tT]?[eE]?[xX]?[1])")
v2Pattern = re.compile("([vV][2])|([vV][eE][rR]?[tT]?[eE]?[xX]?[2])")

singlePattern = re.compile("[sS][iI][nN]?[gG]?[lL]?[eE]?")
sequencePattern = re.compile("[sS][eE][qQ][uU][eE][nN][cC][eE]")

sequenceValuePattern = re.compile("(\d)+-(\d)+")

## GRAPH LOADING METADATA

legalGraphInfoData = ["meta"]
legalGraphInfoFlags = {"meta" : ["type", "info"]}
legalGraphScopes = ["data", "vertices", "edges"]
legalGraphElements = {"data": [], "vertices" : ["vertex"], "edges" : ["edge"]}

vertexElementOrder = {0 : "id", 1 : "weight", 2 : "position", 3 : "color"}
vertexLegalColors = ["black", "blue", "green", "purple", "red", "yellow"]
edgeLegalColors = ["black", "blue", "green", "purple", "red", "yellow"]

edgeElementOrder = {0 : "v1", 1: "v2", 2 : "weight", 3: "color"}

GRAPH_INFO_WEIGHTED 	= 1
GRAPH_INFO_UNWEIGHTED 	= 2
GRAPH_INFO_DIRECTED 	= 4
GRAPH_INFO_UNDIRECTED 	= 8
GRAPH_INFO_METRIC 		= 16
GRAPH_INFO_COLORED 		= 32

## SET LOADING METADATA

legalSetInfoData = ["meta"]
legalSetInfoFlags = {"meta" : ["type", "info"]}
legalSetScopes = ["data", "elements", "set"]
legalSetElements = {"data": [], "elements" : ["element"], "set" : ["elements", "weight"]}

elementElementOrder = {0 : "id", 1 : "weight"}
edgeLegalColors = ["black", "blue", "green", "purple", "red", "yellow"]


SET_INFO_WEIGHTED = 1
SET_INFO_UNWEIGHTED = 2

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