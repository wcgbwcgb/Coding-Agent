from solution import *


def test_mbpp_generated() -> None:
    assert smartNumber(1) == 30
    assert smartNumber(50) == 273
    assert smartNumber(1000) == 2664
