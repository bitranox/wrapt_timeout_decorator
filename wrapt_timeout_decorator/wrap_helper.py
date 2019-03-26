import dill
import platform
import signal
import sys
import threading

if sys.version_info < (3, 3):
    TimeoutError = AssertionError  # there is no TimeoutError below Python 3.3


class WrapHelper(object):
    def __init__(self, dec_timeout=None, use_signals=True, timeout_exception=None,
                 exception_message=None, dec_allow_eval=False):
        self.dec_timeout = dec_timeout
        self.use_signals = use_signals
        self.timeout_exception = timeout_exception
        self.exception_message = exception_message
        self.dec_allow_eval = dec_allow_eval
        self.old_alarm_handler = None

    def get_kwargs(self, kwargs):
        self.dec_allow_eval = kwargs.pop('dec_allow_eval', self.dec_allow_eval)  # make mutable and get possibly kwarg
        self.dec_timeout = kwargs.pop('dec_timeout', self.dec_timeout)   # make mutable and get possibly kwarg
        self.use_signals = kwargs.pop('use_signals', self.use_signals)   # make mutable and get possibly kwarg

    @property
    def should_eval(self):
        if self.dec_allow_eval and isinstance(self.dec_timeout, str):
            return True
        else:
            return False

    def format_exception_message(self, wrapped):
        function_name = wrapped.__name__
        if not function_name:
            function_name = '(unknown name)'
        if not self.exception_message:
            self.exception_message = 'Function {f} timed out after {s} seconds'.format(f=function_name, s=self.dec_timeout)

    def new_alarm_handler(self, signum, frame):
        raise_exception(self.timeout_exception, self.exception_message)

    def save_old_and_set_new_alarm_handler(self):
        self.old_alarm_handler = signal.signal(signal.SIGALRM, self.new_alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, self.dec_timeout)

    def restore_old_alarm_handler(self):
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, self.old_alarm_handler)

    def set_signals_to_false_if_not_possible(self):
        if self.is_system_windows() or not self.is_in_main_thread():
            self.use_signals = False

    @staticmethod
    def is_system_windows():
        if platform.system().lower().startswith('win'):
            return True
        else:
            return False

    def is_in_main_thread(self):
        if sys.version_info < (3, 4):
            return self.is_in_main_thread_pre_python_3_4()
        else:
            return self.is_in_main_thread_from_python_3_4_up()

    @staticmethod
    def is_in_main_thread_pre_python_3_4():
        # old python versions below 3.4
        if isinstance(threading.current_thread(), threading._MainThread):
            return True
        else:
            return False

    @staticmethod
    def is_in_main_thread_from_python_3_4_up():
        # python versions from 3.4 up
        if threading.current_thread() == threading.main_thread():
            return True
        else:
            return False

    def detect_unpickable_objects_and_reraise(self, object_to_pickle):
        # sometimes the detection detects unpickable objects but actually
        # they can be pickled - so we just try to start the thread and report
        # the unpickable objects if that fails
        bad_types = self.get_bad_pickling_types(object_to_pickle)
        if hasattr(object_to_pickle, '__name__'):
            object_name = object_to_pickle.__name__
        else:
            object_name = 'object'
        s_err = 'can not pickle {on}, bad types {bt}'.format(on=object_name, bt=bad_types)
        raise dill.PicklingError(s_err)

    @staticmethod
    def get_bad_pickling_types(object_to_pickle):
        bad_types = list()
        try:
            bad_types = dill.detect.badtypes(object_to_pickle)
        except NotImplementedError:
            pass
        finally:
            return bad_types


def raise_exception(exception, exception_message):
    """ This function checks if a exception message is given.
    If there is no exception message, the default behaviour is maintained.
    If there is an exception message, the message is passed to the exception.
    """
    if not exception:
        exception = TimeoutError
    raise exception(exception_message)
