from solution import *


def test_mbpp_generated() -> None:
    assert find_ways(4) == 2
    assert find_ways(6) == 5
    assert find_ways(8) == 14
