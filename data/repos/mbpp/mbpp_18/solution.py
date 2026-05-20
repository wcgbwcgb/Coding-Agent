def str_to_list(string):
    return list(string)


def remove_dirty_chars(s1: str, s2: str) -> str:
    """Return a string with characters from s1 that are not in s2."""
    dirty = set(s2)
    return ''.join(ch for ch in s1 if ch not in dirty)
