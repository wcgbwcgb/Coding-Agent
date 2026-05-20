from solution import *


def test_mbpp_generated() -> None:
    assert string_to_list("python programming")==['python','programming']
    assert string_to_list("lists tuples strings")==['lists','tuples','strings']
    assert string_to_list("write a program")==['write','a','program']
