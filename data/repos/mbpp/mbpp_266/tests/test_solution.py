from solution import *


def test_mbpp_generated() -> None:
    assert lateralsurface_cube(5)==100
    assert lateralsurface_cube(9)==324
    assert lateralsurface_cube(10)==400
