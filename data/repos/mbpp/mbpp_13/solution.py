from collections import Counter

def count_common(words):
    return Counter(words).most_common(4)
