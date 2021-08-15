def find_next_unclosed(text):
    """Finds the next unclosed HTML tag"""
    tag_stack = []

    # Get an iterator of all tags in file.
    tag_regex = re.compile(r'<[^>]*>', re.DOTALL)
    tags = tag_regex.finditer(text)

    for tag in tags:
        # If it is a closing tag check if it matches the last opening tag.
        if re.match(r'</[^>]*>', tag.group()):
            top_tag = tag_stack[-1]

            if tag_match(top_tag.group(), tag.group()):
                tag_stack.pop()
            else:
                unclosed = tag_stack.pop()
                return (unclosed.start(), unclosed.end())
        else:
            tag_stack.append(tag)

s=input("Your HTML Code ")
find_next_unclosed(s)
