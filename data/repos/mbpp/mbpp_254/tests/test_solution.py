from solution import *


def test_mbpp_generated() -> None:
    assert words_ae("python programe")==['ame']
    assert words_ae("python programe language")==['ame','anguage']
    assert words_ae("assert statement")==['assert', 'atement']
