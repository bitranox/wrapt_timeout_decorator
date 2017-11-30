wrapt-timeout-decorator
=================

|Build Status| |Pypi Status| |Codecov Status| |Better Code| |snyk security| |gemnasium|

there are many timeout decorators out there - that one focuses on correctness if using with Classes, methods,

class methods, static methods and so on, preserving also the traceback information for Pycharm debugging.

There is also a powerful eval function, it allows to read the desired timeout value even from Class attributes.

It is very flexible and can be used from python 2.6 to python 3.x, pypy, pypy3 and probably other dialects.

Since it is using multiprocess and dill, this decorator can be used on more sophisticated objects 

when not using signals (under Windows for instance)


-----


`Report Issues <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/ISSUE_TEMPLATE.md>`_

`Contribute <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/CONTRIBUTING.md>`_

`Pull Request <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/PULL_REQUEST_TEMPLATE.md>`_

`Code of Conduct <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/CODE_OF_CONDUCT.md>`_


-----

Installation
------------

From source code:

::

    python setup.py install

From pypi:

::

    pip install https://github.com/bitranox/wrapt-timeout-decorator/archive/master.zip

Basic Usage
-----------

::

    import time
    from wrapt_timeout_decorator import *

    @timeout(5)
    def mytest(message):
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting')

Specify an alternate exception to raise on timeout:

::

    import time
    from wrapt_timeout_decorator import *

    @timeout(5, timeout_exception=StopIteration)
    def mytest(message):
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting')

Multithreading
--------------

By default, timeout-decorator uses signals to limit the execution time
of the given function. This appoach does not work if your function is
executed not in a main thread (for example if it's a worker thread of
the web application). There is alternative timeout strategy for this
case - by using multiprocessing. To use it, just pass
``use_signals=False`` to the timeout decorator function:

::

    import time
    from wrapt_timeout_decorator import *

    @timeout(5, use_signals=False)
    def mytest(message):
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting')

.. warning::
    Make sure that in case of multiprocessing strategy for timeout, your function does not return objects which cannot
    be pickled, otherwise it will fail at marshalling it between master and child processes.
    
    Since Signals will not work in Windows, it is disabled by default, whatever You set. 
    
    The granularity of the timeout is 0.1 seconds when using use_signals=False (or Windows)
    

Override with kwargs
--------------------

decorator parameters starting with dec_ can be overridden by kwargs with the same name : 

::


    import time
    from wrapt_timeout_decorator import *

    @timeout(dec_timeout=5, use_signals=False)
    def mytest(message):
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting',dec_timeout=12)   # override the decorators setting. The kwarg dec_timeout will be not 
                                            # passed to the decorated function.  

::

Using the decorator without actually decorating the function
------------------------------------------------------------

::


    import time
    from wrapt_timeout_decorator import *

    def mytest(message):
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        timeout(dec_timeout=5)(mytest)('starting')


::

Using allow_eval
----------------
This is very powerful, but can be also very dangerous if you accept strings to evaluate from UNTRUSTED input.

read: https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html

If enabled, the parameter of the function dec_timeout, or the parameter passed by kwarg dec_timeout will 
be evaluated if its type is string. 

You can access :

    wrapped (the function object)
    
    instance    Example: 'instance.x' - an attribute of the instace of the class instance
    
    args        Example: 'args[0]' - the timeout is the first argument in args
    
    kwargs      Example: 'kwargs["max_time"] * 2'
    
    and of course all attributes You can think of - that makes it powerful but dangerouse.
    
    by default allow_eval is disabled - but You can enable it in order to cover some edge cases without
    
    modifying the timeout decorator.


::


    def class Foo(object):
        def __init__(self,x):
            self.x=x

        @timeout('instance.x', dec_allow_eval=True)
        def foo2(self):
            print('swallow')

        @timeout(1)
        def foo3(self):
            print('parrot')

        @timeout(dec_timeout='args[0] + kwargs.pop("more_time",0)', dec_allow_eval=True)
        def foo4(self,base_delay):
            time.sleep(base_delay)
            print('knight')


    if __name__ == '__main__':
        # or override via kwarg :
        my_foo = Foo(3)
        my_foo.foo2(dec_timeout='instance.x * 2.5 +1')
        my_foo.foo3(dec_timeout='instance.x * 2.5 +1', dec_allow_eval=True)
        my_foo.foo4(1,more_time=3)  # this will time out in 4 seconds


::


Requirements
---------------

following Packets will be installed / needed : 

DILL, see  : https://github.com/uqfoundation/dill

MULTIPROCESS, see: https://github.com/uqfoundation/multiprocess

WRAPT, see : https://github.com/GrahamDumpleton/wrapt




Acknowledgement
---------------

Derived from

https://github.com/pnpnpn/timeout-decorator

http://www.saltycrane.com/blog/2010/04/using-python-timeout-decorator-uploading-s3/


Contribute
----------

I would love for you to fork and send me pull request for this project.
Please contribute.


TODO: 
-----

conserving correct Traceback information when use_signals=False, possibly by using tblib

(see https://pypi.python.org/pypi/tblib)


register on Pypi


License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/LICENSE.txt>`_

.. |Build Status| image:: https://travis-ci.org/bitranox/wrapt-timeout-decorator.svg?branch=master
   :target: https://travis-ci.org/bitranox/wrapt-timeout-decorator
.. |Pypi Status| image:: https://badge.fury.io/py/wrapt-timeout-decorator.svg
   :target: https://badge.fury.io/py/wrapt-timeout-decorator
.. |Codecov Status| image:: https://codecov.io/gh/bitranox/wrapt-timeout-decorator/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/wrapt-timeout-decorator
.. |Better Code| image:: https://bettercodehub.com/edge/badge/bitranox/wrapt-timeout-decorator?branch=master
   :target: https://bettercodehub.com/results/bitranox/wrapt-timeout-decorator
.. double, because sometimes the badge does not show up
.. |snyk security| image:: https://snyk.io/test/github/bitranox/wrapt-timeout-decorator/badge.svg
   :target: https://snyk.io/test/github/bitranox/wrapt-timeout-decorator
.. |snyk security| image:: https://snyk.io/test/github/bitranox/wrapt-timeout-decorator/badge.svg
   :target: https://snyk.io/test/github/bitranox/wrapt-timeout-decorator
.. |gemnasium| image:: https://gemnasium.com/badges/github.com/bitranox/wrapt-timeout-decorator.svg
   :target: https://gemnasium.com/github.com/bitranox/wrapt-timeout-decorator 
