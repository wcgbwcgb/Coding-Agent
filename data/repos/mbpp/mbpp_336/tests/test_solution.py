from solution import *


def test_mbpp_generated() -> None:
    assert check_monthnum("February")==True
    assert check_monthnum("January")==False
    assert check_monthnum("March")==False
