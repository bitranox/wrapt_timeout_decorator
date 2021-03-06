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
