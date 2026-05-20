def count_common(words):
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    # order of first appearance
    unique = []
    seen = set()
    for word in words:
        if word not in seen:
            unique.append(word)
            seen.add(word)
    # sort by count descending, then by first appearance
    pos = {word: i for i, word in enumerate(unique)}
    sorted_words = sorted(unique, key=lambda w: (-counts[w], pos[w]))
    # return only the 4 most common words
    return [(w, counts[w]) for w in sorted_words[:4]]
