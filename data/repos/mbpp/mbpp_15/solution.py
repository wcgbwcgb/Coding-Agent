import re

def split_lowerstring(text):
    return re.findall(r'[a-z][^a-z]*', text)
