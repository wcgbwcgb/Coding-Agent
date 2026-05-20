def sort_mixed_list(mixed_list):
    ints = sorted([x for x in mixed_list if isinstance(x, int)])
    strs = sorted([x for x in mixed_list if isinstance(x, str)])
    return ints + strs
