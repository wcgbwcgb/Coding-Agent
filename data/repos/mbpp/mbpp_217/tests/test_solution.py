from solution import *


def test_mbpp_generated() -> None:
    assert first_Repeated_Char("Google") == "o"
    assert first_Repeated_Char("data") == "a"
    assert first_Repeated_Char("python") == '\0'
