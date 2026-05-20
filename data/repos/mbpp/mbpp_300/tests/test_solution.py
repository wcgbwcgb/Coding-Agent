from solution import *


def test_mbpp_generated() -> None:
    assert count_binary_seq(1) == 2.0
    assert count_binary_seq(2) == 6.0
    assert count_binary_seq(3) == 20.0
