#!/usr/local/bin/python3

import markdown2, os, re, rdflib
from rdflib import Namespace, Literal
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_item_id(filepath):

	reading_yaml = False
	yaml_lines = []
	with open(filepath,'r') as f:
		for line in f:
			if line == '---\n' and reading_yaml is False:
				reading_yaml = True 
				continue
			elif line == '---\n' and reading_yaml is True:
				reading_yaml = False
				break

			# Append line to either YAML or main file 
			if reading_yaml: 
				yaml_lines.append(line)

	yaml_document = "".join(yaml_lines)
	pyyam = yaml.load(yaml_document, Loader=yaml.FullLoader);

	f.close()
	
	if "itemId" in pyyam.keys():
		return pyyam["itemId"]
	else: 
		return "0"