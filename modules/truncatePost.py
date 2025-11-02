import re, html5lib
from html5lib_truncation import truncate_html

def truncatePost(post_description, length, itemId):
	# print("Truncating post with id: " + itemId)
	if str(itemId) == 'bcpov6zfbsbr':
		print("Truncating post with id: " + itemId)
		# print(post_description)


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



def format_author_names(authors, max_length=30):
    """
    Format author names with truncation for display in cards.
    
    Args:
        authors: List of author dictionaries with 'name' key containing RDFlib Literal
        max_length: Maximum length for the final joined string
    
    Returns:
        Comma-separated string of author names, truncated to max_length
    """
    if not authors:
        return ""
    
    # Extract all names and join them
    names = []
    for author in authors:
        # Access as dictionary key and convert RDFlib Literal to string
        name = str(author['name'])
        names.append(name)
    
    # Join all names with commas
    joined_names = ", ".join(names)
    
    # Truncate the joined string if it exceeds max_length
    if len(joined_names) > max_length:
        return joined_names[:max_length-3] + "..."
    else:
        return joined_names