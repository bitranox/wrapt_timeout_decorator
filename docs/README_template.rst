wrapt_timeout_decorator
=======================

.. include:: ./badges_with_jupyter.rst

there are many timeout decorators out there - that one focuses on correctness when using with Classes, methods,
class methods, static methods and so on, preserving also the traceback information for Pycharm debugging.

There is also a powerful eval function, it allows to read the desired timeout value even from Class attributes.

It is very flexible and can be used from python 2.7 to python 3.x, pypy, pypy3 and probably other dialects.

Due to the lack of signals and forking on Windows, or for threaded functions where signals cant be used, there is an alternate timeout strategy by using multiprocess.
The decorated function and result needs to be pickable in that case. For that purpose we use "multiprocess" and "dill" instead of "multiprocessing" and "pickle", in order to be able to use this decorator on more sophisticated objects.
Communication to the subprocess is done via "multiprocess.pipe" instead of "queue", which is faster and might also work on Amazon AWS.

.. include:: ./tested_under.rst

----

- `Try it Online`_
- `Installation and Upgrade`_
- `Basic Usage`_
- `use with Windows`_
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

use with Windows
----------------
.. include:: ./use_with_windows.rst

Alternative Exception
---------------------
.. include:: ./alternative_exception.rst

Parameters
----------
.. include:: ./parameters.rst

Override Parameters
-------------------
.. include:: ./override_parameters.rst

Multithreading
--------------
.. include:: ./multithreading.rst

use as function not as decorator
--------------------------------
.. include:: ./use_as_function.rst

use powerful eval function
--------------------------
.. include:: ./use_eval.rst

detect pickle errors
--------------------
.. include:: ./detect_pickle_errors.rst

Logging in decorated functions
------------------------------
.. include:: ./logging.rst

hard timeout
------------
.. include:: ./hard_timeout.rst

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
