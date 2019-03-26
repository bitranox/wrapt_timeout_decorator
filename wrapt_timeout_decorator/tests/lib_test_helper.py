from wrapt_timeout_decorator import *
import time

# classes must not be defined in the main module, because of windows multiprocessing
# so we put it into another file

class ClassTest1(object):
    def __init__(self):
        self.x = 3

    @timeout('instance.x/3', use_signals=True, dec_allow_eval=True)
    def f(self):
        time.sleep(2)


class ClassTest2(object):
    def __init__(self):
        self.x = 3

    @timeout('instance.x/3', use_signals=False, dec_allow_eval=True)
    def f(self):
        time.sleep(2)
