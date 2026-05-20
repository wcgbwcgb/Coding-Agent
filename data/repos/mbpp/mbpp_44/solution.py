import re

def text_match_string(text):
    return 'Found a match!' if re.match(r'^\w', text) else 'Not matched!'
