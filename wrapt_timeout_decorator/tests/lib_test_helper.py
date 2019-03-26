from wrapt_timeout_decorator import *
import time

# classes must NOT be defined in the main module, because of windows multiprocessing spawn - there is no fork,
# so the main module will be reloaded to simulate something like fork.
# so we put it into another file


class ClassTest1(object):
    def __init__(self):
        self.x = 2

    @timeout('instance.x//8', dec_allow_eval=True)
    def f(self):
        time.sleep(1)


class ClassTest2(object):
    def __init__(self, x):
        self.x = x

    @timeout('instance.x', use_signals=False, dec_allow_eval=True)
    def test_method(self):
        print('swallow')
        time.sleep(2)
        return 'done'
