Changelog
=========

v1.3.5
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
