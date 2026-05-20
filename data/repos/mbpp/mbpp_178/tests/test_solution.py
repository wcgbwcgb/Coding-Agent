from solution import *


def test_mbpp_generated() -> None:
    assert string_literals(['language'],'python language')==('Matched!')
    assert string_literals(['program'],'python language')==('Not Matched!')
    assert string_literals(['python'],'programming language')==('Not Matched!')
