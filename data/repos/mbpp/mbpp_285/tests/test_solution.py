from solution import *


def test_mbpp_generated() -> None:
    assert text_match_two_three("ac")==('Not matched!')
    assert text_match_two_three("dc")==('Not matched!')
    assert text_match_two_three("abbbba")==('Found a match!')
