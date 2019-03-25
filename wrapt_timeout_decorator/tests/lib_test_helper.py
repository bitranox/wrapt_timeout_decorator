from wrapt_timeout_decorator import *
import time

class ClassTest1(object):
    def __init__(self):
        self.x = 3

    @timeout('instance.x/3', use_signals=True, dec_allow_eval=True)
    def f(self):
        time.sleep(2)
