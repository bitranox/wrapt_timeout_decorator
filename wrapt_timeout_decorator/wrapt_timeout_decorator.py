"""
Timeout decorator.
    :copyright: (c) 2017 by Robert Nowotny
    :license: MIT, see LICENSE for more details.
"""


import dill          # dill is much more tolerant then pickle, so lets use
import multiprocess  # multiprocess instead of multiprocessing
import platform
import signal
import sys
import threading
import wrapt

############################################################
# Timeout
############################################################

# http://www.saltycrane.com/blog/2010/04/using-python-timeout-decorator-uploading-s3/
# Used work of Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>
# Used work of https://github.com/pnpnpn/timeout-decorator

if sys.version_info < (3, 3):
    TimeoutError = AssertionError  # there is no TimeoutError below Python 3.3


def _raise_exception(exception, exception_message):
    """ This function checks if a exception message is given.
    If there is no exception message, the default behaviour is maintained.
    If there is an exception message, the message is passed to the exception.
    """
    if not exception:
        exception = TimeoutError
    raise exception(exception_message)


def _get_bad_pickling_types(object_to_pickle):
    bad_types = list()
    try:
        bad_types = dill.detect.badtypes(object_to_pickle)
    except NotImplementedError:
        pass
    finally:
        return bad_types


def detect_unpickable_objects_and_reraise(object_to_pickle):
    bad_types = _get_bad_pickling_types(object_to_pickle)
    if hasattr(object_to_pickle, '__name__'):
        object_name = object_to_pickle.__name__
    else:
        object_name = 'object'
    s_err = 'can not pickle {on}, bad types {bt}'.format(on=object_name, bt=bad_types)
    raise dill.PicklingError(s_err)

def timeout2(dec_timeout=None, use_signals=True, timeout_exception=None, exception_message=None, dec_allow_eval=False):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        wrap_helper = WrapHelper(dec_timeout, use_signals, timeout_exception, exception_message, dec_allow_eval)
        wrap_helper.get_and_eval_kwargs(kwargs)
        wrap_helper.format_exception_message(wrapped)
        if not wrap_helper.dec_timeout:
            return wrapped(*args, **kwargs)
        else:
            if b_signals:
                try:
                    wrap_helper.save_old_and_set_new_alarm_handler()
                    return wrapped(*args, **kwargs)
                finally:
                    wrap_helper.restore_old_alarm_handler()
            else:
                try:
                    timeout_wrapper = _Timeout(wrapped, wrap_helper.timeout_exception, wrap_helper.exception_message, wrap_helper.dec_timeout)
                    return timeout_wrapper(*args, **kwargs)
                except dill.PicklingError:
                    # sometimes the detection detects unpickable objects but actually
                    # they can be pickled - so we just try to start the thread and report
                    # the unpickable objects if that fails
                    detect_unpickable_objects_and_reraise(wrapped)

    # automatically disable signals when they cant be used
    if can_use_timeout_signals():
        b_signals = use_signals
    else:
        b_signals = False

    return wrapper


class WrapHelper(object):
    def __init__(self, dec_timeout=None, use_signals=True, timeout_exception=None, exception_message=None, dec_allow_eval=False):
        self.dec_timeout = dec_timeout
        self.use_signals = use_signals
        self.timeout_exception = timeout_exception
        self.exception_message = exception_message
        self.dec_allow_eval = dec_allow_eval
        self.old_alarm_handler = None

    def get_and_eval_kwargs(self, kwargs):
        self.dec_allow_eval = kwargs.pop('dec_allow_eval', self.dec_allow_eval)  # make mutable and get possibly kwarg
        decm_timeout = kwargs.pop('dec_timeout', self.dec_timeout)   # make mutable and get possibly kwarg
        if self.dec_allow_eval and isinstance(self.dec_timeout, str):
            self.dec_timeout = eval(self.dec_timeout)                   # if allowed evaluate timeout

    def format_exception_message(self, wrapped):
        if hasattr(wrapped, '__name__'):
            function_name = wrapped.__name__
        else:
            function_name = '(unknown name)'
        if not self.exception_message:
            self.exception_message = 'Function {f} timed out after {s} seconds'.format(f=function_name, s=self.dec_timeout)

    def new_alarm_handler(self,signum, frame):
        _raise_exception(self.timeout_exception, self.exception_message)

    def save_old_and_set_new_alarm_handler(self):
        self.old_alarm_handler = signal.signal(signal.SIGALRM, self.new_alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, self.dec_timeout)

    def restore_old_alarm_handler(self):
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, self.old_alarm_handler)


