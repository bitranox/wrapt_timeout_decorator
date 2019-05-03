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

Please note that for some unknown reason, probably in multiprocess, Class methods can not be decorated at all under Windows with Python 2.7

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
