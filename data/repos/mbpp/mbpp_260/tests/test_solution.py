from solution import *


def test_mbpp_generated() -> None:
    assert newman_prime(3) == 7 
    assert newman_prime(4) == 17
    assert newman_prime(5) == 41
