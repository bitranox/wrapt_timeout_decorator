# STDLIB
import logging
import platform
import signal
import sys
import threading
from types import FrameType
from typing import Any, Callable, Dict, List, Type, Union, Optional

# EXT
import dill
import multiprocess
import multiprocessing

# Types
AlarmHandler = Union[Callable[[int, Optional[FrameType]], Any], int, signal.Handlers, None]

logger = logging.getLogger("pickle_analyzer")


class WrapHelper(object):
    def __init__(
        self,
        dec_timeout: Union[None, float, str],
        use_signals: bool,
        timeout_exception: Type[BaseException],
        exception_message: str,
        dec_allow_eval: bool,
        dec_hard_timeout: bool,
        dec_poll_subprocess: float,
        dec_mp_reset_signals: bool,
        wrapped: Callable[..., Any],
        instance: object,
        args: Any,
        kwargs: Any,
    ) -> None:
        self.dec_timeout = dec_timeout
        self.use_signals = use_signals
        self.timeout_exception = timeout_exception
        self.exception_message = exception_message
        self.dec_allow_eval = dec_allow_eval
        self.dec_hard_timeout = dec_hard_timeout
        self.dec_poll_subprocess = dec_poll_subprocess
        self.dec_mp_reset_signals = dec_mp_reset_signals
        self.wrapped = wrapped
        self.instance = instance
        self.args = args
        self.kwargs = kwargs

        self.dec_timeout_float: float = 0.0
        self.old_alarm_handler: AlarmHandler = None
        self.child_conn: "multiprocess.Pipe" = None

        self.pop_kwargs()
        self.set_signals_to_false_if_not_possible()
        self.eval_if_required()
        self.convert_timeout_given_to_float()
        self.format_timeout_exception_message()

    def convert_timeout_given_to_float(self) -> None:
        if self.dec_timeout is None:
            self.dec_timeout_float = 0.0
        else:
            try:
                self.dec_timeout_float = float(self.dec_timeout)
            except ValueError:
                raise ValueError(f'the given or evaluated value for the timeout can not be converted to float : "{self.dec_timeout}"')

    def pop_kwargs(self) -> None:
        """ this is to override the decorator settings with parameters given to the decorated function itself """
        self.dec_timeout = self.kwargs.pop("dec_timeout", self.dec_timeout)
        self.use_signals = self.kwargs.pop("use_signals", self.use_signals)
        self.dec_allow_eval = self.kwargs.pop("dec_allow_eval", self.dec_allow_eval)
        self.dec_hard_timeout = self.kwargs.pop("dec_hard_timeout", self.dec_hard_timeout)
        self.dec_poll_subprocess = self.kwargs.pop("dec_poll_subprocess", self.dec_poll_subprocess)
        self.dec_mp_reset_signals = self.kwargs.pop("dec_mp_reset_signals", self.dec_mp_reset_signals)

    @property
    def should_eval(self) -> bool:
        if self.dec_allow_eval and isinstance(self.dec_timeout, str):
            return True
        else:
            return False

    def format_timeout_exception_message(self) -> None:
        # todo : make time human readable lib_cast
        function_name = self.wrapped.__name__ or "(unknown name)"
        if not self.exception_message:
            self.exception_message = f"Function {function_name} timed out after {self.dec_timeout_float} seconds"

    def format_subprocess_exception_message(self, subprocess_run_time: float) -> None:
        # todo : make time human readable lib_cast
        function_name = self.wrapped.__name__ or "(unknown name)"
        self.exception_message = f"Function {function_name} was terminated or killed after {subprocess_run_time} seconds"

    def new_alarm_handler(self, signum: signal.Signals, frame: FrameType) -> None:
        raise_exception(self.timeout_exception, self.exception_message)

    def save_old_and_set_new_alarm_handler(self) -> None:
        self.old_alarm_handler = signal.signal(signal.SIGALRM, self.new_alarm_handler)  # type: ignore
        signal.setitimer(signal.ITIMER_REAL, self.dec_timeout_float)  # type: ignore  # on windows we dont have signals

    def restore_old_alarm_handler(self) -> None:
        signal.setitimer(signal.ITIMER_REAL, 0)  # type: ignore  # on windows we dont have signals
        signal.signal(signal.SIGALRM, self.old_alarm_handler)  # type: ignore  # on windows we dont have signals

    def set_signals_to_false_if_not_possible(self) -> None:
        if is_system_windows() or not is_in_main_thread():
            self.use_signals = False

    def eval_if_required(self) -> None:
        # define local variables which then can be used in eval
        wrapped = self.wrapped  # noqa
        instance = self.instance  # noqa
        args = self.args  # noqa
        kwargs = self.kwargs  # noqa

        if self.should_eval:
            self.dec_timeout = eval(str(self.dec_timeout))


def detect_unpickable_objects_and_reraise(object_to_pickle: Any) -> None:
    # sometimes the detection detects unpickable objects but actually
    # they can be pickled - so we just try to start the thread and report
    # the unpickable objects if that fails
    dict_result = detect_unpickable_objects(object_to_pickle, dill_trace=False, log_warning=False)
    s_err = (
        f"can not pickle {dict_result['object_name']}, bad items: {dict_result['bad_items']}, bad objects: {dict_result['bad_objects']}, "
        f"bad types {dict_result['bad_types']}"
    )
    raise dill.PicklingError(s_err)


