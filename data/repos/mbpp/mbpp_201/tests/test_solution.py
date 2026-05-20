from solution import *


def test_mbpp_generated() -> None:
    assert chkList(['one','one','one']) == True
    assert chkList(['one','Two','Three']) == False
    assert chkList(['bigdata','python','Django']) == False
