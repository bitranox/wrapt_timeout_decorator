There are several timeout decorators available, but the one mentioned here
focuses on ensuring correctness when used with classes, methods, class methods,
static methods, etc. It also preserves traceback information for PyCharm debugging.

Additionally, there is a powerful eval function that allows reading
the desired timeout value even from class attributes.

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