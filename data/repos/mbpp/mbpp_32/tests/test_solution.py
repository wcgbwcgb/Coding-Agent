from solution import *


def test_mbpp_generated() -> None:
    assert max_Prime_Factors(15) == 5
    assert max_Prime_Factors(6) == 3
    assert max_Prime_Factors(2) == 2
