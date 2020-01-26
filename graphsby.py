#!/usr/local/bin/python3

import sys
sys.path.insert(1, './modules')

import markdown2, os, re, rdflib
from rdflib import Namespace, Literal
from pathlib import Path
from get_yaml_var import get_yaml_var
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Vars
cwd = os.getcwd()
config_path = cwd + "/_config.yml"



index_page = get_yaml_var("home", config_path)
site_name = get_yaml_var("site", config_path)
print("### Generating site ###")
print("Site: ", end="")
print(site_name)
print("Homepage: ", end="")
print(index_page)


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
urlSlug = dreamNS['urlSlug']

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

rootdir = cwd + '/_items'

# Instance data in graph
instances = []

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.startswith('.'):
			continue
		
		filepath = os.path.join(subdir, file)

		reading_yaml = False
		lines = []
		yaml_lines = []
		with open(filepath,'r') as f:
			for line in f:
				if line == '---\n' and reading_yaml is False:
					reading_yaml = True 
					continue
				elif line == '---\n' and reading_yaml is True:
					reading_yaml = False
					continue

				# if line

				# Append line to either YAML or main file 
				if reading_yaml: 
					yaml_lines.append(line)
				else: 
					lines.append(line)

		yaml_document = "".join(yaml_lines)
		pyyam = yaml.load(yaml_document, Loader=yaml.FullLoader);

		htmlstring = markdown2.markdown("\n".join(line for line in lines))

		writepath = cwd + '/_site/' + file

		# If type is a user, make handle/index.html
		if "type" in pyyam.keys():
			if pyyam["type"] == "user" or pyyam["type"] == "page":
				user_folderpath = cwd + '/_site/' + pyyam["handle"]
				Path(user_folderpath).mkdir(parents=True, exist_ok=True)
				user_writepath = user_folderpath + "/index.html"
				new_userfile = open(user_writepath, "w")
				new_userfile.write(htmlstring)
				new_userfile.close()
			elif pyyam["type"] == "post":
				post_folderpath = cwd + '/_site/' + str(pyyam["itemId"])
				Path(post_folderpath).mkdir(parents=True, exist_ok=True)
				user_writepath = post_folderpath + "/index.html"
				user_writepath2 = post_folderpath + "/" + re.sub('.md$', '.html', file)
				new_userfile = open(user_writepath, "w")
				new_userfile.write(htmlstring)
				new_userfile.close()
				new_userfile = open(user_writepath2, "w")
				new_userfile.write(htmlstring)
				new_userfile.close()

		# Create index.html file based on "home" in config.yml
		if "handle" in pyyam.keys():
			if pyyam["handle"] == index_page:
				home_writepath = cwd + '/_site/index.html'
				home_page = open(home_writepath, "w")
				home_page.write(htmlstring)
				home_page.close()




		################
		# INSTANCE DATA
		################

		# Map YAML to item classes
		classMap = {
			"person": personClass,
			"page": pageClass,
			"user": userClass,
			"post": postClass
		}

		# When you find an item, store it by its ID
		docId = pyyam['itemId']
		newItem = dreamNS[docId]

		# Add ID as property
		instances.append((newItem, itemId, Literal(docId, datatype=xsdString)))

		# Type of item (e.g. page, person)
		itemType = pyyam["type"]
		if itemType in classMap.keys():
			instances.append((newItem, rdfType, classMap[itemType]))

		# Add handle, if type is person or page
		if itemType == "user" or itemType == "page":
			if "handle" in pyyam.keys():
				instances.append((newItem, handle, Literal(pyyam['handle'], datatype=xsdString)))

		# Add URL slug, if item type is post. 
		if itemType == "post":
			if "urlSlug" in pyyam.keys():
				instances.append((newItem, urlSlug, Literal(pyyam['urlSlug'], datatype=xsdString)))

		# Title
		instances.append((newItem, name, Literal(pyyam['name'], datatype=xsdString)))
		# Description
		instances.append((newItem, description, Literal(htmlstring, datatype=xsdString)))
		# Layout
		instances.append((newItem, layout, Literal(pyyam['layout'], datatype=xsdString)))

		# Tags
		for tag in pyyam['tags']:
			print("", end="")



# Add all triples to the graph
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

graph.serialize(destination='dream-network15.ttl', format='turtle')


# Add properties to the item
		
		
