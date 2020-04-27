#!/usr/local/bin/python3

import yaml, markdown2
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load_file_to_object(filepath):

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

			# Append line to either YAML or main file 
			if reading_yaml: 
				yaml_lines.append(line)
			else: 
				lines.append(line)

	yaml_document = "".join(yaml_lines)
	pyyam = yaml.load(yaml_document);

	htmlstring = markdown2.markdown("\n".join(line for line in lines))

	pyyam["description"] = htmlstring

	f.close()

	return pyyam
