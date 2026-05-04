from solution import *


def test_mbpp_generated() -> None:
    assert split_lowerstring("AbCd")==['bC','d']
    assert split_lowerstring("Python")==['y', 't', 'h', 'o', 'n']
    assert split_lowerstring("Programming")==['r', 'o', 'g', 'r', 'a', 'm', 'm', 'i', 'n', 'g']
