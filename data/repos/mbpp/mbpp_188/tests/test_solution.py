from solution import *


def test_mbpp_generated() -> None:
    assert prod_Square(25) == False
    assert prod_Square(30) == False
    assert prod_Square(16) == True
