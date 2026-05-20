from solution import *


def test_mbpp_generated() -> None:
    assert unique_Characters('aba') == False
    assert unique_Characters('abc') == True
    assert unique_Characters('abab') == False
