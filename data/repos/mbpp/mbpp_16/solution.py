import re

def text_lowercase_underscore(text):
    if re.search('^[a-z]+_[a-z]+$', text):
        return 'Found a match!'
    return 'Not matched!'
