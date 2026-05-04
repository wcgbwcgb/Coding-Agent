from solution import *


def test_mbpp_generated() -> None:
    assert word_len("Hadoop") == False
    assert word_len("great") == True
    assert word_len("structure") == True
