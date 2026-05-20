from solution import *


def test_mbpp_generated() -> None:
    assert hamming_Distance(4,8) == 2
    assert hamming_Distance(2,4) == 2
    assert hamming_Distance(1,2) == 2
