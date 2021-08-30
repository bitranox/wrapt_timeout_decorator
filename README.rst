wrapt_timeout_decorator
=======================

|Pypi Status| |license| |maintenance| |jupyter|

|Build Status| |Codecov Status| |Better Code| |code climate| |code climate coverage| |snyk security|

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License
.. |maintenance| image:: https://img.shields.io/maintenance/yes/2021.svg
.. |Build Status| image:: https://travis-ci.org/bitranox/wrapt_timeout_decorator.svg?branch=master
   :target: https://travis-ci.org/bitranox/wrapt_timeout_decorator
.. for the pypi status link note the dashes, not the underscore !
.. |Pypi Status| image:: https://badge.fury.io/py/wrapt-timeout-decorator.svg
   :target: https://badge.fury.io/py/wrapt_timeout_decorator
.. |Codecov Status| image:: https://codecov.io/gh/bitranox/wrapt_timeout_decorator/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/wrapt_timeout_decorator
.. |Better Code| image:: https://bettercodehub.com/edge/badge/bitranox/wrapt_timeout_decorator?branch=master
   :target: https://bettercodehub.com/results/bitranox/wrapt_timeout_decorator
.. |snyk security| image:: https://snyk.io/test/github/bitranox/wrapt_timeout_decorator/badge.svg
   :target: https://snyk.io/test/github/bitranox/wrapt_timeout_decorator
.. |jupyter| image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=jupyter_test_wrapt_timeout_decorator.ipynb
.. |code climate| image:: https://api.codeclimate.com/v1/badges/2b2b6589f80589689c2b/maintainability
   :target: https://codeclimate.com/github/bitranox/wrapt_timeout_decorator/maintainability
   :alt: Maintainability
.. |code climate coverage| image:: https://api.codeclimate.com/v1/badges/2b2b6589f80589689c2b/test_coverage
   :target: https://codeclimate.com/github/bitranox/wrapt_timeout_decorator/test_coverage
   :alt: Code Coverage

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

automated tests, Travis Matrix, Documentation, Badges for this Project are managed with `lib_travis_template <https://github
.com/bitranox/lib_travis_template>`_ - check it out

supports python 3.6-3.8, pypy3 and possibly other dialects.

`100% code coverage <https://codecov.io/gh/bitranox/wrapt_timeout_decorator>`_, mypy static type checking, tested under `Linux, macOS, Windows and Wine <https://travis-ci
.org/bitranox/wrapt_timeout_decorator>`_, automatic daily builds  and monitoring

----

- `Try it Online`_
- `Installation and Upgrade`_
- `Usage`_
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
- `Report Issues <https://github.com/bitranox/wrapt_timeout_decorator/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/wrapt_timeout_decorator/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/wrapt_timeout_decorator/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/bitranox/wrapt_timeout_decorator/master?filepath=jupyter_test_wrapt_timeout_decorator.ipynb>`_

Installation and Upgrade
------------------------

Before You start, its highly recommended to update pip and setup tools:


.. code-block:: bash

    python3 -m pip --upgrade pip
    python3 -m pip --upgrade setuptools
    python3 -m pip --upgrade wheel


install latest version with pip (recommended):

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    python3 -m pip install --upgrade git+https://github.com/bitranox/wrapt_timeout_decorator.git --upgrade-strategy eager

    # test without installing (can be skipped)
    python3 -m pip install git+https://github.com/bitranox/wrapt_timeout_decorator.git --install-option test

    # normal install
    python3 -m pip install --upgrade git+https://github.com/bitranox/wrapt_timeout_decorator.git


install latest pypi Release (if there is any):

.. code-block:: bash

    # latest Release from pypi
    python3 -m pip install --upgrade wrapt_timeout_decorator

    # test without installing (can be skipped)
    python3 -m pip install wrapt_timeout_decorator --install-option test

    # normal install
    python3 -m pip install --upgrade wrapt_timeout_decorator



