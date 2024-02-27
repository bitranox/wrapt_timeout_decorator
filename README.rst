wrapt_timeout_decorator
=======================


Version v1.5.0 as of 2024-02-27 see `Changelog`_

|build_badge| |codeql| |license| |jupyter| |pypi|
|pypi-downloads| |black| |codecov| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/wrapt_timeout_decorator/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/wrapt_timeout_decorator/actions/workflows/python-package.yml


.. |codeql| image:: https://github.com/bitranox/wrapt_timeout_decorator/actions/workflows/codeql-analysis.yml/badge.svg?event=push
   :target: https://github.com//bitranox/wrapt_timeout_decorator/actions/workflows/codeql-analysis.yml

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=wrapt_timeout_decorator.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/wrapt-timeout-decorator?label=PyPI%20Package
   :target: https://badge.fury.io/py/wrapt_timeout_decorator

.. badge until 2023-10-08:
.. https://img.shields.io/codecov/c/github/bitranox/wrapt_timeout_decorator
.. badge from 2023-10-08:
.. |codecov| image:: https://codecov.io/gh/bitranox/wrapt_timeout_decorator/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/wrapt_timeout_decorator

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/wrapt_timeout_decorator?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/wrapt_timeout_decorator/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/wrapt_timeout_decorator?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/wrapt_timeout_decorator/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/wrapt_timeout_decorator?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/wrapt_timeout_decorator/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://snyk.io/test/github/bitranox/wrapt_timeout_decorator/badge.svg
   :target: https://snyk.io/test/github/bitranox/wrapt_timeout_decorator

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/wrapt-timeout-decorator
   :target: https://pypi.org/project/wrapt-timeout-decorator/
   :alt: PyPI - Downloads

There are several timeout decorators available, but the one mentioned here
focuses on ensuring correctness when used with classes, methods, class methods,
static methods, etc. It also preserves traceback information for PyCharm debugging.

Additionally, there is a powerful eval function that allows reading
the desired timeout value even from class attributes.

Two timeout strategies have been implemented:
one using "Signals" and the other using "Multiprocessing".

Signals
-------

The "Signals" strategy (for POSIX Systems) is elegant and efficient,
but it has some important caveats which should be reviewed
in the `Caveats using Signals`_ section.


Multiprocessing
---------------

The default strategy is to use Multiprocessing

- on Windows, due to the lack of signals, this is only available choice, which is enforced automatically
- signals (on POSIX) can not be used in a subthread, therefore multiprocessing is enforced in such cases

When using a subprocess many types from multiprocessing need to be pickable so that child processes can use them.
Therefore we use "dill" instead of "pickle" and "multiprocess" instead of "multiprocessing".

dill extends python’s pickle module for serializing and de-serializing python objects to the majority of the built-in python types

Communication with the subprocess is done via "multiprocess.pipe" instead of "queue",
which offers improved speed and may also work on Amazon AWS.

----

automated tests, Github Actions, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.8.0 or newer

tested on recent linux with python 3.8, 3.9, 3.10, 3.11, 3.12, pypy-3.9, pypy-3.10 - architectures: amd64

`100% code coverage <https://codeclimate.com/github/bitranox/wrapt_timeout_decorator/test_coverage>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://github.com/bitranox/wrapt_timeout_decorator/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/wrapt_timeout_decorator/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/wrapt_timeout_decorator/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/wrapt_timeout_decorator/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=wrapt_timeout_decorator.ipynb>`_

Usage
-----------

.. code-block:: py

    import time
    from wrapt_timeout_decorator import *

    @timeout(5)
    def mytest(message):
        # this example does NOT work on windows, please check the section
        # "use with Windows" in the README.rst
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting')

General Recommendations
-----------------------
Minimize the excessive use of timeouts in your code and reserve their usage for essential cases.

Implement timeouts at the lowest possible abstraction level to prevent unintended
consequences such as exceptions being caught by unrelated code or non-pickable
functions and arguments.

Avoid incorporating the Timeout Decorator within a loop that iterates multiple times,
as this can result in considerable time overhead,
especially on Windows systems, when utilizing multiprocessing.

