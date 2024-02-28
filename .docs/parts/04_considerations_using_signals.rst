Considerations using Signals
----------------------------

ABADGER1999 highlights in his `blog post <https://anonbadger.wordpress.com/2018/12/15/python-signal-handlers-and-exceptions/>`_ the
potential pitfalls of using signals alongside the TimeoutException.
This approach may not be advisable as the exception can be intercepted within the decorated function.

While it's possible to implement a custom Exception derived from the Base Exception Class,
this doesn't guarantee the code will behave as anticipated.
For an illustrative example, you're encouraged to conduct an experiment using a
`Jupyter notebook <https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=jupyter_test_{repository}.ipynb>`_.


.. code-block::

    import time
    from wrapt_timeout_decorator import *

    # Considerations for Signal Usage - Handling TimeoutError
    # The TimeoutError triggered by a signal might be intercepted within the decorated function.
    # Utilizing a custom Exception, derived from the base Exception Class, is a possible workaround.
    # Within Python 3.7.1's standard library, there are over 300 instances where your custom timeout might be caught
    # if it's based on Exception. Should you base your exception on BaseException,
    # there still remain 231 potential catch points.
    # To ensure proper timeout management, it's advisable to set `use_signals=False`.
    # Consequently, `use_signals` defaults to `False` in this decorator to avoid these issues.

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
