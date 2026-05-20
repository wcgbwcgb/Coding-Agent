from solution import *


def test_mbpp_generated() -> None:
    assert check_Validity(1,2,3) == False
    assert check_Validity(2,3,5) == False
    assert check_Validity(7,10,5) == True
