from solution import *


def test_mbpp_generated() -> None:
    assert check(70) == False
    assert check(23) == False
    assert check(73) == True
