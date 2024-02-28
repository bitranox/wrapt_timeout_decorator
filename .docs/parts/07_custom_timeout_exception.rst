Custom Timeout Exception
------------------------

Define a different exception to be raised upon timeout:

.. code-block::  python

    import time
    from wrapt_timeout_decorator import *

    # this will throw StopIteration Error instead of TimeoutError
    @timeout(5, timeout_exception=StopIteration)
    def mytest(message):
        # this example does NOT work on windows, please check the section
        # "use with Windows" in the README.rst
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting')
