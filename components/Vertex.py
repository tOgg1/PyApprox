from Util import *
import Component
import math

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

def pdistance(pos1, pos2):
	if not(isinstance(pos1, Position) and isinstance(pos2, Position)):
		raise Exception("Invalid input for method distance, expected two positions got " + str(pos1) + ", " + str(pos2))

	dx = pos1.x - pos2.x
	dy = pos1.y - pos2.y

	return math.sqrt(dx*dx + dy*dy)

def vdistance(vertex1, vertex2):
	if not(isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex)):
		raise Exception("Invalid input for method distance, expected two vertices, got " + str(vertex1) + ", " + str(vertex2))

	return pdistance(vertex1.pos, vertex2.pos)