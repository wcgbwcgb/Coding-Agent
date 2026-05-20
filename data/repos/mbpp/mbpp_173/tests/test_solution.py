from solution import *


def test_mbpp_generated() -> None:
    assert remove_splchar('python  @#&^%$*program123')==('pythonprogram123')
    assert remove_splchar('python %^$@!^&*()  programming24%$^^()    language')==('pythonprogramming24language')
    assert remove_splchar('python   ^%&^()(+_)(_^&67)                  program')==('python67program')