include it into Your requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi (if any):
    wrapt_timeout_decorator
    # for the latest Development Version :
    wrapt_timeout_decorator @ git+https://github.com/bitranox/wrapt_timeout_decorator.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python3 -m pip install --upgrade -r /<path>/requirements.txt


Install from source code:

.. code-block:: bash

    # cd ~
    $ git clone https://github.com/bitranox/wrapt_timeout_decorator.git
    $ cd wrapt_timeout_decorator

    # test without installing (can be skipped)
    python3 setup.py test

    # normal install
    python3 setup.py install


via makefile:

if You are on linux, makefiles are a very convenient way to install. Here we can do much more, like installing virtual environment, clean caches and so on.
This is still in development and not recommended / working at the moment:

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

Usage
-----------

.. include:: ./parts/basic_usage.rst
.. include:: ./parts/general_recommendations.rst
.. include:: ./parts/use_with_windows.rst
.. include:: ./parts/caveats_using_signals.rst
.. include:: ./parts/caveats_using_no_signals.rst
.. include:: ./parts/nested_timeouts.rst
.. include:: ./parts/alternative_exception.rst
.. include:: ./parts/parameters.rst
.. include:: ./parts/override_parameters.rst
.. include:: ./parts/multithreading.rst
.. include:: ./parts/use_as_function.rst
.. include:: ./parts/use_eval.rst
.. include:: ./parts/detect_pickle_errors.rst
.. include:: ./parts/logging.rst
.. include:: ./parts/hard_timeout.rst

Usage from Commandline
------------------------

.. code-block:: bash

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    dill
    multiprocess
    wrapt

Acknowledgements
----------------

- derived from `pnp timeout decorator <https://github.com/pnpnpn/timeout-decorator>`_
- inspiration from `salty cranes blog <http://www.saltycrane.com/blog/2010/04/using-python-timeout-decorator-uploading-s3/>`_
- thanks to abadger1999 for `pointing out caveats when using signals <https://anonbadger.wordpress.com/2018/12/15/python-signal-handlers-and-exceptions/>`_
- thanks to Marco Aurélio da Costa for pointing out that `the decorated function needs to be terminable with SIGTERM <https://github.com/bitranox/wrapt_timeout_decorator/issues/18>`_
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

1.3.1
-----
2019-09-02: strict mypy static type checking, housekeeping

1.3.0
-----
2019-05-03: pointing out caveats when using signals, the decorator defaults now to NOT using Signals !

1.2.9
-----
2019-05-03: support nested decorators, mypy static type checking

1.2.8
-----
2019-04-23: import multiprocess as multiprocess, not as multiprocessing - that might brake other packages

1.2.0
------
2019-04-09: initial PyPi release

1.1.0
-----
2019-04-03: added pickle analyze convenience function

1.0.9
-----
2019-03-27: added OsX and Windows tests, added parameter dec_hard_timeout for Windows, 100% Code Coverage

1.0.8
-----
2019-02-26: complete refractoring and code cleaning

1.0.7
-----
2019-02-25:  fix pickle detection, added some tests, codecov now correctly combining the coverage of all tests

1.0.6
-----
2019-02-24: fix pickle detection when use_signals = False, drop Python2.6 support since wrapt dropped it.

1.0.5
-----
2018-09-13: use multiprocessing.pipe instead of queue
If we are not able to use signals, we need to spawn a new process.
This was done in the past by pickling the target function and put it on a queue -
now this is done with a half-duplex pipe.

- it is faster
- it probably can work on Amazon AWS, since there You must not use queues

1.0.4
-----

2017-12-02: automatic detection if we are in the main thread. Signals can only be used in the main thread. If the decorator is running in a subthread, we automatically disable signals.


1.0.3
-----

2017-11-30: using dill and multiprocess to enhance windows functionality


1.0.0
-----

2017-11-10: Initial public release

