from solution import *


def test_mbpp_generated() -> None:
    assert rearange_string("aab")==('aba')
    assert rearange_string("aabb")==('abab')
    assert rearange_string("abccdd")==('cdabcd')
