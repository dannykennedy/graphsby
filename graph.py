from rdflib import Namespace, Literal, ConjunctiveGraph


########################
# SET UP GRAPH STRUCTURE
########################

# Let's give properties some properties
# https://stackoverflow.com/questions/2078404/can-rdf-properties-contain-other-properties

# Namespace declarations
# RDFlib uses square brackets to show prefix and literals
owlNS = Namespace("http://www.w3.org/2002/07/owl#")
owlClass = owlNS["Class"]
owlObjectProperty = owlNS["ObjectProperty"]
owlDatatypeProperty = owlNS["DatatypeProperty"]
rdfNS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfProperty = rdfNS["Property"]
rdfType = rdfNS["type"]
rdfsNS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
rdfsSubClassOf = rdfsNS["subClassOf"]
rdfsDomain = rdfsNS["domain"]
rdfsRange = rdfsNS["range"]
dreamNS = Namespace("https://www.dannykennedy.co/dnj-ontology#")

# XML properties
xsdNS = Namespace("http://www.w3.org/2001/XMLSchema#")
xsdString = xsdNS["string"] #xsd:string
xsdDateTime = xsdNS["dateTime"] #xsd:dateTime
xsdInteger = xsdNS["integer"] #xsd:integer
xsdDecimal = xsdNS["decimal"] #xsd:decimal

# Class names
# (Start with capitals)
personClass = dreamNS['Person']
userClass = dreamNS['User']
pageClass = dreamNS['Page']
queryPageClass = dreamNS['QueryPage']
actorClass = dreamNS['Actor']
itemClass = dreamNS['Item']
otherItemClass = dreamNS['OtherItem']
placeClass = dreamNS['Place']
postClass = dreamNS['Post']
imageClass = dreamNS['Image']

# Object properties
hasTag = dreamNS['hasTag']
hasAuthor = dreamNS['hasAuthor']

# Datatype properties
name = dreamNS['name']
description = dreamNS['description']
itemId = dreamNS['itemId']
handle = dreamNS['handle']
dateCreated = dreamNS['dateCreated']
layout = dreamNS['layout']
profileImg = dreamNS['profileImg']
coverImg = dreamNS['coverImg']
urlSlug = dreamNS['urlSlug']

def createGraph():
	print("Creating graph")
	graph = ConjunctiveGraph()

	# "object is a class in our ontology"
	classTriples = [
	(personClass, rdfType, owlClass),
	(otherItemClass, rdfType, owlClass),
	(pageClass, rdfType, owlClass),
	(actorClass, rdfType, owlClass),
	(itemClass, rdfType, owlClass),
	(placeClass, rdfType, owlClass),
	(postClass, rdfType, owlClass),
	(imageClass, rdfType, owlClass)
	]

	classHierarchyTriples = [
	# items
	(actorClass, rdfsSubClassOf, itemClass),
	(userClass, rdfsSubClassOf, personClass),
	(userClass, rdfsSubClassOf, actorClass),
	(pageClass, rdfsSubClassOf, actorClass),
	(otherItemClass, rdfsSubClassOf, itemClass),
	(personClass, rdfsSubClassOf, itemClass),
	(placeClass, rdfsSubClassOf, itemClass),
	(postClass, rdfsSubClassOf, itemClass),
	(imageClass, rdfsSubClassOf, postClass),
	]

	propertyTriples = [
	# DATATYPE PROPERTIES

	# id (everything has an integer ID - timestamp + random number)
	(itemId, rdfType, owlDatatypeProperty),
	(itemId, rdfsDomain, itemClass),
	(itemId, rdfsRange, xsdInteger),

	# name (could be the name of a person, the title of a post, etc)
	(name, rdfType, owlDatatypeProperty),
	(name, rdfsDomain, itemClass),
	(name, rdfsRange, xsdString),

	# handle (unique string, only for users and pages. Prefixed with "@" in URL)
	(handle, rdfType, owlDatatypeProperty),
	(handle, rdfsDomain, actorClass),
	(handle, rdfsRange, xsdString),

	# URL slug (only for posts)
	(urlSlug, rdfType, owlDatatypeProperty),
	(urlSlug, rdfsDomain, postClass),
	(urlSlug, rdfsRange, xsdString),

	# description (could be the text of a post, or the blurb for a person)
	(description, rdfType, owlDatatypeProperty),
	(description, rdfsDomain, itemClass),
	(description, rdfsRange, xsdString),

	# Date created
	(dateCreated, rdfType, owlDatatypeProperty),
	(dateCreated, rdfsDomain, postClass),
	(dateCreated, rdfsRange, xsdDateTime),

	# Layout
	(layout, rdfType, owlDatatypeProperty),
	(layout, rdfsDomain, itemClass),
	(layout, rdfsRange, xsdString),

	# Featured image
	(profileImg, rdfType, owlDatatypeProperty),
	(profileImg, rdfsDomain, itemClass),
	(profileImg, rdfsRange, xsdString),

	# Cover image
	(coverImg, rdfType, owlDatatypeProperty),
	(coverImg, rdfsDomain, itemClass),
	(coverImg, rdfsRange, xsdString),

	# OBJECT PROPERTIES

	# Tag
	(hasTag, rdfType, owlObjectProperty),
	(hasTag, rdfsDomain, itemClass),
	(hasTag, rdfsRange, itemClass),

	# Author
	(hasAuthor, rdfType, owlObjectProperty),
	(hasAuthor, rdfsDomain, postClass),
	(hasAuthor, rdfsRange, actorClass),

	]

	# Save graph structure
	for triple in classTriples:
		graph.add(triple)

	for triple in classHierarchyTriples:
		graph.add(triple)

	for triple in propertyTriples:
		graph.add(triple)


	return graph
