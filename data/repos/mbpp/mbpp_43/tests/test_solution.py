from solution import *


def test_mbpp_generated() -> None:
    assert text_match("aab_cbbbc") == 'Found a match!'
    assert text_match("aab_Abbbc") == 'Not matched!'
    assert text_match("Aaab_abbbc") == 'Not matched!'
