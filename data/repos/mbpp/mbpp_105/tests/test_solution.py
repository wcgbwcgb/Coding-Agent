from solution import *


def test_mbpp_generated() -> None:
    assert count([True,False,True]) == 2
    assert count([False,False]) == 0
    assert count([True,True,True]) == 3
