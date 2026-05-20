from solution import *


def test_mbpp_generated() -> None:
    assert cal_electbill(75)==246.25
    assert cal_electbill(265)==1442.75
    assert cal_electbill(100)==327.5
