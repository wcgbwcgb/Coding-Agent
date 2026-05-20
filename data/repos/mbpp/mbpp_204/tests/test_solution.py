from solution import *


def test_mbpp_generated() -> None:
    assert count("abcc","c") == 2
    assert count("ababca","a") == 3
    assert count("mnmm0pm","m") == 4
