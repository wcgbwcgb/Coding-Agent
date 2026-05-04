from solution import *


def test_mbpp_generated() -> None:
    assert tn_gp(1,5,2)==16
    assert tn_gp(1,5,4)==256
    assert tn_gp(2,6,3)==486
