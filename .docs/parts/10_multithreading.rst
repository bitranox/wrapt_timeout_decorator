Multithreading
--------------

Signals will not work if your function is not executed in the main thread.
``use_signals`` is therefore automatically disabled (if set) when the function is not running in the main thread.


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
    Make sure that in case of subprocess strategy for timeout, your function does not return objects which cannot
    be pickled, otherwise it will fail at marshalling it between master and child processes. To cover more cases,
    we use multiprocess and dill instead of multiprocessing and pickle.

    Since Signals will not work on Windows, it is disabled by default, whatever You set.
