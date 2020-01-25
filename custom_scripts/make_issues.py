#!/usr/local/bin/python3

import markdown2, os, re
import yaml
from issues_list import *
from id_gen import id_gen

dirname = "custom_scripts"
rootdir = os.getcwd()[:-len(dirname)-1] + '/_items'
print(rootdir)

# layout: post
# type: post
# itemId: PSYy-HU_
# name: "A Psychologist in the Tradition of William James and Gardner Murphy"
# shortDescription: "A Psychologist in the Tradition of William James and Gardner Murphy"
# urlSlug: "a-psychologist-in-the-tradition-of-william-james-and-gardner-murphy"
# tags:
#   - hasTag: "hi"
#   - hasTag: "bye"
# date: 2015-03-24
# featuredImg: dnj.png

# {'layout': 'post', 'type': 'post', 'itemId': 'PSYy-HU_', 'name': 'A Psychologist in the Tradition of William James and Gardner Murphy', 'shortDescription': 'A Psychologist in the Tradition of William James and Gardner Murphy', 'urlSlug': 'a-psychologist-in-the-tradition-of-william-james-and-gardner-murphy', 'tags': [{'hasTag': 'hi'}, {'hasTag': 'bye'}], 'date': datetime.date(2015, 3, 24), 'featuredImg': 'dnj.png'}

for issue in issues:
	print(issue)
	pyyaml = {}

	volume_number_str = issue["imgName"].split(".")[0]
	pdfName = issue["pdfName"]
	imgName = issue["imgName"]

	pyyaml['layout'] = 'page'
	pyyaml['type'] = 'post'
	pyyaml['itemId'] = id_gen()
	pyyaml['name'] = imgName + ": " + issue["title"]
	pyyaml['urlSlug'] = imgName
	pyyaml['tags'] = []
	pyyaml['tags'].append({"hasTag":"dreamnetwork"})
	volume_name = "dream-network-volume-" + volume_number_str
	pyyaml['tags'].append({"hasTag":volume_name})

	writepath = rootdir + "/" + imgName + ".md"
	newfile = open(writepath, "w")
	newfile.write("---\n")
	newfile.write(yaml.dump(pyyaml))
	newfile.write("---\n")
	newfile.write('<a href="files/pdfs/Volume_' + volume_number_str + '/' + pdfName + '" download="">Download issue ' + imgName + '</a>')
	newfile.close()















