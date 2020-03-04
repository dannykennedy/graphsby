#!/usr/local/bin/python3

def map_class_to_css_tag(className):

	map = {
		"Page":"PAGE",
		"User":"PERSON",
		"Person":"PERSON", 
		"Place":"PLACE"
	}

	if className in map.keys():
		return map[className]
	else: 
		return "OTHER"