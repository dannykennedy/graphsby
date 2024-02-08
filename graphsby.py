#!/usr/local/bin/python3

#########
# IMPORTS
#########

# Libraries
import os, sys, re, jinja2, calendar, html5lib, shutil, random
# import dateutil.parser # For converting xsd:datetime to something sensible
from rdflib import Namespace, Literal, ConjunctiveGraph
from pathlib import Path
from html5lib_truncation import truncate_html
from graph import *
from supporters import *

# Custom functions in ./modules
sys.path.insert(1, './modules')
from copytree import copytree
from formatDate import formatDate
from truncatePost import truncatePost
from get_yaml_var import get_yaml_var
from load_file_to_object import load_file_to_object
from map_class_to_css_tag import map_class_to_css_tag

# Vars
cwd = os.getcwd()
config_path = cwd + "/_config.yml"
index_page = get_yaml_var("home", config_path)
site_url = get_yaml_var("site", config_path)
port = get_yaml_var("port", config_path)
build = "prod"
build_folder = "/_site"

if sys.argv[1] in ["dev", "prod"]:
	build = sys.argv[1]

if build == "dev":
	build_folder = "/_build"
	site_url =  "http://localhost:" + str(port) + build_folder
	print("Running dev build on: ", end="")
	print(site_url)
else:
	print("Running prod build")

# Template vars
# https://stackoverflow.com/questions/38642557/how-to-load-jinja-template-directly-from-filesystem
templateLoader = jinja2.FileSystemLoader(searchpath="./_templates")
templateEnv = jinja2.Environment(loader=templateLoader)
POST_TEMPLATE_FILE = "post.html"
PAGE_TEMPLATE_FILE = "page.html"
post_template = templateEnv.get_template(POST_TEMPLATE_FILE)
page_template = templateEnv.get_template(PAGE_TEMPLATE_FILE)
POST_SNIPPET_LENGTH = 150

# Startup messages
print("### Generating site ###")
t = jinja2.Template("Site: {{ site_url }}")
print(t.render(site_url=site_url))
t = jinja2.Template("Homepage: {{ index_page }}")
print(t.render(index_page=index_page))

# Copy folders into build folder
# Styles
style_folderpath = cwd + build_folder + '/styles'
# First delete the existing one
if os.path.exists(style_folderpath):
	shutil.rmtree(style_folderpath)
Path(style_folderpath).mkdir(parents=True, exist_ok=True)
copytree(cwd + "/_styles/", cwd + build_folder + "/styles")
# Scripts
scripts_folderpath = cwd + build_folder + '/scripts'
# First delete the existing one
if os.path.exists(scripts_folderpath):
	shutil.rmtree(scripts_folderpath)
	print("Deleted existing scripts folder")
Path(scripts_folderpath).mkdir(parents=True, exist_ok=True)
copytree(cwd + "/scripts/", cwd + build_folder + "/scripts")
# Images
images_folderpath = cwd + build_folder + '/images'
Path(images_folderpath).mkdir(parents=True, exist_ok=True)
copytree(cwd + "/_images/", cwd + build_folder + "/images")
# Fonts 
fonts_folderpath = cwd + build_folder + '/fonts'
fonts_folderpath2 = cwd + build_folder + 'styles/fonts'
Path(fonts_folderpath).mkdir(parents=True, exist_ok=True)
Path(fonts_folderpath2).mkdir(parents=True, exist_ok=True)
copytree(cwd + "/fonts/", cwd + build_folder + "/styles/fonts")
copytree(cwd + "/fonts/", cwd + build_folder + "/fonts")

# Random images to assign if there's no article image
random_imgs = [
	"1.3-sml.jpg",
	"1.2-sml.jpg",
	"1.5-sml.jpg",
	"1.8-sml.jpg",
	"2.4-sml.jpg",
]

# TODO: Files

##############
# CREATE GRAPH
##############
graph = createGraph()


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
# 1) LOOP ONCE AND ADD INSTANCES (THE ACTUAL ITEMS / CONTENT)
##########################################################

