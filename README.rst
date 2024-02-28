wrapt_timeout_decorator
=======================


Version v1.5.1 as of 2024-02-28 see `Changelog`_

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

The timeout can be dynamically adjusted, calculated from other parameters or methods accessible via an optional eval function.

Two timeout strategies have been implemented:
one using "Signals" and the other using "Subprocess".

Signals Strategy
----------------

The "Signals" strategy (for POSIX Systems) is elegant and efficient,
but it has some important caveats which should be reviewed
in the `Considerations using Signals`_ section.


Subprocess Strategy (the default)
---------------------------------

The utilization of subprocesses serves as the default approach for executing timeouts:

- **Windows Compatibility**:
        Given the absence of signal support,
        subprocesses become the sole method for implementing timeouts on Windows,
        automatically applied to accommodate the platform's limitations.
        On Windows the only available startmethod for subprocesses is ``spawn``
- **POSIX Systems**:
        On POSIX-compliant systems, signals cannot be employed within
        subthreads, necessitating the use of subprocesses in these contexts as well.
        On POSIX the available startmethods for subprocesses are ``fork``, ``forkserver``, ``spawn``

To ensure compatibility and functionality across subprocesses,
it's essential that as many object types as possible are pickleable.
To this end, the ``dill`` library is preferred over Python's standard ``pickle`` module,
and ``multiprocess`` is chosen instead of ``multiprocessing``.
``dill`` enhances the pickle module's capabilities, extending support for
serialization and deserialization of a broader array of Python object types.

Subprocess communication is facilitated through ``multiprocess.pipe`` rather than ``queue``.
This choice not only boosts performance but also enhances compatibility,
potentially offering better support for environments like Amazon AWS.

Subprocesses can be initiated using various methods,
including 'fork', 'forkserver', and 'spawn'.
For detailed information on these methods and their implications,
please refer to Section `Considerations using Subprocesses`_ of this manual.

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

- `Basic Usage`_
- `General Recommendations`_
- `use with Windows`_
    - `Quick Guide for the Eager`_
    - `In-Depth Explanation for the Curious`_
    - `Windows Compatibility Issue`_
    - `Timing Considerations`_
- `Considerations using Signals`_
- `Considerations using Subprocesses`_
    - `Overview`_
    - `Initialization`_
    - `Process Execution and Communication`_
    - `Subprocess Start Methods`_
    - `Choosing the Right Start Method`_
    - `Setting the Start Method`_
    - `Special Considerations for Uvicorn, FastAPI, asyncio`_
- `Handling Nested Timeouts`_
- `Custom Timeout Exception`_
- `Parameters`_
- `Override Parameters`_
- `Multithreading`_
- `Subprocess Monitoring`_
- `use as function not as decorator`_
- `Dynamic Timeout Value Adjustment with eval`_
- `Tools`_
    - `detect pickle errors`_
    - `set_subprocess_starting_method`_
- `Logging Challenges with Subprocesses`_
- `hard timeout`_
- `Understanding Timeout Durations Across Platforms`_
- `MYPY Testing`_

Basic Usage
-----------

.. code-block:: python

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

It's recommended to minimize the utilization of timeouts in your programming, reserving them for truly essential instances.

Timers should be applied at an appropriate level of detail, tailored specifically to the needs of your application.
This precision aids in circumventing unwanted outcomes, such as the mishandling of exceptions by unrelated code sections
or complications with entities that cannot be pickled.

Conversely, it's prudent to refrain from embedding a Timeout Decorator within loops that execute multiple times.
Such an approach can induce notable delays, especially on Windows systems, owing to the additional burden of initiating subprocesses.

Where possible, opt for the timeout features natively available in the functions and libraries at your disposal.
These inherent capabilities are often adequate for the majority of use cases.
The implementation of a Timeout Decorator is best reserved as a measure of last resort,
subsequent to the exhaustive consideration of alternative strategies.

Additionally, be cognizant of the fact that the behavior and efficiency of subprocesses may vary significantly across platforms
(Windows versus Linux) and depending on the chosen method for subprocess initiation.
Refer to the documentation on `Subprocess Start Methods`_ for further details.


    BAD EXAMPLE (Pseudocode) - lets assume the write to the database fails sometimes for unknown reasons, and "hangs"

    .. code-block:: python

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

    .. code-block:: python

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

Quick Guide for the Eager
-------------------------
To bypass complexities, simply place the decorated function within a separate module, rather than in the main script.

In-Depth Explanation for the Curious
------------------------------------
On Windows, due to the absence of native forking support, Python attempts to emulate a forking environment.
This emulation involves re-importing the main module under a different name, not as '__main__'.
This behavior is part of Python's multiprocessing efforts to replicate the main process's environment as closely as possible.
Consequently, it's crucial to protect the entry point of your application with the well-known conditional statement
"if __name__ == '__main__':".


