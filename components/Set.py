from Element import Element


"""
Set class. Has a list of elements.
"""
class Set:

	def __init__(self):
		self.elements = []

	def addElement(self, element):
		if not isinstance(element, Element):
			return
		self.elements.append(element)

	def removeElement(self, element):
		if not isintance(element, Element):
			return

		self.elements.remove(element)