def detect_unpickable_objects(object_to_pickle: Any, dill_trace: bool = True, log_warning: bool = True) -> Dict[str, Union[str, List[Any]]]:
    if log_warning:
        logger.warning('always remember that the "object_to_pickle" should not be defined within the main context')
    dict_result: Dict[str, Union[str, List[Any]]] = dict()
    dict_result["object_name"] = ""
    dict_result["bad_items"] = list()
    dict_result["bad_objects"] = list()
    dict_result["bad_types"] = list()
    safe_status_of_dill_trace = dill.detect.trace
    # noinspection PyBroadException
    try:
        if dill_trace:
            dill.detect.trace = True
        pickled_object = dill.dumps(object_to_pickle)
        dill.loads(pickled_object)
    except Exception:
        dict_result["object_name"] = get_object_name(object_to_pickle)
        dict_result["bad_objects"] = get_bad_pickling_objects(object_to_pickle)
        dict_result["bad_types"] = get_bad_pickling_types(object_to_pickle)
    finally:
        dill.detect.trace = safe_status_of_dill_trace
        return dict_result


def get_object_name(object_to_pickle: object) -> str:
    object_name = "object"
    if hasattr(object_to_pickle, "__name__"):
        if object_to_pickle.__name__:  # type: ignore
            object_name = object_to_pickle.__name__  # type: ignore
    return object_name


def get_bad_pickling_types(object_to_pickle: object) -> List[Any]:
    bad_types: List[Any] = list()
    # noinspection PyBroadException
    try:
        bad_types = dill.detect.badtypes(object_to_pickle)
    except Exception:
        bad_types = [sys.exc_info()[1]]
    finally:
        return bad_types


def get_bad_pickling_objects(object_to_pickle: Any) -> Any:
    bad_objects: List[object] = list()
    # noinspection PyBroadException
    try:
        bad_objects = dill.detect.badobjects(object_to_pickle)
    except Exception:
        bad_objects = [sys.exc_info()[1]]
    finally:
        return bad_objects


def set_subprocess_starting_method(start_method: str) -> None:
    """ Set the start Method for Subprocesses.
    since we use multiprocess, we set the starting method for multiprocess and multiprocessing to the same value.
    we did not test what would happen if we set that to different values.



    :param start_method:
        Windows Limitation: Only `spawn` is available on Windows.
        Linux/Unix Options: Options include `fork`, `forkserver`, and `spawn`.
            fork:       Efficiently clones the parent process, including memory space,
                        but may lead to issues with shared resources or in multi-threaded applications.
            forkserver: Starts a server at program launch, creating new processes upon request
                        for better isolation but at a slower pace due to the server communication requirement.
            spawn:      Initiates a fresh Python interpreter process, ensuring total independence
                        at the cost of slower start-up due to the need for full initialization.

        Choosing the Right Start Method
        -------------------------------
        - fork offers   speed but can encounter issues with resource sharing or threading.
        - forkserver    enhances stability and isolation, ideal for applications requiring safety or managing unstable resources.
        - spawn         provides the highest level of isolation, recommended for a clean start and avoiding shared state complications.

        Setting the Start Method
        ------------------------
        Configure the start method with `set_subprocess_starting_method(method)`
        This should be done cautiously, ideally once, and within the `if __name__ == '__main__'` block to prevent unintended effects.

    >>> # Setup
    >>> test_preserve_current_method = multiprocessing.get_start_method()
    >>> test_available_start_methods = multiprocessing.get_all_start_methods()

    >>> # Test OK
    >>> for test_start_method in test_available_start_methods:
    ...     set_subprocess_starting_method(test_start_method)

    >>> # Test Failed
    >>> set_subprocess_starting_method("unknown_start_method")
    Traceback (most recent call last):
        ...
    RuntimeError: Subprocess Start Method "unknown_start_method" is not supported on this OS. Permittable are : ...

    >>> # Teardown
    >>> set_subprocess_starting_method(test_preserve_current_method)

    """
    available_start_methods = multiprocessing.get_all_start_methods()
    if start_method not in available_start_methods:
        raise RuntimeError(f'Subprocess Start Method "{start_method}" is not supported on this OS. Permittable are : {", ".join(available_start_methods)}')

    multiprocessing.set_start_method(start_method, force=True)
    multiprocess.set_start_method(start_method, force=True)


def raise_exception(exception: Type[BaseException], exception_message: str) -> None:
    """This function checks if a exception message is given.
    If there is no exception message, the default behaviour is maintained.
    If there is an exception message, the message is passed to the exception.
    """
    if not exception:
        exception = TimeoutError
    raise exception(exception_message)


def is_in_main_thread() -> bool:
    if threading.current_thread() == threading.main_thread():
        return True
    else:
        return False


def is_system_windows() -> bool:
    if platform.system().lower().startswith("win"):
        return True
    else:
        return False
