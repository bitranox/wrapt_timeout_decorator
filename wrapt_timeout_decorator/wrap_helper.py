# STDLIB
import logging
import platform
import signal
import sys
import threading
from types import FrameType
from typing import Any, Callable, Dict, List, Type, Union, Optional

# EXT
import dill  # type: ignore
import multiprocess  # type: ignore

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
        self.wrapped = wrapped
        self.instance = instance
        self.args = args
        self.kwargs = kwargs

        self.dec_timeout_float = 0.0  # type: float
        self.old_alarm_handler: AlarmHandler = None
        self.child_conn: "multiprocess.Pipe" = None

        self.pop_kwargs()
        self.set_signals_to_false_if_not_possible()
        self.eval_if_required()
        self.convert_timeout_given_to_float()
        self.format_exception_message()

    def convert_timeout_given_to_float(self) -> None:
        if self.dec_timeout is None:
            self.dec_timeout_float = 0.0
        else:
            try:
                self.dec_timeout_float = float(self.dec_timeout)
            except ValueError:
                raise ValueError(f'the given or evaluated value for the timeout can not be converted to float : "{self.dec_timeout}"')

    def pop_kwargs(self) -> None:
        self.dec_allow_eval = self.kwargs.pop("dec_allow_eval", self.dec_allow_eval)
        self.dec_timeout = self.kwargs.pop("dec_timeout", self.dec_timeout)
        self.use_signals = self.kwargs.pop("use_signals", self.use_signals)
        self.dec_hard_timeout = self.kwargs.pop("dec_hard_timeout", self.dec_hard_timeout)

    @property
    def should_eval(self) -> bool:
        if self.dec_allow_eval and isinstance(self.dec_timeout, str):
            return True
        else:
            return False

    def format_exception_message(self) -> None:
        function_name = self.wrapped.__name__ or "(unknown name)"
        if not self.exception_message:
            self.exception_message = f"Function {function_name} timed out after {self.dec_timeout_float} seconds"

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
    dict_result = dict()  # type: Dict[str, Union[str, List[Any]]]
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
    bad_types = list()  # type: List[Any]
    # noinspection PyBroadException
    try:
        bad_types = dill.detect.badtypes(object_to_pickle)
    except Exception:
        bad_types = [sys.exc_info()[1]]
    finally:
        return bad_types


def get_bad_pickling_objects(object_to_pickle: Any) -> Any:
    bad_objects = list()  # type: List[object]
    # noinspection PyBroadException
    try:
        bad_objects = dill.detect.badobjects(object_to_pickle)
    except Exception:
        bad_objects = [sys.exc_info()[1]]
    finally:
        return bad_objects


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
