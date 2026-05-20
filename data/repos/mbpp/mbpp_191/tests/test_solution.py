from solution import *


def test_mbpp_generated() -> None:
    assert check_monthnumber("February")==False
    assert check_monthnumber("June")==True
    assert check_monthnumber("April")==True
