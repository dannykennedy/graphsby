#!/usr/local/bin/python3

import markdown2
import os
import re
import yaml
from issues_list import *
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

for issue in issues:
    pyyaml = {}

    imgName = issue["imgName"]
    dateCreated = issue["date"]
    filepath = rootdir + "/" + imgName + ".md"
    existing_id = get_item_id(filepath)

    print("existing_id found: ", end=" ")
    print(existing_id)

    # Use existing id, or make a new one if there isn't one
    if len(existing_id) > 1:
        pyyaml['itemId'] = existing_id
    else:
        pyyaml['itemId'] = id_gen()

    volume_number_str = issue["imgName"].split(".")[0]
    issue_number_str = issue["imgName"].split(".")[1].split("-")[0]
    pdfName = issue["pdfName"]
    pyyaml['layout'] = 'page'
    pyyaml['type'] = 'post'
    pyyaml['coverImg'] = imgName + "-cover.jpg"
    namestring = "Volume " + volume_number_str + \
        ", issue " + issue_number_str
    if issue["title"] != "":
        namestring += ": " + issue["title"]
    pyyaml['name'] = namestring

    pyyaml['urlSlug'] = imgName
    pyyaml['tags'] = []
    pyyaml['tags'].append({"hasAuthor": "dreamnetwork"})
    volume_name = "dream-network-volume-" + volume_number_str
    pyyaml['tags'].append({"hasTag": volume_name})
    pyyaml['tags'].append({"hasTag": "dreamnetwork"})
    pyyaml['dateCreated'] = dateCreated
    pyyaml['profileImg'] = imgName + "-rect.jpg"

    print(pyyaml)

    newfile = open(filepath, "w")
    newfile.write("---\n")
    newfile.write(yaml.dump(pyyaml))
    newfile.write("---\n")
    newfile.write('<img class="card-journal-img" src="../images/' +
                  imgName + '-rect.jpg"/>')
    newfile.write('<a href="../files/pdfs/Volume_' + volume_number_str +
                  '/' + pdfName + '" download="">Download issue ' + imgName + '</a>')
    newfile.write('<br><a href="../files/pdfs/Volume_' + volume_number_str +
                  '/' + pdfName + '">View online</a>')
    newfile.close()
