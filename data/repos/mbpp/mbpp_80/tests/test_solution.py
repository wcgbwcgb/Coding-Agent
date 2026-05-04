from solution import *


def test_mbpp_generated() -> None:
    assert tetrahedral_number(5) == 35.0
    assert tetrahedral_number(6) == 56.0
    assert tetrahedral_number(7) == 84.0
