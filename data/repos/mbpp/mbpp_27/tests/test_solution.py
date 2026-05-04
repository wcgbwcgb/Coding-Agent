from solution import *


def test_mbpp_generated() -> None:
    assert remove(['4words', '3letters', '4digits']) == ['words', 'letters', 'digits']
    assert remove(['28Jan','12Jan','11Jan']) == ['Jan','Jan','Jan']
    assert remove(['wonder1','wonder2','wonder3']) == ['wonder','wonder','wonder']
