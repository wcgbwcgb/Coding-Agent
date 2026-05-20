import re

def text_match(text):
    if re.fullmatch(r'[a-z]+_[a-z]+', text):
        return 'Found a match!'
    return 'Not matched!'
