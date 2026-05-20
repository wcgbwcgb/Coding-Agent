def count_Substring_With_Equal_Ends(s: str) -> int:
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return sum(v * (v + 1) // 2 for v in freq.values())
