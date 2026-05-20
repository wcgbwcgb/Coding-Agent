from solution import *


def test_mbpp_generated() -> None:
    assert is_num_keith(14) == True
    assert is_num_keith(12) == False
    assert is_num_keith(197) == True
