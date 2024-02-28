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
