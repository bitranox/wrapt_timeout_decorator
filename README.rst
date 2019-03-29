wrapt-timeout-decorator
=======================

|Build Status| |jupyter| |Pypi Status| |Codecov Status| |Better Code| |snyk security|

there are many timeout decorators out there - that one focuses on correctness if using with Classes, methods,

class methods, static methods and so on, preserving also the traceback information for Pycharm debugging.

There is also a powerful eval function, it allows to read the desired timeout value even from Class attributes.

It is very flexible and can be used from python 2.7 to python 3.x, pypy, pypy3 and probably other dialects.

Since it is using multiprocess and dill, this decorator can be used on more sophisticated objects 

when not using signals (under Windows for instance). In that case multiprocess and multiprocess.pipe is used 

to communicate with the child process (instead of multiprocessing.queue) which is faster and might work on Amazon AWS.

`100% code coverage <https://codecov.io/gh/bitranox/wrapt-timeout-decorator>`_, tested under `linux, OsX and Windows <https://travis-ci.org/bitranox/wrapt-timeout-decorator>`_

-----


`Report Issues <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/ISSUE_TEMPLATE.md>`_

`Contribute <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/CONTRIBUTING.md>`_

`Pull Request <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/PULL_REQUEST_TEMPLATE.md>`_

`Code of Conduct <https://github.com/bitranox/wrapt-timeout-decorator/blob/master/CODE_OF_CONDUCT.md>`_


-----

