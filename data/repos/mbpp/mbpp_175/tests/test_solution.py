from solution import *


def test_mbpp_generated() -> None:
    assert is_valid_parenthese("(){}[]")==True
    assert is_valid_parenthese("()[{)}")==False
    assert is_valid_parenthese("()")==True
