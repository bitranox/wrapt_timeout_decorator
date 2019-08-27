as ABADGER1999 points out in his blog https://anonbadger.wordpress.com/2018/12/15/python-signal-handlers-and-exceptions/
using signals and the TimeoutException is probably not the best idea - because it can be catched in the decorated function.

Of course You can use Your own Exception, derived from the Base Exception Class, but the code might still not work as expected -
see the next example - You may try it out in `jupyter <https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=jupyter_test_{repository}.ipynb>`_:

.. code-block:: py

    import time
    from wrapt_timeout_decorator import *

    # caveats when using signals - the TimeoutError raised by the signal may be catched
    # inside the decorated function.
    # So You might use Your own Exception, derived from the base Exception Class.
    # In Python-3.7.1 stdlib there are over 300 pieces of code that will catch your timeout
    # if you were to base an exception on Exception. If you base your exception on BaseException,
    # there are still 231 places that can potentially catch your exception.
    # You should use use_signals=False if You want to make sure that the timeout is handled correctly !
    # therefore the default value for use_signals = False on this decorator !

    @timeout(5, use_signals=True)
    def mytest(message):
        try:
            print(message)
            for i in range(1,10):
                time.sleep(1)
                print('{} seconds have passed - lets assume we read a big file here'.format(i))
        # TimeoutError is a Subclass of OSError - therefore it is catched here !
        except OSError:
            for i in range(1,10):
                time.sleep(1)
                print('Whats going on here ? - Ooops the Timeout Exception is catched by the OSError ! {}'.format(i))
        except Exception:
            # even worse !
            pass
        except:
            # the worst - and exists more then 300x in actual Python 3.7 stdlib Code !
            # so You never really can rely that You catch the TimeoutError when using Signals !
            pass


    if __name__ == '__main__':
        try:
            mytest('starting')
            print('no Timeout Occured')
        except TimeoutError():
            # this will never be printed because the decorated function catches implicitly the TimeoutError !
            print('Timeout Occured')
