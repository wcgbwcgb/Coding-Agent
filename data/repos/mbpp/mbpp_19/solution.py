def test_duplicate(arraynums):
    return len(arraynums) != len(set(arraynums))

test_duplicate.__test__ = False
