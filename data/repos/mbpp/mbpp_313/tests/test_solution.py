from solution import *


def test_mbpp_generated() -> None:
    assert pos_nos([-1,-2,1,2]) == 1,2
    assert pos_nos([3,4,-5]) == 3,4
    assert pos_nos([-2,-3,1]) == 1
