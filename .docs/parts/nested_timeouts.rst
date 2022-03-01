nested Timeouts
----------------

since there is only ONE ALARM Signal on Unix per process, You need to use use_signals = False for nested timeouts.
The outmost decorator might use Signals, all nested Decorators needs to use use_signals=False (the default)
You may try it out in `jupyter <https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=jupyter_test_{repository}.ipynb>`_:

.. code-block:: py

    # main.py
    import mylib

    # this example will work on Windows and Linux
    # since the decorated function is not in the __main__ scope but in another module !

    if __name__ == '__main__':
    mylib.outer()


.. code-block:: py

    # mylib.py
    from wrapt_timeout_decorator import *
    import time

    # this example will work on Windows and Linux
    # since the decorated function is not in the __main__ scope but in another module !

    @timeout(1, use_signals=True)
    def outer():
        inner()

    @timeout(5)
    def inner():
        time.sleep(3)
        print("Should never be printed if you call outer()")
