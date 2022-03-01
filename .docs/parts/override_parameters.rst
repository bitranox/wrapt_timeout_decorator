Override Parameters
-------------------

decorator parameters starting with \dec_* and use_signals can be overridden by kwargs with the same name :

.. code-block:: py


    import time
    from wrapt_timeout_decorator import *

    @timeout(dec_timeout=5, use_signals=False)
    def mytest(message):
        # this example does NOT work on windows, please check the section
        # "use with Windows" in the README.rst
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting',dec_timeout=12)   # override the decorators setting. The kwarg dec_timeout will be not
                                            # passed to the decorated function.