instances = []

print("Building graph nodes")
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
		if "dateCreated" in pyyam.keys():
			instances.append((newItem, dateCreated, Literal(pyyam["dateCreated"], datatype=xsdDateTime )))

	# Title
	instances.append((newItem, name, Literal(pyyam['name'], datatype=xsdString)))
	# Description
	htmlstring = pyyam["description"]
	instances.append((newItem, description, Literal(htmlstring, datatype=xsdString)))
	# Layout
	instances.append((newItem, layout, Literal(pyyam['layout'], datatype=xsdString)))
	# Featured image
	if 'profileImg' in pyyam.keys():
		instances.append((newItem, profileImg, Literal(pyyam['profileImg'], datatype=xsdString)))
	# Cover image
	if 'coverImg' in pyyam.keys():
		instances.append((newItem, coverImg, Literal(pyyam['coverImg'], datatype=xsdString)))

	# Featured Label
	if 'featuredLabel' in pyyam.keys():
		instances.append((newItem, featuredLabel, Literal(pyyam['featuredLabel'], datatype=xsdString)))
	# Canonical URL
	if 'canonicalUrl' in pyyam.keys():
		instances.append((newItem, canonicalUrl, Literal(pyyam['canonicalUrl'], datatype=xsdString)))
		
# Add instances to the graph
for triple in instances:
	graph.add(triple)


###############################################
# 2) LOOP AGAIN AND ADD TAGS (EDGES BETWEEN ITEMS)
###############################################

edges = []

print("Building graph edges")
for pyyam in file_objects:
	# Add tags
	if 'tags' in pyyam.keys() and pyyam['tags'] is not None:
		for tag in pyyam['tags']:
			tag_key = list(tag.keys())[0] # e.g. hasTag, hasAuthor, etc.
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
			# This should be the case if string identifiers are unique
			tag_item = ""
			for row in q:
				tag_item = row[0]

			# Append edge to edges array
			curr_item = pyyam["itemId"]
			if tag_item != "":
				edges.append((dreamNS[curr_item], dreamNS[tag_key], dreamNS[tag_item]))

# Add edges to the graph
for triple in edges:
	graph.add(triple)



################
# OUTPUT GRAPH
################

graph.serialize(destination='dream-network16.ttl', format='turtle')
# graph.serialize(destination='dream-network16.nt', format='nt')
# graph.serialize(destination='dream-network16.xml', format='xml')


################
# GENERATE PAGES
################
print("Total pages processed:", end=" ")
print(len(file_objects))


##########################################
# GET ALL ITEMS THAT HAVE TAGGED THAT PAGE
##########################################

