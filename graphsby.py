#!/usr/local/bin/python3

import markdown2, os, re, rdflib
from rdflib import Namespace

# Namespace declarations
# RDFlib uses square brackets to show prefix and literals
owlNS = Namespace("http://www.w3.org/2002/07/owl#")
owlClass = owlNS["Class"]
owlObjectProperty = owlNS["ObjectProperty"]
owlDatatypeProperty = owlNS["DatatypeProperty"]
rdfNS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfProperty = rdfNS["Property"]
rdfType = rdfNS["type"]
rdfsNS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
rdfsSubClassOf = rdfsNS["subClassOf"]
rdfsDomain = rdfsNS["domain"]
rdfsRange = rdfsNS["range"]
xsdNS = Namespace("http://www.w3.org/2001/XMLSchema#")
xsdString = xsdNS["string"]
dreamNS = Namespace("https://www.dannykennedy.co/dnj-ontology#")

# Class names
# (Start with capitals)
personClass = dreamNS['Person']
pageClass = dreamNS['Page']
thingClass = dreamNS['Thing']
placeClass = dreamNS['Place']

# Property names start with lowercase
name = dreamNS['name']
tag = dreamNS['tag']
orderContains = dreamNS['orderContains']
availableAt = dreamNS['availableAt']

# "object is a class in our ontology"
classTriples = [
	(dreamNS['Person'], rdfType, owlClass),
	(dreamNS['Page'], rdfType, owlClass),
	(dreamNS['Thing'], rdfType, owlClass),
	(dreamNS['Place'], rdfType, owlClass)
]









rootdir = os.getcwd() + '/_items'

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.startswith('.'):
			continue
		lines = []
		filepath = os.path.join(subdir, file)
		print(os.path.join(subdir, file))

		with open(filepath,'r') as f:
			for line in f:
				lines.append(line)

		htmlstring = markdown2.markdown("\n".join(line for line in lines))
		writepath = os.getcwd() + '/_site/' + file

		# renamee is the file getting renamed, pre is the part of file name before extension and ext is current extension
		writepath = re.sub('.md$', '.html', writepath)
		newfile = open(writepath, "w")
		newfile.write(htmlstring)
		newfile.close()
		
		
