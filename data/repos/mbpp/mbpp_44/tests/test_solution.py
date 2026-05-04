from solution import *


def test_mbpp_generated() -> None:
    assert text_match_string(" python")==('Not matched!')
    assert text_match_string("python")==('Found a match!')
    assert text_match_string("  lang")==('Not matched!')
