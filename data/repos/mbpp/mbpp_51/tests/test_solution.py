from solution import *


def test_mbpp_generated() -> None:
    assert check_equilateral(6,8,12)==False 
    assert check_equilateral(6,6,12)==False
    assert check_equilateral(6,6,6)==True
