#!/usr/local/bin/python3

import markdown2, os, re, rdflib
from rdflib import Namespace

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
actorClass = dreamNS['Actor']
itemClass = dreamNS['Item']
otherItemClass = dreamNS['OtherItem']
placeClass = dreamNS['Place']
postClass = dreamNS['Post']
imageClass = dreamNS['Image']

# Object properties
hasTag = dreamNS['hasTag']
hasAuthor = dreamNS['hasAuthor']
featuredImage = dreamNS['featuredImage']

# Datatype properties
name = dreamNS['name']
description = dreamNS['description']
itemId = dreamNS['itemId']
handle = dreamNS['handle']
dateCreated = dreamNS['dateCreated']

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

	# handle (unique string, only for users and pages. Prefixed with "@")
	(handle, rdfType, owlDatatypeProperty),
	(handle, rdfsDomain, actorClass),
	(handle, rdfsRange, xsdString),

	# description (could be the text of a post, or the blurb for a person)
	(description, rdfType, owlDatatypeProperty),
	(description, rdfsDomain, itemClass),
	(description, rdfsRange, xsdString),

	(dateCreated, rdfType, owlDatatypeProperty),
	(dateCreated, rdfsDomain, postClass),
	(dateCreated, rdfsRange, xsdDateTime),

	# OBJECT PROPERTIES

	# Tag
	(hasTag, rdfType, owlObjectProperty),
	(hasTag, rdfsDomain, itemClass),
	(hasTag, rdfsRange, itemClass),

	# Author
	(hasAuthor, rdfType, owlObjectProperty),
	(hasAuthor, rdfsDomain, personClass),
	(hasAuthor, rdfsRange, postClass),
]



from rdflib import ConjunctiveGraph
graph = ConjunctiveGraph()

for triple in classTriples:
	graph.add(triple)

for triple in classHierarchyTriples:
	graph.add(triple)

for triple in propertyTriples:
	graph.add(triple)



################
# OUTPUT GRAPH
################

graph.serialize(destination='dream-network9.ttl', format='turtle')









################
# INSTANCE DATA
################

# When you find an item, store it by its ID
itemId = 'b3eae388-e8d2-4834-8284-a170aef489f3'
newitem = dreamNS[itemId]


# Add properties to the item










rootdir = os.getcwd() + '/_items'

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.startswith('.'):
			continue
		lines = []
		filepath = os.path.join(subdir, file)
		print(os.path.join(subdir, file))

		with open(filepath,'r') as f:
			for line in f:
				lines.append(line)

		htmlstring = markdown2.markdown("\n".join(line for line in lines))
		writepath = os.getcwd() + '/_site/' + file

		# renamee is the file getting renamed, pre is the part of file name before extension and ext is current extension
		writepath = re.sub('.md$', '.html', writepath)
		newfile = open(writepath, "w")
		newfile.write(htmlstring)
		newfile.close()
		
		
