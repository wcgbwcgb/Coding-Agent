from solution import *


def test_mbpp_generated() -> None:
    assert zigzag(4, 3) == 5
    assert zigzag(4, 2) == 4
    assert zigzag(3, 1) == 1
