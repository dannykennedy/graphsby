import re, html5lib
from html5lib_truncation import truncate_html

def truncatePost(post_description, length):
	truncated_desc = truncate_html(post_description, length, end="...", break_words=True)
	# Remove lists
	truncated_desc = re.sub("(<ol.*?ol>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	truncated_desc = re.sub("(<ul.*?ul>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	truncated_desc = re.sub("(<li.*?li>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	# Remove hr
	truncated_desc = re.sub("(<hr.*?>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	# Remove images
	truncated_desc = re.sub("(<img.*?>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	# Remove iframes
	truncated_desc = re.sub("(<div class=\"media-item resp-container\">.*</div>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	# Remove empty <p> tags
	truncated_desc = re.sub("(<p></p>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	# Remove break tags
	truncated_desc = re.sub("(<br/?>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	# Remove pre tags
	truncated_desc = re.sub("(<pre>[^\<]*<\/pre>)", "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
	# Remove captions
	truncated_desc = re.sub('<!--nopreview-->.*<!--/nopreview-->', "", truncated_desc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)

	return truncated_desc