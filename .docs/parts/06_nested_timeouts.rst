Handling Nested Timeouts
------------------------

Due to Unix's limitation of having just one ALARM signal per process, it's necessary to set `use_signals=False` for nested timeouts
to function correctly. While the outermost decorator may utilize signals,
all inner decorators must have `use_signals` set to `False`—which is the default setting.
For practical experimentation and to see this behavior in action,
you're encouraged to use a `Jupyter notebook <https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=jupyter_test_{repository}.ipynb>`_.


.. code-block:: python

    # main.py
    import mylib

    # this example will work on Windows and Linux
    # since the decorated function is not in the __main__ scope but in another module !

    if __name__ == '__main__':
    mylib.outer()


.. code-block:: python

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
