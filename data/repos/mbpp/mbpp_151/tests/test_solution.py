from solution import *


def test_mbpp_generated() -> None:
    assert is_coprime(17,13) == True
    assert is_coprime(15,21) == False
    assert is_coprime(25,45) == False
