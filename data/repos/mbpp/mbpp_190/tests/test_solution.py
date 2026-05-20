from solution import *


def test_mbpp_generated() -> None:
    assert count_Intgral_Points(1,1,4,4) == 4
    assert count_Intgral_Points(1,2,1,2) == 1
    assert count_Intgral_Points(4,2,6,4) == 1
