def remove_dirty_chars(string, dirty_chars):
    dirty_set = set(dirty_chars)
    return "".join(c for c in string if c not in dirty_set)
