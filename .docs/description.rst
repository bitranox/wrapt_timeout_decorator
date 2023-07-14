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
