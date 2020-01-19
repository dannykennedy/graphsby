#!/usr/local/bin/python3

import markdown2, os, re, rdflib
from rdflib import Namespace, Literal
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


document = """
  a: 1
  b:
    c: 3
    d: 4
"""


pyyam = yaml.load(document, Loader=yaml.FullLoader);
print(pyyam)

print(yaml.dump(yaml.load(document, Loader=yaml.FullLoader)))


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

# Datatype properties
name = dreamNS['name']
description = dreamNS['description']
itemId = dreamNS['itemId']
handle = dreamNS['handle']
dateCreated = dreamNS['dateCreated']
layout = dreamNS['layout']
featuredImage = dreamNS['featuredImage']

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

	# Date created
	(dateCreated, rdfType, owlDatatypeProperty),
	(dateCreated, rdfsDomain, postClass),
	(dateCreated, rdfsRange, xsdDateTime),

	# Layout
	(layout, rdfType, owlDatatypeProperty),
	(layout, rdfsDomain, itemClass),
	(layout, rdfsRange, xsdString),

	# OBJECT PROPERTIES

	# Tag
	(hasTag, rdfType, owlObjectProperty),
	(hasTag, rdfsDomain, itemClass),
	(hasTag, rdfsRange, itemClass),

	# Author
	(hasAuthor, rdfType, owlObjectProperty),
	(hasAuthor, rdfsDomain, postClass),
	(hasAuthor, rdfsRange, personClass),
]






#################
# PARSE DOCUMENTS
#################



rootdir = os.getcwd() + '/_items'

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.startswith('.'):
			continue
		lines = []
		filepath = os.path.join(subdir, file)
		print(os.path.join(subdir, file))

		reading_yaml = False
		yaml_lines = []
		with open(filepath,'r') as f:
			for line in f:
				if line == '---\n' and reading_yaml is False:
					reading_yaml = True 
					print("yay!")
				elif line == '---\n' and reading_yaml is True:
					reading_yaml = False

				# if line

				# Append line to either YAML or main file 
				print(reading_yaml)
				# print(line)
				if reading_yaml: 
					yaml_lines.append(line)
				else: 
					lines.append(line)



				

		htmlstring = markdown2.markdown("\n".join(line for line in lines))
		writepath = os.getcwd() + '/_site/' + file

		# renamee is the file getting renamed, pre is the part of file name before extension and ext is current extension
		writepath = re.sub('.md$', '.html', writepath)
		newfile = open(writepath, "w")
		newfile.write(htmlstring)
		newfile.close()

################
# INSTANCE DATA
################

# When you find an item, store it by its ID
itemId = 'DBcy-HU_'
newItem = dreamNS[itemId]

instances = [

	# Customers
	(newItem, rdfType, itemClass),
	(newItem, description, Literal(htmlstring, datatype=xsdString)),

]

from rdflib import ConjunctiveGraph
graph = ConjunctiveGraph()

for triple in classTriples:
	graph.add(triple)

for triple in classHierarchyTriples:
	graph.add(triple)

for triple in propertyTriples:
	graph.add(triple)

for triple in instances: 
	graph.add(triple) 



################
# OUTPUT GRAPH
################

graph.serialize(destination='dream-network11.ttl', format='turtle')


# Add properties to the item
		
		