print("Finding linked items")
for pyyam in file_objects:

	# print(pyyam["name"])

	item_string_identifier = ""
	item_type = pyyam["type"]
	if item_type == "user" or item_type == "page":
		item_string_identifier = pyyam["handle"]
	elif item_type == "post":
		item_string_identifier = pyyam["urlSlug"]

	####################
	# 'TEST' - AUTHOR PAGE
	####################
	query_string = ""
	is_contributors_page = "handle" in pyyam.keys() and pyyam["handle"] == "dreamnetwork~contributors"
	is_main_page = "handle" in pyyam.keys() and pyyam["handle"] == "dreamnetwork"

	if is_contributors_page:

		# Find all dream network authors
		query_string = """
			PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
	   		SELECT DISTINCT ?item ?name ?description ?itemId ?dateCreated ?img ?stringid ?type
	   		WHERE {{
			?item a dnj:User .
			?item dnj:name ?name .
			?item dnj:itemId ?itemId .
			?item dnj:handle|dnj:urlSlug ?stringid .
			?item a ?type .
			OPTIONAL {{ ?item dnj:profileImg ?img }}
			OPTIONAL {{ ?item dnj:description ?description }}
			OPTIONAL {{ ?item dnj:dateCreated ?dateCreated }}
			}}
			ORDER BY ASC(?name)
			"""



		q = graph.query(query_string)
		print("result: ", end="")
		print(str(len(q)))

	else:
		# Find all items that have tagged the current page
		query_string = """
					PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
			   		SELECT DISTINCT ?item ?name ?description ?itemId ?dateCreated ?img ?stringid ?type ?relationship
			   		WHERE {{
			   		?currentItem dnj:handle|dnj:urlSlug "{string_identifier}"^^xsd:string .
			   		?item ?relationship ?currentItem .
			   		?item dnj:name ?name .
			   		?item dnj:description ?description .
			   		?item dnj:itemId ?itemId .
					?item dnj:dateCreated ?dateCreated .
					?item dnj:handle|dnj:urlSlug ?stringid .
					?item a ?type .
					OPTIONAL {{ ?item dnj:profileImg ?img }}
			   		}}
					ORDER BY DESC(?dateCreated)""".format(string_identifier=item_string_identifier)

	q = graph.query(query_string)

	tagged_items = []
	featured_items = []
	for row in q:
		# item_to_page_relation is the predicate that links the item to the page
		# e.g. hasAuthor, hasTag, featuredIn
		item_to_page_relation = ""
		if 0 <= 8 < len(row):


			item_to_page_relation = row[8].split("#")[1]
			# Check if row[8] includes the string "featured"
			# If so, add to featured items
			if "featured" in row[8]:
				print("featured")
				print(row[8])

		# Now find everything that this item is tagged with
		# This is literally Inception
		query_string = """
			PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
			SELECT DISTINCT ?littleTag ?tagName ?tagId ?textId ?tagType ?property ?image
			WHERE {{
				?item dnj:itemId "{id}"^^xsd:string .
				?item ?property ?littleTag .
				?littleTag dnj:name ?tagName .
				?littleTag dnj:itemId ?tagId .
				?littleTag dnj:handle|dnj:urlSlug ?textId .
				?littleTag a ?tagType .
				?littleTag dnj:profileImg ?image
			}}""".format(id=row[3])
		tag_query = graph.query(query_string)

		# Create a tags array (for dem little tags on the cards)
		little_tags = []
		authors = []
		for lil_tag in tag_query:

			# Break down query object
			tagName = lil_tag[1]
			tagId = lil_tag[2]
			textId = lil_tag[3]
			tagType = lil_tag[4].split("#")[1]
			relation = lil_tag[5].split("#")[1]
			image = lil_tag[6]

			tagLink = ""
			if tagType == "Page" or tagType == "User":
				tagLink = "@" + textId
			else:
				tagLink = tagId + "/" + textId

			cssTagClass = map_class_to_css_tag(tagType)

			if relation == "hasTag":
				little_tags.append({"name": tagName, "tagId": tagId, "textId": textId, "tagClass":cssTagClass, "tagLink":tagLink})
			elif relation == "hasAuthor":
				authors.append({"name": tagName, "tagId": tagId, "textId": textId, "tagClass":cssTagClass, "tagLink":tagLink, "profileImg": image})

		dateOfPost = row[4]
		date_string = ""
		if dateOfPost:
			date_string = formatDate(dateOfPost, "month")

		post_description = row[2]
		# Truncate
		truncated_desc = truncatePost(post_description, POST_SNIPPET_LENGTH).replace("...", "<span class='read-more'> ...read more</span>")

		card_type = row[7]
		string_identifier = row[6]
		item_id = row[3]
		card_link = ""
		card_type_literal = ""
		if card_type == userClass:
			card_link = "@" + string_identifier
			card_type_literal = "User"
		else:
			card_link = item_id + "/" + string_identifier
			card_type_literal = "Post"

		# Add to array
		item_to_add = {"name": row[1], "description":truncated_desc, "itemId":row[3], "dateCreated":date_string, "tags": little_tags, "authors": authors, "profileImg": row[5], "string_identifier": row[6], "card_link": card_link, "card_type": card_type_literal}

		if item_to_page_relation == "featuredIn":
			featured_items.append(item_to_add)
		# Fix this hack
		elif item_to_page_relation == "hasTag" or is_contributors_page:
			tagged_items.append(item_to_add)
		elif item_to_page_relation == "hasAuthor":
			continue
		else:
			continue

	full_html = ""
	# Layout
	# Post is for individual posts, page is for pages with many posts

	# Get things that item is tagged with
	query_string = """
			PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
			SELECT DISTINCT ?littleTag ?tagName ?tagId ?textId ?tagType ?property ?image
			WHERE {{
				?item dnj:itemId "{id}"^^xsd:string .
				?item ?property ?littleTag .
				?littleTag dnj:name ?tagName .
				?littleTag dnj:itemId ?tagId .
				?littleTag dnj:handle|dnj:urlSlug ?textId .
				?littleTag a ?tagType .
				?littleTag dnj:profileImg ?image
			}}""".format(id=pyyam["itemId"])
	tag_query = graph.query(query_string)

	# Create a tags array (for info about the post)
	little_tags = []
	other_articles_in_issue = {
		"issueName": "",
		"articles": []
	}
	authors = []
	for lil_tag in tag_query:

		# Break down query object
		tagName = lil_tag[1]
		tagId = lil_tag[2]
		textId = lil_tag[3]
		tagType = lil_tag[4].split("#")[1]
		relation = lil_tag[5].split("#")[1]
		image = lil_tag[6]

		tagLink = ""
		if tagType == "Page" or tagType == "User":
			tagLink = "@" + textId
		else:
			tagLink = tagId + "/" + textId

		cssTagClass = map_class_to_css_tag(tagType)

		if relation == "hasTag":
			little_tags.append({"name": tagName, "tagId": tagId, "textId": textId, "tagClass":cssTagClass, "tagLink":tagLink})
		elif relation == "inIssue":
			# Find the name of the issue and the other articles in it
			issue_query_string = """
				PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
				SELECT DISTINCT ?issueName ?articleName ?img ?articleId ?stringid
				WHERE {{
					?issue dnj:itemId "{issue_id}"^^xsd:string .
					?article dnj:inIssue ?issue .
					?article dnj:name ?articleName .
					?article dnj:itemId ?articleId .
					?article dnj:handle|dnj:urlSlug ?stringid .
					?issue dnj:name ?issueName .
					OPTIONAL {{ ?article dnj:profileImg ?img }}
				}}""".format(issue_id=tagId, article_id=pyyam["itemId"])

			issue_query = graph.query(issue_query_string)

			# Get issue name
			issue_name = ""
			if issue_query:
				for issue in issue_query:
					issue_name = issue[0]
					break
			other_articles_in_issue.update({"issueName": issue_name})

			for issue in issue_query:

				issue_name = issue[0]
				article_name = issue[1]
				article_profile_img = issue[2]
				article_id = str(issue[3])
				article_string_identifier = issue[4]

				display_profile_img = article_profile_img
				if article_profile_img is None:
					# Choose a random image for the display_profile_img
					# Based on the article name % length of random_imgs
					# This way, the same article will always have the same image
					# But it will be random for each article
					display_profile_img = random_imgs[len(article_name) % len(random_imgs)]

				# If it's not the current article, add it to the list of other articles in the issue
				if article_id != pyyam["itemId"]:
					other_articles_in_issue["articles"].append({"issue_name": issue_name, "name": article_name, "itemId": article_id, "profileImg": display_profile_img, "string_identifier": article_string_identifier, "url": '../' + article_id + '/' + article_string_identifier, "target": "_self"})

		elif relation == "hasAuthor":
			author = {"name": tagName, "tagId": tagId, "textId": textId, "tagClass":cssTagClass, "tagLink":tagLink, "profileImg": image, "articles": []}
			
			# RELATED ARTICLES - Find all articles that this author has written
			query_string = """
				PREFIX dnj:<https://www.dannykennedy.co/dnj-ontology#>
				SELECT DISTINCT ?item ?name ?itemId ?img ?stringid
				WHERE {{
					?item dnj:itemId ?itemId .
					?item dnj:handle|dnj:urlSlug ?stringid .
					?item dnj:name ?name .
					?item dnj:dateCreated ?dateCreated .
					?item dnj:hasAuthor ?author .
					?author dnj:itemId "{id}"^^xsd:string
					OPTIONAL {{ ?item dnj:profileImg ?img }}
				}}""".format(id=tagId)

			author_query = graph.query(query_string)

			for article in author_query:
				# Don't add the current article to the list of articles
				# Convert article[3] (the itemId) to a pure string
				# Otherwise it's a weird rdflib object
				article_name = article[1]
				article_id = str(article[2])
				article_profile_img = article[3]
				article_string_identifier = article[4]

				display_profile_img = article_profile_img
				if article_profile_img is None:
					# Choose a random image for the display_profile_img
					display_profile_img = random_imgs[len(article_name) % len(random_imgs)]

				if article_id != pyyam["itemId"]:
					author["articles"].append({"name": article_name, "itemId": article_id, "profileImg": display_profile_img, "string_identifier": article_string_identifier, "url": '../' + article_id + '/' + article_string_identifier, "target": "_self"})

			authors.append(author)

	pyyam["authors"] = authors
	pyyam["otherArticlesInIssue"] = other_articles_in_issue
	pyyam["tags"] = little_tags

	if "dateCreated" in pyyam.keys():
		dateOfPost = pyyam["dateCreated"]
		pyyam["dateString"] = formatDate(dateOfPost, "month")

	# Add supporters
	# If a supporter has a descriptionB, randomly choose one to display
	# And add the description to the url for AB testing
	# supporters = []
	# for supporter in supporters:
	# 	if "descriptionB" in supporter.keys():
	# 		# Randomly choose description or descriptionB
	# 		# 50/50 chance
	# 		if random.randint(0,1) == 0:
	# 			supporter["description"] = supporter["descriptionB"]
	# 			supporter["url"] = supporter["url"] + "&cta=b"
	# 		else:
	# 			supporter["url"] = supporter["url"] + "&cta=a"
			
	
	pyyam["supporters"] = supporters


	canonical_url = ""
	custom_keywords = ""
	if "canonicalUrl" in pyyam.keys():
		canonical_url = pyyam["canonicalUrl"]
	elif "handle" in pyyam.keys():
		canonical_url = site_url + "@" + pyyam["handle"]
		custom_keywords = pyyam["name"] + ", "
	else: 
		canonical_url = site_url + str(pyyam["itemId"]) + "/" + pyyam["urlSlug"]
	


	if "layout" in pyyam.keys():
		if pyyam["layout"] == "post":
			full_html = post_template.render(is_main_page=is_main_page, render_item=pyyam, featured_items=featured_items, posts=tagged_items, site_url=site_url, canonical_url=canonical_url, custom_keywords=custom_keywords)
		else:
			full_html = page_template.render(is_main_page=is_main_page, render_item=pyyam, featured_items=featured_items, posts=tagged_items, site_url=site_url, canonical_url=canonical_url, custom_keywords=custom_keywords)
	else:
		full_html = post_template.render(is_main_page=is_main_page, render_item=pyyam, featured_items=featured_items, posts=tagged_items, site_url=site_url, canonical_url=canonical_url, custom_keywords=custom_keywords)

	# Path to write to (Dependant on type of item)
	folderpath = cwd + "/site/no-type"
	writepaths = []

	if "type" in pyyam.keys():
		# If type is a user or page, make @handle/index.html
		if pyyam["type"] == "user" or pyyam["type"] == "page":
			folderpath = cwd + build_folder + "/@" + pyyam["handle"]
			writepaths.append(folderpath + "/index.html")
		elif pyyam["type"] == "post":
			folderpath = cwd + build_folder + "/" + str(pyyam["itemId"])
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
			home_writepath = cwd + build_folder + '/index.html'
			home_page = open(home_writepath, "w")
			home_page.write(full_html)
			home_page.close()

print("\nDone")
