Whenever feasible, leverage the existing built-in timeouts already provided by the functions
and libraries you utilize. These built-in timeouts can handle most situations effectively.
Only resort to use this Timeout Decorator as a last resort when all other alternatives have been exhausted.


    BAD EXAMPLE (Pseudocode) - lets assume the write to the database fails sometimes for unknown reasons, and "hangs"

    .. code-block:: py

        # module file_analyzer
        import time
        from wrapt_timeout_decorator import *

        def read_the_file(filename):
            ...

        def analyze_the_file(filename):
            ...

        def write_to_database(file_content):
            ...


        @timeout(5)  # try to minimize the scope of the timeout
        def import_file(filename):
            file_content = read_the_file(filename)
            structured_data = analyze_the_file(file_content)
            write_to_database(structured_data)


    BETTER EXAMPLE (Pseudocode)

    .. code-block:: py

        # module file_analyzer
        import time
        from wrapt_timeout_decorator import *

        def read_the_file(filename):
            ...

        def analyze_the_file(filename):
            ...

        @timeout(5)     # better, because smaller scope
        def write_to_database(file_content):
            ...

        def import_file(filename):
            file_content = read_the_file(filename)
            structured_data = analyze_the_file(file_content)
            write_to_database(structured_data)

use with Windows
----------------

For the impatient:

All You need to do is to put the decorated function into another Module, NOT in the main program.

For those who want to dive deeper :


On Windows the main module is imported again (but with a name != 'main') because Python is trying to simulate
a forking-like behavior on a system that doesn't support forking. multiprocessing tries to create an environment
similar to Your main process by importing the main module again with a different name. Thats why You need to shield
the entry point of Your program with the famous " if __name__ == '__main__': "

.. code-block:: py

    import lib_foo

    def some_module():
        lib_foo.function_foo()

    def main():
        some_module()


    # here the subprocess stops loading, because __name__ is NOT '__main__'
    if __name__ = '__main__':
        main()

This is a problem of Windows OS, because the Windows Operating System does not support "fork"

You can find more information on that here:

https://stackoverflow.com/questions/45110287/workaround-for-using-name-main-in-python-multiprocessing

https://docs.python.org/2/library/multiprocessing.html#windows

Since main.py is loaded again with a different name but "__main__", the decorated function now points to objects that do not exist anymore, therefore You need to put the decorated Classes and functions into another module.
In general (especially on windows) , the main() program should not have anything but the main function, the real thing should happen in the modules.
I am also used to put all settings or configurations in a different file - so all processes or threads can access them (and also to keep them in one place together, not to forget typing hints and name completion in Your favorite editor)

The "dill" serializer is able to serialize also the __main__ context, that means the objects in our example are pickled to "__main__.lib_foo", "__main__.some_module","__main__.main" etc.
We would not have this limitation when using "pickle" with the downside that "pickle" can not serialize following types:

functions with yields, nested functions, lambdas, cell, method, unboundmethod, module, code, methodwrapper,
dictproxy, methoddescriptor, getsetdescriptor, memberdescriptor, wrapperdescriptor, xrange, slice,
notimplemented, ellipsis, quit

additional dill supports:

save and load python interpreter sessions, save and extract the source code from functions and classes, interactively diagnose pickling errors

To support more types with the decorator, we selected dill as serializer, with the small downside that methods and classes can not be decorated in the __main__ context, but need to reside in a module.

You can find more information on that here:
https://stackoverflow.com/questions/45616584/serializing-an-object-in-main-with-pickle-or-dill

**Timing :** Since spawning takes some unknown timespan (all imports needs to be done again !), You can specify when the timeout should start, please read the section `hard timeout`_

