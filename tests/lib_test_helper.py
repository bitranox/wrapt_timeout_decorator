from wrapt_timeout_decorator import timeout  # type: ignore
import time

# classes must NOT be defined in the main module, because of windows multiprocessing spawn - there is no fork,
# so the main module will be reloaded to simulate something like fork.
# so we put it into another file


class ClassTest1(object):
    def __init__(self) -> None:
        self.x = 1.0

    @timeout("instance.x/10", dec_allow_eval=True)  # type: ignore
    def f(self) -> None:
        time.sleep(0.2)


class ClassTest2(object):
    def __init__(self, x: float) -> None:
        self.x = x

    @timeout("instance.x", use_signals=False, dec_allow_eval=True)  # type: ignore
    def test_method(self) -> str:  # type: ignore
        print("swallow")
        time.sleep(0.2)
        return "done"
