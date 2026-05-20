from solution import *


def test_mbpp_generated() -> None:
    assert check_String('thishasboth29') == True
    assert check_String('python') == False
    assert check_String ('string') == False
