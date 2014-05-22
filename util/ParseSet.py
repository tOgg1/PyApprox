from Set import *
from Element import *
from Util import *
from Parser import *

def loadSet(filePath):
	setStructure = loadFile(filePath)

	infoObjects, scopeObjects = setStructure.separate()

	info = 0

	for object in infoObjects:
		if not(object.name in legalSetInfoData):
			raise Exception("Error while post-parsing set data. Received an invalid info-object. Allowed infoobjects:".join(legalSetInfoData))
		if not(object.flag in legalSetInfoFlags[object.name]):
			raise Exception("Error while post-parsing set data. Received an info-object with invalid type. Allowed types for infoclass ".join(legalSetInfoFlags[object.name]))

		if(object.flag == "info"):
			info = info ^ parseFlags(object.values)

		if(object.flag == "type"):
			if not(object.values[0] == "set"):
				raise Exception("Error while post-parsing set data. meta:type was not set equal to graph")
			if not(len(object.values) == 1):
				raise Exception("Error while post-parsing set data. meta::type had more than one value")

	elements = []
	sets = []

	for object in scopeObjects:
		
		if not(object.name in legalSetScopes):
			raise Exception("Error while post-parsing set data. Encountered illegal scopeobject: " + object.name)

		if(object.name == "data"):
			for underObject in object.values:
				if not(isinstance(underObject, Object)):
					raise Exception("Error while post-parsing set data. Data-object had something else than an object as a child")

				if not(underObject.name in legalSetScopes):
					raise Exception("Error while post-parsing set data. Encountered illegal scopeobject: " + object.name)

				if(underObject.name == "elements"):
					for element in underObject.values:
						if not (isinstance(element, Element)):
							raise Exception("Error while post-parsing set data. Element-object had something else than an element as a child")
						
						if not (element.name in legalSetElements[underObject.name]):
							raise Exception("Error while post-parsing set data. Element type " + element.name +" is not legal in scopeobject " + underObject.name)
						
						elm = parseElement(element.values)
						duplicates = [x for x in elements if x.id == elm.id]
						if(len(duplicates) != 0):
							raise Exception("Error while post-parsing set data. Duplicate elements with id " + str(elm.id))
						elements.append(elm)
						elements = sorted(elements, key=lambda x: x.id)

				# This needs to be its own method as we can have recursive set-structures
				if(underObject.name == "set"):
					sets.append(parseSet(underObject, elements))

		else:
			raise Exception("Error while post-parsing set data. All data in a graph has to be put in a data-scopeobject")

	return sets

def parseSet(setObject, elements):
	weight = 1
	set = Set()
	for element in setObject.values:
		if(isinstance(element, Object)):
			childSet = parseSet(element, elements)
			set.addElement(childSet)
			continue

		if not(isinstance(element, Element)):
			raise Exception("Error while post-parsing set data. Invalid structure type encountered. Please report this as a bug.")

		# setObject.name is obviously "set"
		if not (element.name in legalSetElements[setObject.name]):
			raise Exception("Error while post-parsing set data. Element type " + element.name + " is not legal in scopeobject " + setObject.name)	

		if(element.name == "elements"):
			setElements = parseElements(element.values, elements)
			
			for oelement in setElements:
				set.addElement(oelement)

		if(element.name == "weight"):
			weight = parseWeight(element.values)

	set.weight = weight
	return set

def parseElement(elementData):
	if(len(elementData) > len(elementElementOrder)):
		raise Exception("Error while post-parsing graph data. Invalid argument count for element `element`, expected expected 1-"+str(len(elementElementOrder))+", got " + str(len(elementData)))
	id = 0
	weight = 1
	for i in range(len(elementData)):
		splitData = elementData[i].split("=")
		value = ""
		name = ""

		if(len(splitData) <= 1):
			name = elementElementOrder[i] 
			value = splitData[0]
		else:
			name = splitData[0].replace(" ", "")
			value = splitData[1]

		value = value.replace(" ", "")

		if(idPattern.match(name)):
			id = int(value)
		elif(weightPattern.match(name)):
			weight = float(value)

	e = Elem()
	e.id = id
	e.weight = weight
	return e

def parseElements(elementsData, elements):

	setElements = []

	for i in range(len(elementsData)):
		splitData = elementsData[i].split("=")
		value = ""
		name = ""

		if(len(splitData) <= 1):
			name = "" 
			value = splitData[0]
		else:
			name = splitData[0].replace(" ", "")
			value = splitData[1]
		
		value = value.replace(" ", "")

		if(singlePattern.match(name)):
			eid = int(value)

			if(eid > len(elements)+1):
				raise Exception("Error while post-parsing set data.")

			setElements.append(elements[eid-1])

		elif(sequencePattern.match(name)):
			values = value.split("-")
			
			if(len(values) != 2):
				raise Exception("Error while post-parsing set data. Poorly formatted sequence: " + value)

			v1 = int(values[0])
			v2 = int(values[1])

			# Swap if necessary
			if v1 > v2:
				t = v1
				v1 = v2
				v2 = t

			if(v2 > len(elements)+1):
				raise Exception("Error while post-parsing set data. Element range exceeds id of last element")
			
			for i in range(v1, v2+1):
				setElements.append(elements[i])

		# We need to figure out what it is. But fear not, for the options is not many; neigh said the horse to the bishop, they areth but a few
		else:
			# Try to parse sequence
			if(sequenceValuePattern.match(value)):
				values = value.split("-")
			
				if(len(values) != 2):
					raise Exception("Error while post-parsing set data. Poorly formatted sequence: " + value)

				v1 = int(values[0])
				v2 = int(values[1])

				# Swap if necessary
				if v1 > v2:
					t = v1
					v1 = v2
					v2 = t

				if(v2 > len(elements)+1):
					raise Exception("Error while post-parsing set data. Element range exceeds id of last element")
				
				for i in range(v1, v2+1):
					setElements.append(elements[i])

			# Try to parse sequence
			else:
				try:
					eid = int(value)
					if(eid > len(elements)+1):
						raise Exception("Error while post-parsing set data.")
					
					setElements.append(elements[eid-1])
				except Exception, e:
					continue

	return setElements

def parseWeight(weightData):
	if(len(weightData) > 1):
		raise Exception("Error while post-parsing set data. Weight-element has too many values. Expected 1, got " + len(weightData))

	splitData = weightData[0].split("=")
	value = ""
	name = ""

	if(len(splitData) <= 1):
		name = "weight" 
		value = splitData[0]
	else:
		name = splitData[0].replace(" ", "")
		value = splitData[1]
	
	value = value.replace(" ", "")

	if not(weightPattern.match(name)):
		raise Exception("Error while post-parsing set data. Weight-element contained invalid value. Expected `weight`, found " + name)

	try:
		return float(value)
	except Exception, e:
		raise Exception("Error while-post-parsing set data. Weight-element's value is not float-value. Expected float, found " + value)

def parseFlags(infoValues):
	flag = 0

	if("weighted" in infoValues and "unweighted" in infoValues):
		raise Exception("Error while post-parsing set data. The set has been flagged as both weighted and unweighted")

	if("weighted" in infoValues):
		flag |= SET_INFO_WEIGHTED

	if("unweighted" in infoValues):
		flag |= SET_INFO_UNWEIGHTED

	return flag