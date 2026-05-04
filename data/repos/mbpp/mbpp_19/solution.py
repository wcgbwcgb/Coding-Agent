def test_duplicate(arraynums):
    return len(set(arraynums)) != len(arraynums)

test_duplicate.__test__ = False
