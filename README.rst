wrapt-timeout-decorator
=================

|Build Status| |Pypi Status| |Coveralls Status|

there are many timeout decorators out there - that one focuses on correctness if using with Classes, methods, class methods, static methods and so on, preserving also the traceback information for Pycharm debugging.
There is also a powerful eval function, it allows to read the desired timeout value even from Class attributes.
It is very flexible and van be used with python2.6, python 3.x, pypy, pypy3 and probably more.

Installation
------------

From source code:

::

    python setup.py install

From pypi:

::

    pip install https://github.com/bitranox/wrapt-timeout-decorator/archive/master.zip

Usage
-----

::

    import time
    from wrapt_timeout_decorator import *

    @timeout(5)
    def mytest():
        print("Start")
        for i in range(1,10):
            time.sleep(1)
            print("{} seconds have passed".format(i))

    if __name__ == '__main__':
        mytest()

Specify an alternate exception to raise on timeout:

::

    import time
    from wrapt_timeout_decorator import *

    @timeout(5, timeout_exception=StopIteration)
    def mytest():
        print("Start")
        for i in range(1,10):
            time.sleep(1)
            print("{} seconds have passed".format(i))

    if __name__ == '__main__':
        mytest()

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
    def mytest():
        print "Start"
        for i in range(1,10):
            time.sleep(1)
            print("{} seconds have passed".format(i))

    if __name__ == '__main__':
        mytest()

.. warning::
    Make sure that in case of multiprocessing strategy for timeout, your function does not return objects which cannot
    be pickled, otherwise it will fail at marshalling it between master and child processes.


Acknowledgement
---------------

Derived from
https://github.com/pnpnpn/timeout-decorator

http://www.saltycrane.com/blog/2010/04/using-python-timeout-decorator-uploading-s3/


Contribute
----------

I would love for you to fork and send me pull request for this project.
Please contribute.

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/LICENSE.txt>`_

.. |Build Status| image:: https://travis-ci.org/bitranox/wrapt-timeout-decorator.svg?branch=master
   :target: https://travis-ci.org/bitranox/wrapt-timeout-decorator
.. |Pypi Status| image:: https://badge.fury.io/py/wrapt-timeout-decorator.svg
   :target: https://badge.fury.io/py/wrapt-timeout-decorator
.. |Coveralls Status| image:: https://coveralls.io/repos/bitranox/wrapt-timeout-decorator/badge.png?branch=master
   :target: https://coveralls.io/r/bitranox/wrapt-timeout-decorator
