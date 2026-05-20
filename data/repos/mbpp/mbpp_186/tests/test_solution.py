from solution import *


def test_mbpp_generated() -> None:
    assert check_literals('The quick brown fox jumps over the lazy dog.',['fox']) == 'Matched!'
    assert check_literals('The quick brown fox jumps over the lazy dog.',['horse']) == 'Not Matched!'
    assert check_literals('The quick brown fox jumps over the lazy dog.',['lazy']) == 'Matched!'