def timeout(dec_timeout=None, use_signals=True, timeout_exception=None, exception_message=None, dec_allow_eval=False):
    """Add a timeout parameter to a function and return it.

    ToDo : Traceback information when using no_signals
           integrate tblib in order to get exceptions when use_signals=False
           (see https://pypi.python.org/pypi/tblib)

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
                                wrapped (the function object)
                                instance    Example: 'instance.x' - see example above or doku
                                args        Example: 'args[0]' - the timeout is the first argument in args
                                kwargs      Example: 'kwargs["max_time"] * 2'

    * all parameters starting with dec_ can be overridden via kwargs passed to the wrapped function.

    :type dec_timeout:          float
    :type use_signals:          bool
    :type timeout_exception:    Exception
    :type exception_message:    str

    :raises:                    TimeoutError if time limit is reached
    :returns:                   the Result of the wrapped function

    It is illegal to pass anything other than a function as the first parameter.
    The function is wrapped and returned to the caller.
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        exc_msg = exception_message                             # make mutable
        decm_allow_eval = kwargs.pop('dec_allow_eval', dec_allow_eval)  # make mutable and get possibly kwarg
        decm_timeout = kwargs.pop('dec_timeout', dec_timeout)   # make mutable and get possibly kwarg
        if decm_allow_eval and isinstance(dec_timeout, str):
            decm_timeout = eval(decm_timeout)                   # if allowed evaluate timeout
        if not exc_msg:
            exc_msg = 'Function {f} timed out after {s} seconds'.format(f=wrapped.__name__, s=decm_timeout)
        if not decm_timeout:
            return wrapped(*args, **kwargs)
        else:
            if b_signals:
                old_alarm_handler = _return_old_and_set_new_alarm_handler(timeout_exception, exc_msg, decm_timeout)
                try:
                    return wrapped(*args, **kwargs)
                finally:
                    _reset_and_restore_old_alarm_handler(old_alarm_handler)
            else:
                try:
                    timeout_wrapper = _Timeout(wrapped, timeout_exception, exc_msg, decm_timeout)
                    return timeout_wrapper(*args, **kwargs)
                except dill.PicklingError:
                    # sometimes the detection detects unpickable objects but actually
                    # they can be pickled - so we just try to start the thread and report
                    # the unpickable objects if that fails
                    detect_unpickable_objects_and_reraise(wrapped)

    # automatically disable signals when they cant be used
    if can_use_timeout_signals():
        b_signals = use_signals
    else:
        b_signals = False

    return wrapper


def can_use_timeout_signals():
    """ gives True when we can use timeout signals, otherwise False"""
    if platform.system().lower().startswith('win'):  # on Windows we cant use Signals
        return False
    if sys.version_info < (3, 4):
        # on old python use this method - we can only use Signals in the Main Thread
        return isinstance(threading.current_thread(), threading._MainThread)
    else:
        # much nicer after python 3.4 - we can only use Signals in the Main Thread
        return threading.current_thread() == threading.main_thread()


def _target(child_conn, function, *args, **kwargs):
    """Run a function with arguments and return output via a queue.
    This is a helper function for the Process created in _Timeout. It runs
    the function with positional arguments and keyword arguments and then
    returns the function's output by way of a queue. If an exception gets
    raised, it is returned to _Timeout to be raised by the value property.
    """
    try:
        child_conn.send((True, function(*args, **kwargs)))
    except:
        child_conn.send((False, sys.exc_info()[1]))
    finally:
        child_conn.close()


def _return_old_and_set_new_alarm_handler(timeout_exception, exc_msg, decm_timeout):
    def new_alarm_handler(signum, frame):
        _raise_exception(timeout_exception, exc_msg)
    old_alarm_handler = signal.signal(signal.SIGALRM, new_alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, decm_timeout)
    return old_alarm_handler


def _reset_and_restore_old_alarm_handler(old_alarm_handler):
    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.signal(signal.SIGALRM, old_alarm_handler)


class _Timeout(object):

    """Wrap a function and add a timeout (limit) attribute to it.
    Instances of this class are automatically generated by the add_timeout
    function defined above. Wrapping a function allows asynchronous calls
    to be made and termination of execution after a timeout has passed.
    """

    def __init__(self, function, timeout_exception, exception_message, limit):
        """Initialize instance in preparation for being called."""
        self.__limit = limit
        self.__function = function
        self.__timeout_exception = timeout_exception
        self.__exception_message = exception_message
        self.__name__ = function.__name__
        self.__doc__ = function.__doc__
        self.__process = None
        self.__parent_conn = None
        self.__child_conn = None

    def __call__(self, *args, **kwargs):
        """Execute the embedded function object asynchronously.
        The function given to the constructor is transparently called and
        requires that "ready" be intermittently polled. If and when it is
        True, the "value" property may then be checked for returned data.
        """
        self.__parent_conn, self.__child_conn = multiprocess.Pipe(duplex=False)
        args = (self.__child_conn, self.__function) + args
        self.__process = multiprocess.Process(target=_target, args=args, kwargs=kwargs)
        self.__process.daemon = True
        self.__process.start()

        if self.__parent_conn.poll(self.__limit):
            return self.value
        else:
            self.cancel()

    def cancel(self):
        """Terminate any possible execution of the embedded function."""
        self.__parent_conn.close()
        if self.__process.is_alive():
            self.__process.terminate()

        _raise_exception(self.__timeout_exception, self.__exception_message)

    @property
    def value(self):
        flag, load = self.__parent_conn.recv()
        self.__parent_conn.close()
        # when self.__parent_conn.recv() exits, maybe __process is still alive,
        # then it might zombie the process. so join it explicitly
        self.__process.join(1)

        if flag:
            return load
        raise load
