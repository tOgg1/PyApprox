from Util import *
import Component

"""
Vertex class. 
"""
class Vertex(Component.Component):

	def __init__(self):
		self.color = COLOR_NONE
		self.weight = 0
		self.pos = Position(1, 1)

	def toString(self):
		return "Vertex = {Color="+colorToString(self.color)+", weight = " + str(self.weight) +", pos = (" + str(self.pos.x) + ", " + str(self.pos.y) + ")}" 

class Position:

	def __init__(self, x = None, y = None):
		if(x == None):
			self.x = 1
		else:
			self.x = x
			
		if(y == None):
			self.y = 1
		else:
			self.y = y
