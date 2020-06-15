wrapt_timeout_decorator
=======================

.. include:: ./badges_with_jupyter.rst

there are many timeout decorators out there - that one focuses on correctness when using with Classes, methods,
class methods, static methods and so on, preserving also the traceback information for Pycharm debugging.

There is also a powerful eval function, it allows to read the desired timeout value even from Class attributes.

It is very flexible and can be used with python >= 3.5, pypy3 and probably other dialects.

There are two timeout strategies implemented, the ubiquitous method using "Signals" and the second using Multiprocessing.
Using "Signals" is slick and lean, but there are nasty caveats, please check section `Caveats using Signals`_

The default strategy is therefore using Multiprocessing, but You can also use Signals, You have been warned !

Due to the lack of signals on Windows, or for threaded functions (in a subthread) where signals cant be used, Your only choice is Multiprocessing,
this is set automatically.

Under Windows the decorated function and results needs to be pickable.
For that purpose we use "multiprocess" and "dill" instead of "multiprocessing" and "pickle", in order to be able to use this decorator on more sophisticated objects.
Communication to the subprocess is done via "multiprocess.pipe" instead of "queue", which is faster and might also work on Amazon AWS.


.. include:: ./tested_under.rst

----

- `Try it Online`_
- `Installation and Upgrade`_
- `Basic Usage`_
- `General Recommendations`_
- `use with Windows`_
- `Caveats using Signals`_
- `Caveats using Multiprocessing`_
- `nested Timeouts`_
- `Alternative Exception`_
- `Parameters`_
- `Override Parameters`_
- `Multithreading`_
- `use as function not as decorator`_
- `use powerful eval function`_
- `detect pickle errors`_
- `Logging in decorated functions`_
- `hard timeout`_ or - when the timout should start ?
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/{repository_slug}/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/{repository_slug}/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/{repository_slug}/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

.. include:: ./try_in_jupyter.rst


Installation and Upgrade
------------------------

.. include:: ./installation.rst


Basic Usage
-----------
.. include:: ./basic_usage.rst

General Recommendations
-----------------------
dont sprincle Your code with timeouts. Just use it were absolutely necessary, for instance when reading or writing a file. And do that on the lowest
abstraction level possible to avoid unwanted side effects (Exceptions caught by some other code, non pickable functions or arguments, and so on, but not TOO
low. Remember that forking the program takes some time (when use multiprocessing).

Most functions and libraries You call, they HAVE already some timeouts. use those. This Timeout Decorator should be only the last ressort, if everything else
fails.

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



Requirements
------------

following modules will be automatically installed :

.. include:: ../requirements.txt
        :code: shell

Acknowledgements
----------------
.. include:: ./acknowledgment.rst

Contribute
----------
.. include:: ./contribute.rst

License
-------
.. include:: ./licence_mit.rst

-----------------------------------------------------------------

.. Changelog link comes from the included document !

.. include:: ../CHANGES.rst

