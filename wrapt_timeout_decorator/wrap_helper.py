import dill
import logging
import platform
import signal
import sys
import threading
from typing import Any, Dict

logging.basicConfig()
logger = logging.getLogger('pickle_analyzer')

if sys.version_info < (3, 3):
    TimeoutError = AssertionError  # there is no TimeoutError below Python 3.3


class WrapHelper(object):
    def __init__(self, dec_timeout=None, use_signals=True, timeout_exception=None,
                 exception_message=None, dec_allow_eval=False, dec_hard_timeout=False,
                 wrapped=None, instance=None, args=None, kwargs=None):
        self.dec_timeout = dec_timeout
        self.use_signals = use_signals
        self.timeout_exception = timeout_exception
        self.exception_message = exception_message
        self.dec_allow_eval = dec_allow_eval
        self.dec_hard_timeout = dec_hard_timeout
        self.old_alarm_handler = None
        self.wrapped = wrapped
        self.instance = instance
        self.args = args
        self.kwargs = kwargs
        self.child_conn = None

        self.pop_kwargs()
        self.set_signals_to_false_if_not_possible()
        self.eval_if_required()
        self.format_exception_message()

    def pop_kwargs(self):
        self.dec_allow_eval = self.kwargs.pop('dec_allow_eval', self.dec_allow_eval)
        self.dec_timeout = self.kwargs.pop('dec_timeout', self.dec_timeout)
        self.use_signals = self.kwargs.pop('use_signals', self.use_signals)
        self.dec_hard_timeout = self.kwargs.pop('dec_hard_timeout', self.dec_hard_timeout)

    @property
    def should_eval(self):
        if self.dec_allow_eval and isinstance(self.dec_timeout, str):
            return True
        else:
            return False

    def format_exception_message(self):
        function_name = self.wrapped.__name__ or '(unknown name)'
        if not self.exception_message:
            self.exception_message = 'Function {function_name} timed out after {dec_timeout} seconds'
        self.exception_message = self.exception_message.format(function_name=function_name, dec_timeout=self.dec_timeout)

    def new_alarm_handler(self, signum, frame):
        raise_exception(self.timeout_exception, self.exception_message)

    def save_old_and_set_new_alarm_handler(self):
        self.old_alarm_handler = signal.signal(signal.SIGALRM, self.new_alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, self.dec_timeout)

    def restore_old_alarm_handler(self):
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, self.old_alarm_handler)

    def set_signals_to_false_if_not_possible(self):
        if is_system_windows() or not is_in_main_thread():
            self.use_signals = False

    def eval_if_required(self):
        wrapped = self.wrapped
        instance = self.instance
        args = self.args
        kwargs = self.kwargs

        if self.should_eval:
            self.dec_timeout = eval(str(self.dec_timeout))


def detect_unpickable_objects_and_reraise(object_to_pickle):
    # sometimes the detection detects unpickable objects but actually
    # they can be pickled - so we just try to start the thread and report
    # the unpickable objects if that fails
    dict_result = detect_unpickable_objects(object_to_pickle, dill_trace=False, log_warning=False)
    s_err = 'can not pickle {on}, bad items: {bi}, bad objects: {bo}, bad types {bt}'.format(on=dict_result['object_name'],
                                                                                             bi=dict_result['bad_items'],
                                                                                             bo=dict_result['bad_objects'],
                                                                                             bt=dict_result['bad_types'])
    raise dill.PicklingError(s_err)


def detect_unpickable_objects(object_to_pickle, dill_trace=True, log_warning=True):
    # type: (Any, bool, bool) -> Dict
    if log_warning:
        logger.warning('always remember that the "object_to_pickle" should not be defined within the main context')
    dict_result = dict()
    dict_result['object_name'] = ''
    dict_result['bad_items'] = list()
    dict_result['bad_objects'] = list()
    dict_result['bad_types'] = list()

    safe_status_of_dill_trace = dill.detect.trace
    # noinspection PyBroadException
    try:
        if dill_trace:
            dill.detect.trace = True
        pickled_object = dill.dumps(object_to_pickle)
        dill.loads(pickled_object)
    except Exception:
        dict_result['object_name'] = object_to_pickle.__name__ or 'object'
        dict_result['bad_objects'] = get_bad_pickling_objects(object_to_pickle)
        dict_result['bad_types'] = get_bad_pickling_types(object_to_pickle)
    finally:
        dill.detect.trace = safe_status_of_dill_trace
        return dict_result


def get_bad_pickling_types(object_to_pickle):
    bad_types = list()
    # noinspection PyBroadException
    try:
        bad_types = dill.detect.badtypes(object_to_pickle)
    except Exception:
        bad_types = [sys.exc_info()[1]]
    finally:
        return bad_types


def get_bad_pickling_objects(object_to_pickle):
    bad_objects = list()
    # noinspection PyBroadException
    try:
        bad_objects = dill.detect.badobjects(object_to_pickle)
    except Exception:
        bad_objects = [sys.exc_info()[1]]
    finally:
        return bad_objects


def raise_exception(exception, exception_message):
    """ This function checks if a exception message is given.
    If there is no exception message, the default behaviour is maintained.
    If there is an exception message, the message is passed to the exception.
    """
    if not exception:
        exception = TimeoutError
    raise exception(exception_message)


def is_in_main_thread():
    if sys.version_info < (3, 4):
        return is_in_main_thread_pre_python_3_4()
    else:
        return is_in_main_thread_from_python_3_4_up()


def is_in_main_thread_pre_python_3_4():
    # old python versions below 3.4
    if isinstance(threading.current_thread(), threading._MainThread):
        return True
    else:
        return False


def is_in_main_thread_from_python_3_4_up():
    # python versions from 3.4 up
    if threading.current_thread() == threading.main_thread():
        return True
    else:
        return False


def is_system_windows():
    if platform.system().lower().startswith('win'):
        return True
    else:
        return False
