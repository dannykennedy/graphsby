#!/usr/local/bin/python3

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_yaml_var(var, filepath):
	yaml_lines = []
	with open(filepath,'r') as f:
		for line in f:
			yaml_lines.append(line)

	yaml_document = "".join(yaml_lines)
	pyyam = yaml.load(yaml_document, Loader=yaml.FullLoader);

	f.close()
	
	if var in pyyam.keys():
		return pyyam[var]
	else: 
		return "0"