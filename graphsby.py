#!/usr/local/bin/python3

#########
# IMPORTS
#########

# Libraries
import os, sys, jinja2
from rdflib import Namespace, Literal, ConjunctiveGraph
from pathlib import Path

# Custom functions in ./modules
sys.path.insert(1, './modules')
from copytree import copytree
from get_yaml_var import get_yaml_var
from load_file_to_object import load_file_to_object




# Vars
cwd = os.getcwd()
config_path = cwd + "/_config.yml"
index_page = get_yaml_var("home", config_path)
site_url = get_yaml_var("site", config_path)

# Template vars
# https://stackoverflow.com/questions/38642557/how-to-load-jinja-template-directly-from-filesystem
templateLoader = jinja2.FileSystemLoader(searchpath="./_templates")
templateEnv = jinja2.Environment(loader=templateLoader)
POST_TEMPLATE_FILE = "post.html"
PAGE_TEMPLATE_FILE = "page.html"
post_template = templateEnv.get_template(POST_TEMPLATE_FILE)
page_template = templateEnv.get_template(PAGE_TEMPLATE_FILE)


# Startup messages
print("### Generating site ###")
t = jinja2.Template("Site: {{ site_url }}")
print(t.render(site_url=site_url))
t = jinja2.Template("Homepage: {{ index_page }}")
print(t.render(index_page=index_page))

# Copy folders into _site
# Styles
style_folderpath = cwd + '/_site/styles'
Path(style_folderpath).mkdir(parents=True, exist_ok=True)
copytree(cwd + "/_styles/", cwd + "/_site/styles")
# Images
images_folderpath = cwd + '/_site/images'
Path(images_folderpath).mkdir(parents=True, exist_ok=True)
copytree(cwd + "/_images/", cwd + "/_site/images")
# TODO: Files


########################
# SET UP GRAPH STRUCTURE
########################

# Create graph
graph = ConjunctiveGraph()


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

# Save graph structure
for triple in classTriples:
	graph.add(triple)

for triple in classHierarchyTriples:
	graph.add(triple)

for triple in propertyTriples:
	graph.add(triple)






#################
# PARSE DOCUMENTS
#################

file_objects = []

for subdir, dirs, files in os.walk(cwd + '/_items'):
	for file in files:

		# Ignore hidden files
		if file.startswith('.'):
			continue

		# Load YAML/Markdown file to Python object
		filepath = os.path.join(subdir, file)
		pyyam = load_file_to_object(filepath)
		file_objects.append(pyyam)


##########################################################
# LOOP ONCE AND ADD INSTANCES (THE ACTUAL ITEMS / CONTENT)
##########################################################

instances = []

for pyyam in file_objects:

	# Map YAML descriptions to graph classes
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
	htmlstring = pyyam["description"]
	instances.append((newItem, description, Literal(htmlstring, datatype=xsdString)))
	# Layout
	instances.append((newItem, layout, Literal(pyyam['layout'], datatype=xsdString)))

# Add instances to the graph
for triple in instances: 
	graph.add(triple) 


###############################################
# LOOP AGAIN AND ADD TAGS (EDGES BETWEEN ITEMS)
###############################################

edges = []

for pyyam in file_objects:
	if 'tags' in pyyam.keys() and pyyam['tags'] is not None:
		for tag in pyyam['tags']:

			tag_value = list(tag.values())[0]

			# Find the object in the graph that the tag points to
			query_string = """
					PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
					SELECT DISTINCT ?itemId
				    WHERE {{
				    	?item dnj:handle|dnj:urlSlug "{string_identifier}"^^xsd:string .
				    	?item dnj:itemId ?itemId			   	
				   	}}""".format(string_identifier=tag_value)

			q = graph.query(query_string)

			# Naively assume there is only one result
			tag_item = ""
			for row in q:
				tag_item = row[0]

			# Append edge to edges array
			curr_item = pyyam["itemId"]
			if tag_item != "":
				edges.append((dreamNS[curr_item], hasTag, dreamNS[tag_item]))

# Add edges to the graph
for triple in edges: 
	graph.add(triple) 



