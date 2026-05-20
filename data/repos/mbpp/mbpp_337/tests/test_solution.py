from solution import *


def test_mbpp_generated() -> None:
    assert text_match_word("python.")==('Found a match!')
    assert text_match_word("python.")==('Found a match!')
    assert text_match_word("  lang  .")==('Not matched!')
