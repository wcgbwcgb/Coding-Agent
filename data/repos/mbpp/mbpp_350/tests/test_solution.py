from solution import *


def test_mbpp_generated() -> None:
    assert minimum_Length("mnm") == 1
    assert minimum_Length("abcda") == 3
    assert minimum_Length("abcb") == 2
