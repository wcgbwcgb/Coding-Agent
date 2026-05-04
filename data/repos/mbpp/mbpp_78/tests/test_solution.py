from solution import *


def test_mbpp_generated() -> None:
    assert count_With_Odd_SetBits(5) == 3
    assert count_With_Odd_SetBits(10) == 5
    assert count_With_Odd_SetBits(15) == 8
