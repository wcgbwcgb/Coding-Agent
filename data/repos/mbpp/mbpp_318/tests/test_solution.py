from solution import *


def test_mbpp_generated() -> None:
    assert max_volume(8) == 18
    assert max_volume(4) == 2
    assert max_volume(1) == 0
