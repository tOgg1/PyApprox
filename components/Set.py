import copy

import Component

from Element import Element as Elem
from Parser import *
from Util import *

legalSetInfoData = ["meta"]
legalSetInfoFlags = {"meta" : ["type", "info"]}
legalSetScopes = ["data", "elements", "set"]
legalSetElements = {"data": [], "elements" : ["element"], "set" : ["elements", "weight"]}

elementElementOrder = {0 : "id", 1 : "weight"}
edgeLegalColors = ["black", "blue", "green", "purple", "red", "yellow"]


SET_INFO_WEIGHTED = 1
SET_INFO_UNWEIGHTED = 2

"""
Set class. Has a list of elements.
"""
class Set(Component.Component):

	def __init__(self):
		self.elements = []
		self.info = SET_INFO_UNWEIGHTED

	def addElement(self, element):
		self.elements.append(element)

	def removeElement(self, element):
		self.elements.remove(element)

	def getNonSetElements(self):
		nonSetElements = []
		for element in self.elements:
			if not(isinstance(element, Set)):
				nonSetElements.append(element)
		return copy.deepcopy(nonSetElements)

	def getSetElements(self):
		setElements = []
		for element in self.elements:
			if(isinstance(element, Set)):
				setElements.append(element)
		return copy.deepcopy(setElements)
		
	def getAllElements(self):
		return copy.deepcopy(self.elements)