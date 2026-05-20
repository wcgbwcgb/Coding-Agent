from solution import *


def test_mbpp_generated() -> None:
    assert min_of_three(10,20,0)==0
    assert min_of_three(19,15,18)==15
    assert min_of_three(-10,-20,-30)==-30
