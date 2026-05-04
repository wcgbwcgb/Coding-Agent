from solution import *


def test_mbpp_generated() -> None:
    assert count_Substring_With_Equal_Ends("abc") == 3
    assert count_Substring_With_Equal_Ends("abcda") == 6
    assert count_Substring_With_Equal_Ends("ab") == 2
