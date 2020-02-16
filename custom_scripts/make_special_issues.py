#!/usr/local/bin/python3

import markdown2
import os
import re
import yaml
from special_publications import *
from id_gen import id_gen
from get_item_id import get_item_id

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
# profileImg: dnj.png

# {'layout': 'post', 'type': 'post', 'itemId': 'PSYy-HU_', 'name': 'A Psychologist in the Tradition of William James and Gardner Murphy', 'shortDescription': 'A Psychologist in the Tradition of William James and Gardner Murphy', 'urlSlug': 'a-psychologist-in-the-tradition-of-william-james-and-gardner-murphy', 'tags': [{'hasTag': 'hi'}, {'hasTag': 'bye'}], 'date': datetime.date(2015, 3, 24), 'profileImg': 'dnj.png'}

for pub in special_publications:
    print(pub)
    pyyaml = {}

    imgName = pub["imgName"]
    filepath = rootdir + "/" + imgName + ".md"
    existing_id = get_item_id(filepath)

    # Use existing id, or make a new one if there isn't one
    if len(existing_id) > 1:
        pyyaml['itemId'] = existing_id
    else:
        pyyaml['itemId'] = id_gen()

    volume_number_str = pub["imgName"].split(".")[0]
    pdfName = pub["pdfName"]
    pyyaml['layout'] = 'page'
    pyyaml['type'] = 'post'
    pyyaml['name'] = pub["title"]
    pyyaml['urlSlug'] = imgName
    pyyaml['tags'] = []
    pyyaml['dateCreated'] = pub['dateCreated']
    pyyaml['profileImg'] = imgName + "-sml.jpg"
    pyyaml['tags'].append({"hasTag": "dreamnetwork"})
    pyyaml['tags'].append({"hasAuthor": pub["author"]})
    pyyaml['tags'].append({"hasTag": pub["author"]})
    pyyaml['tags'].append({"hasTag": "special-publications"})

    newfile = open(filepath, "w")
    newfile.write("---\n")
    newfile.write(yaml.dump(pyyaml))
    newfile.write("---\n")
    newfile.write('<img class="card-journal-img" src="../images/' +
                  imgName + '-rect.jpg"/>')
    newfile.write('<a href="../files/pdfs/Volume_publications/' +
                  pdfName + '" download="">Download</a>')
    newfile.close()
