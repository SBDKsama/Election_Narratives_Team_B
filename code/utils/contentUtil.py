# Summary:
# The `contentUtil.py` script provides a utility function `clean` to sanitize text content by removing unwanted characters, URLs, and formatting issues.

# Description:
# - The function `clean` takes a string input (`content`) and performs multiple regular expression operations to sanitize it.
# - It removes URLs using a regex that matches common URL patterns.
# - Non-ASCII characters are removed to ensure the text only contains basic ASCII characters, which simplifies encoding and further processing.
# - Multiple consecutive spaces are reduced to a single space to standardize spacing.
# - Newlines and carriage returns are stripped out to convert the content into a single continuous line.
# - The function also removes empty square brackets, which may be left over from data formatting or erroneous input.
# - The result is a cleaner, more standardized text string that is easier to handle for further text processing tasks like analysis or display.
# - Additionally, the function returns a list of extracted URLs and the cleaned content, providing both the sanitized text and any potentially useful link data.

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