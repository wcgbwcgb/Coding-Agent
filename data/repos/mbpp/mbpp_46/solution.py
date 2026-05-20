def distinct_check(data):
    return len(data) == len(set(data))

test_distinct = distinct_check
test_distinct.__test__ = False
