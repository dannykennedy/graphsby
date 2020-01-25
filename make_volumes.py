#!/usr/local/bin/python3

import markdown2, os, re, rdflib
from rdflib import Namespace, Literal
import yaml
from pathlib import Path

# rootdir = str(Path(os.getcwd()).parents[2]) + '/_items'
rootdir = str(os.getcwd())[0] + '/_fuck'
print(rootdir)

# full_path = "path/to/directory"
# str(Path(full_path).parents[0])  # "path/to"


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

volume_sizes = [11, 10, 7, 6, 10, 14, 13, 13, 38, 23, 24, 25, 27, 27, 54, 59, 32, 31, 55, 5, 22, 19, 10, 9, 10, 8, 13, 6, 14, 6, 9, 6, 10]

print(len(volume_sizes))

for vol in range(1, 34):

	pyyaml = {}
	pyyaml['layout'] = 'page'
	pyyaml['type'] = 'post'
	pyyaml['itemId'] = vol
	pyyaml['name'] = "Volume " + str(vol)
	pyyaml['urlSlug'] = "dream-network-volume-" + str(vol)
	pyyaml['tags'] = []
	pyyaml['tags'].append({"hasTag":"dreamnetwork"})

	writepath = rootdir + "/Volume_" + str(vol) + ".md"
	newfile = open(writepath, "w")
	newfile.write("---\n")
	newfile.write(yaml.dump(pyyaml))
	newfile.write("---\n")
	newfile.write('<a href="files/Volume_' + str(vol) + '.zip" download>Volume ' + str(vol) + ' (.zip file, ' + str(volume_sizes[vol-1]) + 'mb</a>')
	newfile.close()















