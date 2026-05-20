from solution import *


def test_mbpp_generated() -> None:
    assert month_season('January',4)==('winter')
    assert month_season('October',28)==('autumn')
    assert month_season('June',6)==('spring')
