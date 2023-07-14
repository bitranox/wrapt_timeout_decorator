Multithreading
--------------

By default, timeout-decorator uses signals to limit the execution time
of the given function. This approach does not work if your function is
executed not in the main thread (for example if it's a worker thread of
the web application) or when the operating system does not support signals (aka Windows).
There is an alternative timeout strategy for this case - by using multiprocessing.
This is done automatically, so you dont need to set ``use_signals=False``.
You can force not to use signals on Linux by passing the parameter ``use_signals=False`` to the timeout
decorator function for testing. If Your program should (also) run on Windows, I recommend to test under
Windows, since Windows does not support forking (read more under Section ``use with Windows``).
The following Code will run on Linux but NOT on Windows :

.. code-block:: py

    import time
    from wrapt_timeout_decorator import *

    @timeout(5, use_signals=False)
    def mytest(message):
        # this example does NOT work on windows, please check the section
        # "use with Windows" in the README.rst
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting')

.. warning::
    Make sure that in case of multiprocessing strategy for timeout, your function does not return objects which cannot
    be pickled, otherwise it will fail at marshalling it between master and child processes. To cover more cases,
    we use multiprocess and dill instead of multiprocessing and pickle.

    Since Signals will not work on Windows, it is disabled by default, whatever You set.


Multithreading
--------------

when using multiprocessing, the subprocess is monitored if it is still alive.
if the subprocess was terminated or killed (for instance by OOMKiller),
``multiprocessing.context.ProcessError`` will be raised.
By default the subprocess is monitored every 5 seconds, but can be set with parameter
``dec_poll_subprocess``

.. include:: .../tests/test_subprocess_alive_polling.py
    :code: python
    :start-after: # TestPolling{{{
    :end-before:  # TestPolling}}}

