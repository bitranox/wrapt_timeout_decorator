there are many timeout decorators out there - that one focuses on correctness when using with Classes, methods,
class methods, static methods and so on, preserving also the traceback information for Pycharm debugging.

There is also a powerful eval function, it allows to read the desired timeout value even from Class attributes.

There are two timeout strategies implemented, the ubiquitous method using "Signals" and the second using Multiprocessing.
Using "Signals" is slick and lean, but there are nasty caveats, please check section `Caveats using Signals`_

The default strategy is therefore using Multiprocessing, but You can also use Signals, You have been warned !

Due to the lack of signals on Windows, or for threaded functions (in a subthread) where signals cant be used, Your only choice is Multiprocessing,
this is set automatically.

Under Windows the decorated function and results needs to be pickable.
For that purpose we use "multiprocess" and "dill" instead of "multiprocessing" and "pickle", in order to be able to use this decorator on more sophisticated objects.
Communication to the subprocess is done via "multiprocess.pipe" instead of "queue", which is faster and might also work on Amazon AWS.
