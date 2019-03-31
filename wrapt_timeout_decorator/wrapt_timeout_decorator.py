"""
Timeout decorator.
    :copyright: (c) 2017 by Robert Nowotny
    :license: MIT, see LICENSE for more details.
"""

from dill import PicklingError
from typing import Union, Callable
import wrapt
from .wrap_helper import WrapHelper
from.wrap_function_multiprocess import Timeout


def timeout(dec_timeout=None, use_signals=True, timeout_exception=None, exception_message=None,
            dec_allow_eval=False, dec_hard_timeout=False):

    # type: (Union[None, float, str], bool, Exception, str, bool, bool) -> Callable

    """Add a timeout parameter to a function and return it.

    ToDo :   Traceback information when use_signals=False (see https://pypi.python.org/pypi/tblib)
             connect the Logger of the Subprocess to the main logger when use_signals=False
             makes life easier on Windows

    Windows remark : dont use the decorator on classes in the main.py because of Windows multiprocessing limitations
                     read the README

    Usage:

    @timeout(3)
    def foo():
        pass

    Overriding the timeout:

    foo(dec_timeout=5)

    Usage without decorating a function :

    def test_method(a,b,c):
        pass

    timeout(3)(test_method)(1,2,c=3)

    Usage with eval (beware, security hazard, no user input values here):
        read : https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html before usage !

    def class ClassTest4(object):
        def __init__(self,x):
            self.x=x

        @timeout('instance.x', dec_allow_eval=True)
        def test_method(self):
            print('swallow')

        @timeout(1)
        def foo3(self):
            print('parrot')

    # or override via kwarg :
    my_foo = ClassTest4(3)
    my_foo.test_method(dec_timeout='instance.x * 2.5 +1')
    my_foo.foo3(dec_timeout='instance.x * 2.5 +1', dec_allow_eval=True)

    :param dec_timeout: *       optional time limit in seconds or fractions of a second. If None is passed,
                                no seconds is applied. This adds some flexibility to the usage: you can disable timing
                                out depending on the settings. dec_timeout will always be overridden by a
                                kwarg passed to the wrapped function, class or class method.
    :param use_signals:         flag indicating whether signals should be used or the multiprocessing
                                when using multiprocessing, timeout granularity is limited to 10ths of a second.
    :param timeout_exception:   the Exception to be raised when timeout occurs, default = TimeoutException
    :param exception_message:   the Message for the Exception. Default: 'Function {f} timed out after {s} seconds.
    :param dec_allow_eval: *    allows a string in parameter dec_timeout what will be evaluated. Beware this can
                                be a security issue. This is very powerful, but is also very dangerous if you
                                accept strings to evaluate from untrusted input.
                                read: https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html

                                If enabled, the parameter of the function dec_timeout, or the parameter passed
                                by kwarg dec_timeout will be evaluated if its type is string. You can access :
                                wrapped (the function object and all their exposed objects)
                                instance    Example: 'instance.x' - see example above or doku
                                args        Example: 'args[0]' - the timeout is the first argument in args
                                kwargs      Example: 'kwargs["max_time"] * 2'

    :param dec_hard_timeout:    only considered when use_signals = True (Windows)
                                if dec_hard_timeout = True, the decorator will timeout after dec_timeout after the
                                decorated function is called by the main program.
                                If You set up a small timeout value like 0.1 seconds, in windows that function might
                                actually never run - because setting up the process will already take longer
                                then 0.1 seconds - that means the decorated function will ALWAYS time out (and never run).

                                if dec_hard_timeout = False, the decorator will timeout after the process is allowed to
                                run for dec_timeout seconds, that means the time to set up the new process is not considered.
                                If You set up a small timeout value like 0.1 seconds, in windows that function might now
                                take something like 0.6 seconds to timeout - 0.5 seconds to set up the process, and
                                allowing the function in the process to run for 0.1 seconds.
                                Since You can not know how long the spawn() will take under Windows, this is the default setting.

    * all parameters starting with dec_ can be overridden via kwargs passed to the wrapped function.

    :raises:                    TimeoutError if time limit is reached
    :returns:                   the Result of the wrapped function

    It is illegal to pass anything other than a function as the first parameter.
    The function is wrapped and returned to the caller.
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        wrap_helper = WrapHelper(dec_timeout, use_signals, timeout_exception, exception_message, dec_allow_eval, dec_hard_timeout)
        wrap_helper.get_kwargs(kwargs)
        wrap_helper.set_signals_to_false_if_not_possible()
        if wrap_helper.should_eval:
            wrap_helper.dec_timeout = eval(str(wrap_helper.dec_timeout))
        wrap_helper.format_exception_message(wrapped)
        if not wrap_helper.dec_timeout:
            return wrapped(*args, **kwargs)
        else:
            if wrap_helper.use_signals:
                try:
                    wrap_helper.save_old_and_set_new_alarm_handler()
                    return wrapped(*args, **kwargs)
                finally:
                    wrap_helper.restore_old_alarm_handler()
            else:
                try:
                    timeout_wrapper = Timeout(wrapped, wrap_helper.timeout_exception,
                                              wrap_helper.exception_message, wrap_helper.dec_timeout, wrap_helper.dec_hard_timeout)
                    return timeout_wrapper(*args, **kwargs)
                except PicklingError:
                    wrap_helper.detect_unpickable_objects_and_reraise(wrapped)
    return wrapper
