from solution import *


def test_mbpp_generated() -> None:
    assert dig_let("python")==(6,0)
    assert dig_let("program")==(7,0)
    assert dig_let("python3.0")==(6,2)
