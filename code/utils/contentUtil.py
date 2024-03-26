import re

# Remove URLs, non-ASCII characters, multiple spaces, newlines, and carriage returns
def clean(content):
    if (content is None or content == '' or len(content) == 0):
        return [], content

    # Extract URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = url_pattern.findall(content)

    # Remove URLs
    content = url_pattern.sub('', content)

    # Remove non-ASCII characters
    unicode_pattern = re.compile(r'[^\x00-\x7F]+')
    content = unicode_pattern.sub('', content)

    # Remove multiple spaces
    multiple_spaces_pattern = re.compile(r'\s\s+')
    content = multiple_spaces_pattern.sub(' ', content)

    # Remove empty square brackets
    empty_brackets_pattern = re.compile(r'\[\s*\]')
    content = empty_brackets_pattern.sub('', content)

    # Remove newlines and carriage returns
    content = content.replace('\r', '').replace('\n', '')

    # Remove consecutive symbols e.g ||| !!!!! -----
    consecutive_symbol_pattern = re.compile(r'(\W)\1{2,}')
    content = consecutive_symbol_pattern.sub(r'\1', content)

    return urls, content.strip()