from solution import *


def test_mbpp_generated() -> None:
    assert answer(3,8) == (3,6)
    assert answer(2,6) == (2,4)
    assert answer(1,3) == (1,2)