Here an example that will work on Linux but wont work on Windows (the variable "name" and the function "sleep" wont be found in the spawned process :


.. code-block:: py

    main.py:

    from time import sleep
    from wrapt_timeout_decorator import *

    name="my_var_name"

    @timeout(5, use_signals=False)
    def mytest():
        # this example does NOT work on windows, please check the example below !
        # You need to move this function into a module to be able to run it on windows.
        print("Start ", name)
        for i in range(1,10):
            sleep(1)
            print("{} seconds have passed".format(i))
        return i


    if __name__ == '__main__':
        mytest()


here the same example, which will work on Windows:


.. code-block:: py


    # my_program_main.py:

    import lib_test

    def main():
        lib_test.mytest()

    if __name__ == '__main__':
        main()


.. code-block:: py


        # conf_my_program.py:

        class ConfMyProgram(object):
            def __init__(self):
                self.name:str = 'my_var_name'

        conf_my_program = ConfMyProgram()


.. code-block:: py

    # lib_test.py:

    from wrapt_timeout_decorator import *
    from time import sleep
    from conf_my_program import conf_my_program

    # use_signals = False is not really necessary here, it is set automatically under Windows
    # but You can force NOT to use Signals under Linux
    @timeout(5, use_signals=False)
    def mytest():
        print("Start ", conf_my_program.name)
        for i in range(1,10):
            sleep(1)
            print("{} seconds have passed".format(i))
        return i

Caveats using Signals
---------------------

as ABADGER1999 `points out in his blog <https://anonbadger.wordpress.com/2018/12/15/python-signal-handlers-and-exceptions/>`_
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

Multiprocessing Caveats and Usage Guidelines
--------------------------------------------

Overview
--------
Multiprocessing is utilized by default to implement timeout functionality. This involves forking or spawning subprocesses, each with its own set of considerations and caveats.

Initialization
--------------
- **Windows Considerations:** On Windows, the spawn method can significantly slow down the process initiation.
- **Main Context Protection:** It is crucial to protect the ``__main__`` context for compatibility, especially on Windows. See the "Usage with Windows" section for more details.
- **Pickle Requirements:** Function codes and arguments must be pickleable. To accommodate a wider range of types, `dill` is used for serialization.
- **Global Variables:** Access to global variables from a child process might not reflect the parent process's state at the time of the fork. Module-level constants are generally unaffected.

Process Execution and Communication
------------------------------------
- **Subprocess Execution:** Functions run in a separate subprocess, whether forked or spawned.
- **Data Transmission:** Parameters and results are communicated through pipes, with `dill` used for serialization.
- **Timeout Management:** Absent a result within the specified timeout, the subprocess is terminated using `SIGTERM`. Ensuring subprocesses can terminate safely is essential; thus, disabling the `SIGTERM` handler is not advisable.

Multiprocessing Start Methods
-----------------------------
- **Windows Limitation:** Only `spawn` is available on Windows.
- **Linux/Unix Options:** Options include `fork`, `forkserver`, and `spawn`.
    - **Fork:** Efficiently clones the parent process, including memory space, but may lead to issues with shared resources or in multi-threaded applications.
    - **Forkserver:** Starts a server at program launch, creating new processes upon request for better isolation but at a slower pace due to the server communication requirement.
    - **Spawn:** Initiates a fresh Python interpreter process, ensuring total independence at the cost of slower start-up due to the need for full initialization.

Choosing the Right Start Method
-------------------------------
- **fork** offers speed but can encounter issues with resource sharing or threading.
- **forkserver** enhances stability and isolation, ideal for applications requiring safety or managing unstable resources.
- **spawn** provides the highest level of isolation, recommended for a clean start and avoiding shared state complications.

Setting the Start Method
------------------------
Configure the start method with ``multiprocessing.set_start_method(method, force=False)``. This should be done cautiously, ideally once, and within the ``if __name__ == '__main__'`` block to prevent unintended effects.

Special Considerations for Uvicorn and FastAPI
----------------------------------------------
For Uvicorn or FastAPI applications, a specific approach to the `fork` method is recommended to ensure proper signal handling and isolation, facilitated by the `dec_mp_reset_signals` parameter. This design aims to reset signal handlers and manage file descriptors in child processes effectively.

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

Alternative Exception
---------------------

Specify an alternate exception to raise on timeout:

.. code-block:: py

    import time
    from wrapt_timeout_decorator import *

    @timeout(5, timeout_exception=StopIteration)
    def mytest(message):
        # this example does NOT work on windows, please check the section
        # "use with Windows" in the README.rst
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        mytest('starting')

Parameters
----------

.. code-block::

    @timeout(dec_timeout, use_signals, timeout_exception, exception_message, dec_allow_eval, dec_hard_timeout)
    def decorated_function(*args, **kwargs):
        # interesting things happens here ...
        ...

    """
    dec_timeout         the timeout period in seconds, or a string that can be evaluated when dec_allow_eval = True
                        type: float, integer or string
                        default: None (no Timeout set)
                        can be overridden by passing the kwarg dec_timeout to the decorated function*

    use_signals         if to use signals (linux, osx) to realize the timeout. The most accurate method but with caveats.
                        By default the Wrapt Timeout Decorator does NOT use signals !
                        Please note that signals can only be used in the main thread and only on linux. In all other cases
                        (not the main thread, or under Windows) signals cant be used anyway and will be disabled automatically.
                        In general You dont need to set use_signals Yourself.
                        Please read the sections - `Caveats using Signals` and `Caveats using Multiprocessing`
                        type: boolean
                        default: False
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

    dec_mp_reset_signals  This parameter is relevant when using the "fork" start method for multiprocessing.
                        Setting it to True accomplishes two primary objectives:

                        - Restores Default Signal Handlers in Child Processes:
                            It ensures that child processes revert to the default signal handling behavior,
                            rather than inheriting signal handlers from the parent process.
                            This adjustment is crucial for applications utilizing frameworks like "unicorn" or "FastAPI",
                            facilitating the use of the efficient "fork" method while maintaining correct signal handling.
                            For more context, refer to the Discussion on
                            FastAPI GitHub page: https://github.com/tiangolo/fastapi/discussions/7442

                        - Avoids Inheritance of the File Descriptor (fd) for Wakeup Signals:
                            Typically, if the parent process utilizes a wakeup_fd, child processes inherit this descriptor.
                            Consequently, when a signal is sent to a child, it is also received by the parent process
                            via this shared socket, potentially leading to unintended termination or shutdown of the application.
                            By resetting signal handlers and not using the inherited fd, this parameter prevents such conflicts,
                            ensuring isolated and correct signal handling in child processes.

                        Note: This parameter exclusively affects processes initiated with the "fork" method
                        and is not applicable to other multiprocessing start methods.

    For enhanced isolation of subprocesses, consider utilizing the "forkserver" or "spawn" start methods in multiprocessing.
    These methods provide a greater degree of independence between the parent process and its children,
    mitigating the risks associated with shared resources and ensuring a cleaner execution environment for each subprocess,
    at the cost of slower startup times. This slowdown is due to the additional overhead involved in setting up a completely
    new process environment for each child process, as opposed to directly duplicating the parent process's environment,
    which occurs with the "fork" method.

    * that means the decorated_function must not use that kwarg itself, since this kwarg will be popped from the kwargs
    """

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


Subprocess Monitoring
---------------------

when using multiprocessing, the subprocess is monitored if it is still alive.
if the subprocess was terminated or killed (for instance by OOMKiller),
``multiprocessing.context.ProcessError`` will be raised.
By default the subprocess is monitored every 5 seconds, but can be set with parameter
``dec_poll_subprocess``. polling can be turned off by setting to 0.0 seconds

.. code-block:: python

    from wrapt_timeout_decorator import timeout


    @timeout(10, use_signals=False, timeout_exception=TimeoutError, dec_poll_subprocess=1)
    def slow_process() -> None:
        # should have enough time to finish
        # but instead it gets terminated, and the
        # poll the subprocess every second
        logger.error(f"Slow process started at {get_str_time()}")
        time.sleep(5)
        logger.error(f"Slow process done at {get_str_time()}")


    def fake_oom_killer() -> None:
        logger.error(f"Fake OOMKiller started at {get_str_time()}")
        time.sleep(2)
        # kill sibling slow_process
        # hacky way to find it
        target = psutil.Process().parent().children(recursive=True)[-1]
        target.kill()
        logger.error(f"Killed {target.pid} at {get_str_time()}")


    def start_processes() -> None:
        """
        starts the 'fake_oom_killer' and 'slow_process' process -
        and kill 'slow_process' after two seconds

        >>> start_processes()
        Traceback (most recent call last):
            ...
        multiprocessing.context.ProcessError: Function slow_process was terminated or killed after ... seconds
        """
        process_oom_killer = multiprocessing.Process(target=fake_oom_killer, args=())
        process_oom_killer.start()
        slow_process()
        process_oom_killer.join()


    def get_str_time() -> str:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time


    if __name__ == '__main__':
        start_processes()

use as function not as decorator
--------------------------------

You can use the timout also as function, without using as decorator:

.. code-block:: py

    import time
    from wrapt_timeout_decorator import *

    def mytest(message):
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        timeout(dec_timeout=5)(mytest)('starting')

use powerful eval function
--------------------------

This is very powerful, but can be also very dangerous if you accept strings to evaluate from UNTRUSTED input.

read: https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html

If enabled, the parameter of the function dec_timeout, or the parameter passed by kwarg dec_timeout will
be evaluated if its type is string.

You can access :

- "wrapped"
   (the decorated function and its attributes)

- "instance"
   Example: 'instance.x' - an attribute of the instance of the class instance

- "args"
   Example: 'args[0]' - the timeout is the first argument in args

- "kwargs"
   Example: 'kwargs["max_time"] * 2'

- and of course all attributes You can think of - that makes it powerful but dangerous.
   by default allow_eval is disabled - but You can enable it in order to cover some edge cases without
   modifying the timeout decorator.


.. code-block:: py

    # this example does NOT work on windows, please check the section
    # "use with Windows" in the README.rst
    def class FunnyMemes(object):
        def __init__(self,x):
            self.x=x

        @timeout('instance.x', dec_allow_eval=True)
        def swallow(self):
            while True:
                time.sleep(0.5)
                print('swallow')

        @timeout(1)
        def parrot(self):
            while True:
                time.sleep(0.5)
                print('parrot')

        @timeout(dec_timeout='args[0] + kwargs.pop("more_time",0)', dec_allow_eval=True)
        def knight(self,base_delay):
            while True:
                time.sleep(base_delay)
                print('knight')


    def main():
        my_memes = FunnyMemes(2)
        my_memes.swallow()                                                      # this will time out after 2 seconds
        my_memes.swallow(dec_timeout='instance.x * 2 + 1')                      # this will time out after 5 seconds
        my_memes.parrot(dec_timeout='instance.x * 2 + 1', dec_allow_eval=True)  # this will time out after 5 seconds
        my_memes.knight(1,more_time=4)                                          # this will time out after 5 seconds

    if __name__ == '__main__':
        main()

detect pickle errors
--------------------

remember that decorated functions (and their results !) needs to be pickable under Windows. In order to detect pickle problems You can use :

.. code-block:: py

    from wrapt_timeout_decorator import *
    # always remember that the "object_to_pickle" should not be defined within the main context
    detect_unpickable_objects(object_to_pickle, dill_trace=True)  # type: (Any, bool) -> Dict

Logging in decorated functions
------------------------------

when signals=False (on Windows), logging in the wrapped function can be tricky. Since a new process is
created, we can not use the logger object of the main process. Further development is needed to
connect to the main process logger via a socket or queue.

When the wrapped function is using logger=logging.getLogger(), a new Logger Object is created.
Setting up that Logger can be tricky (File Logging from two Processes is not supported ...)
I think I will use a socket to implement that (SocketHandler and some Receiver Thread)

Until then, You need to set up Your own new logger in the decorated function, if logging is needed.
Again - keep in mind that You can not write to the same logfile from different processes !
(although there are logging modules which can do that)

hard timeout
------------

when use_signals = False (this is the only method available on Windows), the timeout function is realized by starting
another process and terminate that process after the given timeout.
Under Linux fork() of a new process is very fast, under Windows it might take some considerable time,
because the main context needs to be reloaded on spawn().
Spawning of a small module might take something like 0.5 seconds and more.

By default, when using signals=False, the timeout begins after the new process is created.

This means that the timeout given, is the time the decorated process is allowed to run, not included the time excluding the time to setup the process itself.
This is especially important if You use small timeout periods :

for Instance:


.. code-block:: py

    @timeout(0.1)
    def test():
        time.sleep(0.2)


the total time to timeout on linux with use_signals = False will be around 0.1 seconds, but on windows this can take
about 0.6 seconds: 0.5 seconds to spawn the new process, and giving the function test() 0.1 seconds to run !

If You need that a decorated function should timeout exactly** after the given timeout period, You can pass
the parameter dec_hard_timeout=True. in this case the called function will timeout exactly** after the given time,
no matter how long it took to spawn the process itself. In that case, if You set up the timeout too short,
the process might never run and will always timeout during spawning.

** well, more or less exactly - it still takes some short time to return from the spawned process - so be extra cautious on very short timeouts !

MYPY Testing
------------
for local MYPY Testing please make sure that the stub file "wrapt.pyi" is in in the MYPY Path (once!), in order to preserve the decorated function signature.

Usage from Commandline
------------------------

.. code-block::

   Usage: wrapt_timeout_decorator [OPTIONS] COMMAND [ARGS]...

     The better timout decorator

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     info  get program informations

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block::

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools

- to install the latest release from PyPi via pip (recommended):

.. code-block::

    python -m pip install --upgrade wrapt_timeout_decorator


- to install the latest release from PyPi via pip, including test dependencies:

.. code-block::

    python -m pip install --upgrade wrapt_timeout_decorator[test]

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/wrapt_timeout_decorator.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    wrapt_timeout_decorator

    # for the latest development version :
    wrapt_timeout_decorator @ git+https://github.com/bitranox/wrapt_timeout_decorator.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version, including test dependencies from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/wrapt_timeout_decorator.git
    $ cd wrapt_timeout_decorator
    python -m pip install -e .[test]

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/wrapt_timeout_decorator.git
    $ cd wrapt_timeout_decorator

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    cli_exit_tools
    lib_detect_testenv

    # class decorators are failing on windows with dill 0.3.5, 0.3.5.1
    dill>0.3.0,!=0.3.5,!=0.3.5.1;sys_platform=="win32"
    dill;sys_platform!="win32"
    multiprocess
    psutil
    wrapt

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/wrapt_timeout_decorator/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

v1.5.0
---------
2024-02-27:
    - thanks to `Alberto Ornaghi: <https://github.com/alor>`_
    - parameter ``dec_mp_reset_signals``
    - restores the default behavior of signal handlers on multiprocessing ``fork``
    - suitible especially for ``FastAPI`` and ``Uvicorn``

v1.4.1
---------
2024-01-10:
    - thanks to `fayak: <https://github.com/fayak>`_
    - omit mypy option --no-implicit-reexport
    - explicitly export methods in ``__init__.py``

v1.4.0
---------
2023-07-13:
    - check for killed child processes (for instance by OOMKiller)
    - change dill requirements for windows
    - require minimum python 3.8
    - remove python 3.7 tests
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove mypy.ini
    - remove pytest.ini
    - remove setup.cfg
    - remove setup.py
    - remove .bettercodehub.yml
    - remove .travis.yml
    - update black config
    - clean ./tests/test_cli.py
    - add codeql badge
    - move 3rd_party_stubs outside the src directory to ``./.3rd_party_stubs``
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v1.3.12.2
---------
2022-06-01: update to github actions checkout@v3 and setup-python@v3

v1.3.12
--------
2022-05-23: update requirements.txt

v1.3.11
--------
2022-05-23:
    - set dill version < 0.3.5 on windows, because decorating class methods fails with dill 0.3.5 upwards
    - update tests to the latest python versions

v1.3.10
--------
2022-04-26: add tests for thread lock

v1.3.9
--------
2022-04-26: preserve Signature of the decorator

v1.3.8
--------
2022-03-29: remedy mypy Untyped decorator makes function "cli_info" untyped

v1.3.7
--------
2022-03-28: extend time on test_timeout_decorator_arg - github macos seems to be slow, so sometimes that test fails

v1.3.6
--------
2022-03-25: fix github actions windows test

v1.3.4
-------
2022-03-23: extend time on test_timeout_ok_timeout_as_kwarg - github macos seems to be slow, so sometimes that test fails

v1.3.3
-------
2022-03-10: extend time on test_timeout_alternate_exception - github macos seems to be slow, so sometimes that test fails

v1.3.2
-------
2022-03-01: github actions pipeline, codestyle black, fix requirements

v1.3.1
-------
2019-09-02: strict mypy static type checking, housekeeping

v1.3.0
-------
2019-05-03: pointing out caveats when using signals, the decorator defaults now to NOT using Signals !

v1.2.9
-------
2019-05-03: support nested decorators, mypy static type checking

v1.2.8
-------
2019-04-23: import multiprocess as multiprocess, not as multiprocessing - that might brake other packages

v1.2.0
------
2019-04-09: initial PyPi release

v1.1.0
-------
2019-04-03: added pickle analyze convenience function

v1.0.9
-------
2019-03-27: added OsX and Windows tests, added parameter dec_hard_timeout for Windows, 100% Code Coverage

v1.0.8
-------
2019-02-26: complete refractoring and code cleaning

v1.0.7
-------
2019-02-25:  fix pickle detection, added some tests, codecov now correctly combining the coverage of all tests

v1.0.6
-------
2019-02-24: fix pickle detection when use_signals = False, drop Python2.6 support since wrapt dropped it.

v1.0.5
-------
2018-09-13: use multiprocessing.pipe instead of queue
If we are not able to use signals, we need to spawn a new process.
This was done in the past by pickling the target function and put it on a queue -
now this is done with a half-duplex pipe.

- it is faster
- it probably can work on Amazon AWS, since there You must not use queues

v1.0.4
-------
2017-12-02: automatic detection if we are in the main thread. Signals can only be used in the main thread. If the decorator is running in a subthread, we automatically disable signals.

v1.0.3
-------
2017-11-30: using dill and multiprocess to enhance windows functionality

v1.0.0
-------
2017-11-10: Initial public release

