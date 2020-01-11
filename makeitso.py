#!/usr/local/bin/python3

import markdown2

print(markdown2.markdown("*boo!*"))  # or use `html = markdown_path(PATH)`
# u'<p><em>boo!</em></p>\n'