################
# OUTPUT GRAPH
################

graph.serialize(destination='dream-network16.ttl', format='turtle')


################
# GENERATE PAGES
################
print("Total pages processed:", end=" ")
print(len(file_objects))

##########################################
# GET ALL ITEMS THAT HAVE TAGGED THAT PAGE
##########################################

for pyyam in file_objects:

	item_string_identifier = ""
	item_type = pyyam["type"]
	if item_type == "user" or item_type == "page":
		item_string_identifier = pyyam["handle"]
	elif item_type == "post":
		item_string_identifier = pyyam["urlSlug"]

	# Find all items that have tagged the current page
	query_string = """
				PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
		   		SELECT DISTINCT ?item ?name ?description ?itemId
		   		WHERE {{ 
		   		?currentItem dnj:handle|dnj:urlSlug "{string_identifier}"^^xsd:string .
		   		?item dnj:hasTag ?currentItem .
		   		?item dnj:name ?name .
		   		?item dnj:description ?description .
		   		?item dnj:itemId ?itemId
		   		}}""".format(string_identifier=item_string_identifier)

	q = graph.query(query_string)

	tagged_items = []
	for row in q:
		# Now find everything that this item is tagged with
		# This is literally Inception
		query_string = """
			PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
			SELECT DISTINCT ?littleTag ?tagName ?tagId ?textId ?tagType
			WHERE {{ 
				?item dnj:itemId "{id}"^^xsd:string .
				?item dnj:hasTag ?littleTag .
				?littleTag dnj:name ?tagName .
				?littleTag dnj:itemId ?tagId .
				?littleTag dnj:handle|dnj:urlSlug ?textId .
				?littleTag a ?tagType .
			}}""".format(id=row[3])
		tag_query = graph.query(query_string)

		# Create a tags array (for dem little tags on the cards)
		little_tags = []
		for lil_tag in tag_query:

			# Break down query object
			tagName = lil_tag[1]
			tagId = lil_tag[2]
			textId = lil_tag[3]
			tagType = lil_tag[4].split("#")[1]

			tagLink = ""
			if tagType == "Page" or tagType == "User":
				tagLink = "@" + textId
			else: 
				tagLink = tagId + "/" + textId

			little_tags.append({"name": tagName, "tagId": tagId, "textId": textId, "tagType":tagType, "tagLink":tagLink})

		tagged_items.append({"name": row[1], "description":row[2], "itemId":row[3], "tags": little_tags})


	full_html = ""
	# Layout 
	# Post is for individual posts, page is for pages with many posts
	if "layout" in pyyam.keys():
		if pyyam["layout"] == "post":
			full_html = post_template.render(render_item=pyyam, posts=tagged_items, site=site_url)
		else: 
			full_html = page_template.render(render_item=pyyam, posts=tagged_items, site=site_url)
	else: 
		full_html = post_template.render(render_item=pyyam, posts=tagged_items, site=site_url)


	# Path to write to (Dependant on type of item)
	folderpath = cwd + "/site/no-type"
	writepaths = []

	if "type" in pyyam.keys():
		# If type is a user or page, make @handle/index.html
		if pyyam["type"] == "user" or pyyam["type"] == "page":
			folderpath = cwd + '/_site/' + "@" + pyyam["handle"]
			writepaths.append(folderpath + "/index.html")
		elif pyyam["type"] == "post":
			folderpath = cwd + '/_site/' + str(pyyam["itemId"])
			writepaths.append(folderpath + "/index.html")
			writepaths.append(folderpath + "/" + pyyam["urlSlug"] + ".html")

	# Make the folder for the posts
	Path(folderpath).mkdir(parents=True, exist_ok=True)

	# Add post file(s) to the folder
	for path in writepaths:
		new_file = open(path, "w")
		new_file.write(full_html)
		new_file.close()


	# Create index.html file based on "home" in config.yml
	if "handle" in pyyam.keys():
		if pyyam["handle"] == index_page:
			home_writepath = cwd + '/_site/index.html'
			home_page = open(home_writepath, "w")
			home_page.write(full_html)
			home_page.close()






















		
		
