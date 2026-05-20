from solution import *


def test_mbpp_generated() -> None:
    assert validate(1234) == True
    assert validate(51241) == False
    assert validate(321) == True
