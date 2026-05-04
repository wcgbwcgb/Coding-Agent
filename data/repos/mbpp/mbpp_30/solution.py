def count_Substring_With_Equal_Ends(s):
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    return sum(k * (k + 1) // 2 for k in counts.values())
