from solution import *


def test_mbpp_generated() -> None:
    assert check("01010101010") == "Yes"
    assert check("name0") == "No"
    assert check("101") == "Yes"