.. code-block:: py

    import lib_foo

    def some_module():
        lib_foo.function_foo()

    def main():
        some_module()


    # here the subprocess stops loading, because __name__ is NOT '__main__'
    if __name__ = '__main__':
        main()


Windows Compatibility Issue
---------------------------
The challenge arises from Windows OS's lack of support for the "fork" process model, a limitation not present in Unix-based systems.

Further details can be explored through these resources:

- [Stack Overflow discussion on multiprocessing and `__name__ == '__main__'`](https://stackoverflow.com/questions/45110287/workaround-for-using-name-main-in-python-multiprocessing)
- [Python's multiprocessing documentation for Windows](https://docs.python.org/2/library/multiprocessing.html#windows)

Due to this, when `main.py` is re-imported under a name different from `"__main__"`, references within decorated classes
and functions become invalid. To circumvent this, it's advisable to house decorated entities in a separate module.
Generally, and particularly on Windows, the `main()` function should be streamlined to act merely as an entry point,
with the substantive logic residing in modules.
Additionally, storing settings or configurations in a distinct file is beneficial for centralized access and to leverage features
like type hints and auto-completion in your preferred IDE.

The `dill` serializer, chosen for its broader compatibility, successfully serializes the `__main__` context,
enabling objects to be pickled to `"__main__.lib_foo"`, `"__main__.some_module"`, `"__main__.main"`, etc.
This overcomes the limitations faced when using `pickle`, which cannot serialize various types including functions
with yields, nested functions, and more.
`Dill` enhances functionality by enabling the saving/loading of Python sessions, extraction of source code, and interactive debugging of serialization errors.
However, it necessitates that decorated methods and classes not be defined in the `__main__` context but within a module.

For more insights on serialization with `pickle` or `dill`:
- [Stack Overflow discussion on serializing objects in `__main__` with `pickle` or `dill`](https://stackoverflow.com/questions/45616584/serializing-an-object-in-main-with-pickle-or-dill)

Timing Considerations
---------------------
Given the variable duration of the spawning process (due to re-importing modules),
the `hard timeout`_ section provides guidance on configuring the commencement of timeouts.


An illustration highlights a scenario functional on Linux but problematic on Windows,
where the variable `"name"` and the function `"sleep"` are not recognized in the spawned process:


.. code-block:: python

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


.. code-block:: python


    # my_program_main.py:

    import lib_test

    def main():
        lib_test.mytest()

    if __name__ == '__main__':
        main()


.. code-block:: python


        # conf_my_program.py:

        class ConfMyProgram(object):
            def __init__(self):
                self.name:str = 'my_var_name'

        conf_my_program = ConfMyProgram()


.. code-block:: python

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

Considerations using Signals
----------------------------

ABADGER1999 highlights in his `blog post <https://anonbadger.wordpress.com/2018/12/15/python-signal-handlers-and-exceptions/>`_ the
potential pitfalls of using signals alongside the TimeoutException.
This approach may not be advisable as the exception can be intercepted within the decorated function.

While it's possible to implement a custom Exception derived from the Base Exception Class,
this doesn't guarantee the code will behave as anticipated.
For an illustrative example, you're encouraged to conduct an experiment using a
`Jupyter notebook <https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=jupyter_test_{repository}.ipynb>`_.


.. code-block:: python

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

Considerations using Subprocesses
---------------------------------

Overview
--------
Subprocesses ares utilized by default to implement timeout functionality. This involves forking or spawning subprocesses, each with its own set of
considerations and caveats.

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

Subprocess Start Methods
------------------------
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
Configure the start method with ``multiprocessing.set_start_method(method, force=True)``. This should be done cautiously, ideally once, and within the ``if
__name__ == '__main__'`` block to prevent unintended effects.
Since we use ``multiprocess`` instead of ``multiprocessing``, we provide a method to set the starting method on both at the same time.
see : `set_subprocess_starting_method`_

Special Considerations for Uvicorn, FastAPI, asyncio
----------------------------------------------------
For Uvicorn or FastAPI applications, a specific approach to the `fork` method is recommended to ensure proper signal handling and isolation, facilitated by the ``dec_mp_reset_signals`` parameter.
This design aims to reset signal handlers and manage file descriptors in child processes effectively.
You can set that by passing the parameter ``dec_mp_reset_signals=True`` to the decorator.

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

Custom Timeout Exception
------------------------

Define a different exception to be raised upon timeout:

.. code-block::  python

    import time
    from wrapt_timeout_decorator import *

    # this will throw StopIteration Error instead of TimeoutError
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

.. code-block::  python

    @timeout(dec_timeout, use_signals, timeout_exception, exception_message,
             dec_allow_eval, dec_hard_timeout, dec_mp_reset_signals)
    def decorated_function(*args, **kwargs):
        # interesting things happens here ...
        ...



- dec_timeout
    This parameter sets the timeout duration. It accepts a float, integer, or a string
    that can be evaluated to a number if dec_allow_eval is enabled.
    By default, there's no timeout (None). You can change the timeout dynamically
    by passing a dec_timeout keyword argument to the decorated function.

- use_signals
    This boolean parameter controls whether to use UNIX signals for implementing timeouts.
    It's the most accurate method but comes with certain limitations,
    such as being available only on Linux and macOS, and only in the main thread.
    By default, signals are not used (False). It's typically not necessary to modify
    this setting manually, but you can override it by passing 'use_signals=True' to the decorated function.

- timeout_exception
    Specifies the exception to raise when a timeout occurs.
    by default, it's set to TimeoutError
    type: exception
    default: TimeoutError

- exception_message
    You can customize the message of the timeout exception.
    The default message includes the name of the function and the timeout duration.
    This message gets formatted with the actual values when a timeout occurs.
    type: str
    default : 'Function {function_name} timed out after {dec_timeout} seconds' (will be formatted)

- dec_allow_eval
    When enabled (True), this boolean parameter allows the dec_timeout string to be evaluated dynamically.
    It provides access

    - to the decorated function (wrapped),
    - the instance it belongs to (instance),
    - the positional arguments (args),
    - and keyword arguments (kwargs).

    It's disabled (False) by default for safety reasons but can be enabled by passing a dec_allow_eval
    keyword argument to the decorated function.

                    instance    Example: 'instance.x' - see example above or doku
                    args        Example: 'args[0]' - the timeout is the first argument in args
                    kwargs      Example: 'kwargs["max_time"] * 2'
                    type: bool
                    default: false
                    see section "Dynamic Timeout Value Adjustment with eval" in the manual

- dec_hard_timeout
    This boolean parameter is relevant when signals cannot be used,
    necessitating the creation of a new process for the timeout mechanism.
    Setting it to True means the timeout strictly applies to the execution time of the function,
    potentially not allowing enough time for process creation.
    With False, the process creation time is not included in the timeout, giving the actual function
    the full duration to execute.
    You can override this setting by passing a dec_hard_timeout keyword argument to the decorated function.
    type: bool
    default: false
    can be overridden by passing the kwarg dec_hard_timeout to the decorated function*

- dec_mp_reset_signals
    This parameter is relevant when using the "fork" start method for multiprocessing.
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

Override Parameters
-------------------

decorator parameters starting with \dec_* and use_signals can be overridden by kwargs with the same name :

.. code-block:: python


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

Signals will not work if your function is not executed in the main thread.
``use_signals`` is therefore automatically disabled (if set) when the function is not running in the main thread.


.. code-block:: python

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

Subprocess Monitoring
---------------------

when using subprocesses, the subprocess is monitored if it is still alive.
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

.. code-block:: python

    import time
    from wrapt_timeout_decorator import *

    def mytest(message):
        print(message)
        for i in range(1,10):
            time.sleep(1)
            print('{} seconds have passed'.format(i))

    if __name__ == '__main__':
        timeout(dec_timeout=5)(mytest)('starting')

Dynamic Timeout Value Adjustment with eval
------------------------------------------

The timeout value can be dynamically adjusted, calculated from other parameters or methods accessible via the eval function.
This capability is highly potent yet bears significant risks, especially when evaluating strings from UNTRUSTED sources.

.. caution::

   Utilizing eval with untrusted input is perilous.
   For an in-depth understanding, refer to `this article by Ned Batchelder <https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html>`_.

When activated, the ``dec_timeout`` function parameter,
or the value passed through the ``dec_timeout`` keyword argument (kwarg), will undergo evaluation if it's a string type.

Accessible objects within the eval context include:

- **wrapped**: Represents the decorated function and its attributes.

- **instance**: Accesses attributes of the class instance, e.g., ``'instance.x'`` refers to an attribute ``x`` of the instance.

- **args**: Refers to positional arguments, e.g., ``'args[0]'`` might be used to indicate the first argument is the timeout.

- **kwargs**: Accesses keyword arguments, e.g., ``'kwargs["max_time"] * 2'`` doubles the value of ``max_time``.

These elements underscore the feature's versatility but also highlight its potential hazards.
By default, ``allow_eval`` is turned off to mitigate risks.
However, it can be enabled to address specific use cases without altering the timeout decorator's core functionality.


.. code-block:: python

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

Tools
-----

detect pickle errors
--------------------

Keep in mind that when employing subprocesses, both decorated functions and their return values must be pickleable.
To identify issues with pickling, you can utilize the ``detect_unpickable_objects`` function:

.. code-block:: python

    from wrapt_timeout_decorator import *
    detect_unpickable_objects(object_to_pickle, dill_trace=True)


set_subprocess_starting_method
------------------------------

Set the start Method for Subprocesses. Since we use multiprocess,
we set the starting method for multiprocess and multiprocessing to the same value.
we did not test what would happen if we set that to different values.

    - Windows Limitation: Only `spawn` is available on Windows.
    - Linux/Unix Options: Options include `fork`, `forkserver`, and `spawn`.
        - fork:
            Efficiently clones the parent process, including memory space,
            but may lead to issues with shared resources or in multi-threaded applications.
        - forkserver:
            Starts a server at program launch, creating new processes upon request
            for better isolation but at a slower pace due to the server communication requirement.
        - spawn:
            Initiates a fresh Python interpreter process, ensuring total independence
            at the cost of slower start-up due to the need for full initialization.

    - Choosing the Right Start Method
        - fork
            offers speed but can encounter issues with resource sharing or threading.
        - forkserver
            enhances stability and isolation, ideal for applications requiring safety or managing unstable resources.
        - spawn
            provides the highest level of isolation, recommended for a clean start and avoiding shared state complications.

    - Setting the Start Method
        Configure the start method with `set_subprocess_starting_method(method)`
        This should be done cautiously, ideally once, and within the `if __name__ == '__main__'` block to prevent unintended effects.

.. code-block:: python

    from wrapt_timeout_decorator import *
    set_subprocess_starting_method("forkserver")

Logging Challenges with Subprocesses
------------------------------------

When `signals=False` is set, implementing logging within a subprocess poses challenges.
A new process does not inherit the main process's logger object, necessitating further development
for integration with the main process's logger via mechanisms like sockets or queues.

Utilizing `logger=logging.getLogger()` within the wrapped function results in the instantiation of a new Logger Object.
Configuring this Logger, especially for file logging from concurrent processes, presents complications as direct file
logging from multiple processes is generally unsupported.
A potential solution involves employing a SocketHandler coupled with a Receiver Thread to facilitate logging.

In the interim, it's necessary to initialize a separate logger within the decorated function for logging purposes.
It's crucial to remember that writing to the same logfile from multiple processes is not advisable.
While certain logging modules may offer solutions for concurrent logging, they require specific setup and configuration.

hard timeout
------------

When employing subprocesses (which is the default behavior), the timeout functionality is achieved by initiating
a new subprocess and terminating it once the specified timeout period elapses.
The process creation speed varies significantly between operating systems.
On Linux, the ``fork()`` method allows rapid creation of a new process.
In contrast, on Windows, the ``spawn()`` method can introduce a noticeable delay due to the necessity of reloading the main context,
with spawning a small module potentially taking upwards of 0.5 seconds.

The timeout duration commences subsequent to the creation of the new process.
Consequently, the specified timeout reflects the period the decorated function is permitted to execute,
exclusive of the process setup time. This distinction is particularly vital for scenarios utilizing brief timeout intervals:

.. code-block:: py

    @timeout(0.1)
    def test():
        time.sleep(0.2)


Understanding Timeout Durations Across Platforms
------------------------------------------------

The implementation of timeouts, yields different total timeout durations on Linux (fork, forkserver) compared to Windows (spawn).
On Linux, the timeout process may for instance complete in approximately 0.1 seconds with "fork".
Conversely, on Windows, the total time to reach timeout could extend for instance to about 0.6 seconds,
comprising a 0.5-second delay to spawn a new process and then allowing 0.1 seconds for the function ``test()`` to execute.

To enforce a decorated function to timeout strictly after the specified timeout period,
you may use the ``dec_hard_timeout=True`` parameter.

With this setting, the targeted function will timeout precisely after the designated duration after start,
regardless of the process spawning time.
However, setting a very short timeout with this option may prevent the process from running at all,
resulting in an immediate timeout upon spawning.

.. note::

   The term "precisely" should be interpreted with a degree of flexibility.
   There remains a negligible delay in returning from the spawned process, making it imperative to approach very short timeouts with caution.

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

- Before You start, its highly recommended to update pip:


.. code-block::

    python -m pip --upgrade pip

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

v1.5.1
---------
2024-02-28:
    - overhaul documentation
    - github actions/checkout@v4
    - github actions/setup-python@v5

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

