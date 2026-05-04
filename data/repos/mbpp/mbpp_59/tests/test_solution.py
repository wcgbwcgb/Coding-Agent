from solution import *


def test_mbpp_generated() -> None:
    assert is_octagonal(5) == 65
    assert is_octagonal(10) == 280
    assert is_octagonal(15) == 645
