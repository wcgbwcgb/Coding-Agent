from solution import *


def test_mbpp_generated() -> None:
    assert check_integer("python")==False
    assert check_integer("1")==True
    assert check_integer("12345")==True
