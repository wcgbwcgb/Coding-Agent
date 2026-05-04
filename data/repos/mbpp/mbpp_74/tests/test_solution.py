from solution import *


def test_mbpp_generated() -> None:
    assert is_samepatterns(["red","green","green"], ["a", "b", "b"])==True 
    assert is_samepatterns(["red","green","greenn"], ["a","b","b"])==False 
    assert is_samepatterns(["red","green","greenn"], ["a","b"])==False 
