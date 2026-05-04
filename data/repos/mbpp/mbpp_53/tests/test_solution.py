from solution import *


def test_mbpp_generated() -> None:
    assert check_Equality("abcda") == "Equal"
    assert check_Equality("ab") == "Not Equal"
    assert check_Equality("mad") == "Not Equal"
