#!/usr/local/bin/python3

import markdown2
import os
import re
import yaml
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
# date: 2022-10-21
# profileImg: volume-1.jpg

# {'layout': 'post', 'type': 'post', 'itemId': 'PSYy-HU_', 'name': 'A Psychologist in the Tradition of William James and Gardner Murphy', 'shortDescription': 'A Psychologist in the Tradition of William James and Gardner Murphy', 'urlSlug': 'a-psychologist-in-the-tradition-of-william-james-and-gardner-murphy', 'tags': [{'hasTag': 'hi'}, {'hasTag': 'bye'}], 'date': datetime.date(2015, 3, 24), 'profileImg': 'dnj.png'}

volume_sizes = [11, 10, 7, 6, 10, 14, 13, 13, 38, 23, 24, 25, 27, 27,
                54, 59, 32, 31, 55, 5, 22, 19, 10, 9, 10, 8, 13, 6, 14, 6, 9, 6, 10]

print(len(volume_sizes))

for vol in range(1, 34):

    filepath = rootdir + "/Volume_" + str(vol) + ".md"
    existing_id = get_item_id(filepath)

    pyyaml = {}

    # Use existing id, or make a new one if there isn't one
    if len(existing_id) > 1:
        pyyaml['itemId'] = existing_id
    else:
        pyyaml['itemId'] = id_gen()

    pyyaml['layout'] = 'page'
    pyyaml['type'] = 'post'
    pyyaml['name'] = "Volume " + str(vol)
    pyyaml['profileImg'] = "volume-" + str(vol) + ".jpg"
    pyyaml['urlSlug'] = "dream-network-volume-" + str(vol)
    pyyaml['tags'] = []
    pyyaml['tags'].append({"hasAuthor": "dreamnetwork"})

    writepath = rootdir + "/Volume_" + str(vol) + ".md"
    newfile = open(writepath, "w")
    newfile.write("---\n")
    newfile.write(yaml.dump(pyyaml))
    newfile.write("---\n")
    newfile.write('<a href="../files/Volume_' + str(vol) + '.zip" download>Volume ' +
                  str(vol) + ' (.zip file, ' + str(volume_sizes[vol-1]) + 'mb)</a>')
    newfile.close()
