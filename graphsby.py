#!/usr/local/bin/python3

import markdown2, os, re

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