Try it in Jupyter Notebook
--------------------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/bitranox/wrapt-timeout-decorator/master?filepath=jupyter_test_wrapt_timeout_decorator.ipynb>`_

Installation and Upgrade
------------------------

From source code:

::

    python setup.py install
    python setup.py test

via pip (preferred):

::

    pip install --upgrade https://github.com/bitranox/wrapt-timeout-decorator/archive/master.zip

via requirements.txt:

::

    Insert following line in Your requirements.txt:
    https://github.com/bitranox/wrapt-timeout-decorator/archive/master.zip

    to install and upgrade all modules mentioned in requirements.txt:
    pip install --upgrade -r /<path>/requirements.txt

via python:

::

    python -m pip install --upgrade https://github.com/bitranox/wrapt-timeout-decorator/archive/master.zip


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


Parameters
----------

::

    @timeout(dec_timeout, use_signals, timeout_exception, exception_message, dec_allow_eval, dec_hard_timeout)
    def decorated_function(*args, **kwargs):
        # interesting things happens here ...
        ...

    dec_timeout         the timeout period in seconds, or a string that can be evaluated when dec_allow_eval = True
                        type: float, integer or string
                        default: None (no Timeout set)
                        can be overridden by passing the kwarg dec_timeout to the decorated function*

    use_signals         if to use signals (linux, osx) to realize the timeout. The most accurate and preferred method.
                        Please note that signals can be used only in the main thread and only on linux. In all other cases
                        (not the main thread, or under Windows) signals will not be used, no matter what You set here,
                        in that cases use_signals will be disabled automatically.
                        type: boolean
                        default: True
                        can be overridden by passing the kwarg use_signals to the decorated function*

    timeout_exception   the Exception that will be raised if a timeout occurs.
                        type: exception
                        default: TimeoutError, on Python < 3.3: Assertion Error (since TimeoutError does not exist on that Python Versions)

    exception_message   custom Exception message.
                        type: str
                        default : 'Function {function_name} timed out after {dec_timeout} seconds' (will be formatted)

    dec_allow_eval      will allow to evaluate the parameter dec_timeout.
                        If enabled, the parameter of the function dec_timeout, or the parameter passed
                        by kwarg dec_timeout will be evaluated if its type is string. You can access :
                        wrapped (the decorated function object and all the exposed objects below)
                        instance    Example: 'instance.x' - see example above or doku
                        args        Example: 'args[0]' - the timeout is the first argument in args
                        kwargs      Example: 'kwargs["max_time"] * 2'
                        type: bool
                        default: false
                        can be overridden by passing the kwarg dec_allow_eval to the decorated function*

    dec_hard_timeout    only relevant when signals can not be used. In that case a new process needs to be created.
                        The creation of the process on windows might take 0.5 seconds and more, depending on the size
                        of the main module and modules to be imported. Especially useful for small timeout periods.

                        dec_hard_timeout = True : the decorated function will time out after dec_timeout, no matter what -
                        that means if You set 0.1 seconds here, the subprocess can not be created in that time and the
                        function will always time out and never run.

                        dec_hard_timeout = False : the decorated function will time out after the called function
                        is allowed to run for dec_timeout seconds. The time needed to create that process is not considered.
                        That means if You set 0.1 seconds here, and the time to create the subprocess is 0.5 seconds,
                        the decorated function will time out after 0.6 seconds in total, allowing the decorated function to run
                        for 0.1 seconds.

                        type: bool
                        default: false
                        can be overridden by passing the kwarg dec_hard_timeout to the decorated function*

    * that means the decorated_function must not use that kwarg itself, since this kwarg will be popped from the kwargs




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
    be pickled, otherwise it will fail at marshalling it between master and child processes. To cover more cases,
    we use multiprocess and dill instead of multiprocessing and pickle.
    
    Since Signals will not work on Windows, it is disabled by default, whatever You set. 
    
    The granularity of the timeout is 0.1 seconds when using use_signals=False (on Windows
    or in a sub-thread)


Override with kwargs
--------------------

decorator parameters starting with \dec_* and use_signals can be overridden by kwargs with the same name :

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


Using allow_eval
----------------
This is very powerful, but can be also very dangerous if you accept strings to evaluate from UNTRUSTED input.

read: https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html

If enabled, the parameter of the function dec_timeout, or the parameter passed by kwarg dec_timeout will 
be evaluated if its type is string. 

You can access :

    wrapped (the function object)
    
    instance    Example: 'instance.x' - an attribute of the instance of the class instance
    
    args        Example: 'args[0]' - the timeout is the first argument in args
    
    kwargs      Example: 'kwargs["max_time"] * 2'
    
    and of course all attributes You can think of - that makes it powerful but dangerous.
    
    by default allow_eval is disabled - but You can enable it in order to cover some edge cases without
    
    modifying the timeout decorator.


::


    def class ClassTest4(object):
        def __init__(self,x):
            self.x=x

        @timeout('instance.x', dec_allow_eval=True)
        def test_method(self):
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
        my_foo = ClassTest4(3)
        my_foo.test_method(dec_timeout='instance.x * 2.5 +1')
        my_foo.foo3(dec_timeout='instance.x * 2.5 +1', dec_allow_eval=True)
        my_foo.foo4(1,more_time=3)  # this will time out in 4 seconds

Logging
-------

when signals=False (on Windows), logging in the wrapped function can be tricky. Since a new process is
created, we can not use the logger object of the main process. Further development is needed to
connect to the main process logger via a socket or queue.

When the wrapped function is using logger=logging.getLogger(), a new Logger Object is created.
Setting up that Logger can be tricky (File Logging from two Processes is not supported ...)
I think I will use a socket to implement that (SocketHandler and some Receiver Thread)

Until then, You need to set up Your own new logger in the decorated function, if logging is needed.
Again - keep in mind that You can not write to the same logfile from different processes !
(although there are logging modules which can do that)


use with Windows
----------------

On Windows the main module is imported again (but with name != 'main') because Windows is trying to simulate
a forking-like behavior on a system that doesn't have forking. multiprocessing has no way to know that you didn't do
anything important in you main module, so the import is done "just in case" to create an environment similar
to the one in your main process.

It is more a problem of Windows, because the Windows Operating System does neither support "fork", nor "signals"
You can find more information on that here:

https://stackoverflow.com/questions/45110287/workaround-for-using-name-main-in-python-multiprocessing

https://docs.python.org/2/library/multiprocessing.html#windows

Classes in the __main__ context can not be pickled, You need to put decorated Classes into another module.
In general (especially for windows) , the main() program should not have anything but the main function, the real thing should happen in the modules.
I am also used to put all settings or configurations in a different file - so all processes or threads can access them (and also to keep them in one place together, not to forget typing hints and name completion in Your favorite editor)
Please note that due some limitation in dill (the pickle replacement) Classes can not be decorated at all under Windows with Python 2.7

here an example that will work on Linux but wont work on Windows (the variable "name" and the function "sleep" wont be found in the spawned process :


::

    main.py:

    from time import sleep
    from wrapt_timeout_decorator import *

    name="my_var_name"


    @timeout(5, use_signals=False)
    def mytest():
        print("Start ", name)
        for i in range(1,10):
            sleep(1)
            print("{} seconds have passed".format(i))
        return i


    if __name__ == '__main__':
        mytest()


here the same example, which will work on Windows with Python 3.x but not with Python 2.x because of pickling Errors:


::


    my_program_main.py:

    from multiprocessing import freeze_support
    import lib_test

    def main():
        lib_test.mytest()


    if __name__ == '__main__':
        freeze_support()
        main()


::


        conf_my_program.py:

        class ConfMyProgram(object):
            def __init__(self):
                self.name:str = 'my_var_name'

        conf_my_program = ConfMyProgram()


::


    lib_test.py:

    from wrapt_timeout_decorator import *
    from time import sleep
    from conf_my_program import conf_my_program

    @timeout(5, use_signals=False)
    def mytest():
        print("Start ", conf_my_program.name)
        for i in range(1,10):
            sleep(1)
            print("{} seconds have passed".format(i))
        return i


use_signals = False (Windows) gives different total time
--------------------------------------------------------

when use_signals = False (this is the only method available on Windows), the timeout function is realized by starting
another process and terminate that process after the given timeout.
Under Linux fork() of a new process is very fast, under Windows it might take some considerable time,
because the main context needs to be reloaded on spawn() since fork() is not available on Windows.
Spawning of a small module might take something like 0.5 seconds and more.

Since it is not predictable how long the spawn() will take on windows, the timeout will start AFTER
spawning the new process.

This means that the timeout given, is the time the process is allowed to run, excluding the time to setup the process itself.
This is especially important if You use small timeout periods :

for Instance:


::


    @timeout(0.1)
    def test():
        time.sleep(0.2)


the total time to timeout on linux with use_signals = False will be around 0.1 seconds, but on windows this will take
about 0.6 seconds. 0.5 seconds to set up the new process, and giving the function test() 0.1 seconds to run !

If You need that a decorated function should time out exactly after the given timeout, You can pass
the parameter dec_hard_timeout=True. in this case the function will time out exactly after the given time,
no matter how long it took to spawn the process itself. In that case, if You set up the time out too short,
the process might never run and will always timeout.

Requirements
------------

following Packets will be installed / needed :

DILL, see  : https://github.com/uqfoundation/dill

MULTIPROCESS, see: https://github.com/uqfoundation/multiprocess

WRAPT, see : https://github.com/GrahamDumpleton/wrapt

PYTEST, see : https://github.com/pytest-dev/pytest

Acknowledgement
---------------

Derived from

https://github.com/pnpnpn/timeout-decorator

http://www.saltycrane.com/blog/2010/04/using-python-timeout-decorator-uploading-s3/

and special thanks to Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
Please contribute.

TODO: 
-----

conserving correct Traceback information when use_signals=False, possibly by using tblib

(see https://pypi.python.org/pypi/tblib)

better logging for signals=false. Since a new process is created, we can not log to the logger of the main process.
logger=logging.getLogger() will crate a new Logger in the wrapped function.

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
.. |snyk security| image:: https://snyk.io/test/github/bitranox/wrapt-timeout-decorator/badge.svg
   :target: https://snyk.io/test/github/bitranox/wrapt-timeout-decorator
.. |jupyter| image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/bitranox/wrapt-timeout-decorator/master?filepath=jupyter_test_wrapt_timeout_decorator.ipynb
