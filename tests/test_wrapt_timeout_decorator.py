"""Timeout decorator tests."""
# STDLIB
import sys
from threading import Thread
import time
from typing import Any

# EXT
from dill import PicklingError  # type: ignore
import pytest  # type: ignore

# OWN
from wrapt_timeout_decorator import *
from wrapt_timeout_decorator.wrap_helper import *
from lib_test_helper import *


@pytest.fixture(params=[False, True])  # type: ignore
def use_signals(request: Any) -> Any:
    """Use signals for timing out or not."""
    return request.param


def test_timeout_decorator_arg(use_signals: bool) -> None:
    @timeout(0.1, use_signals=use_signals)  # type: ignore
    def f() -> None:
        time.sleep(0.2)

    with pytest.raises(TimeoutError):
        f()


def test_timeout_class_method(use_signals: bool) -> None:
    with pytest.raises(TimeoutError, match=r"Function f timed out after 0\.1 seconds"):
        ClassTest1().f(use_signals=use_signals)
    assert ClassTest1().f(dec_timeout="instance.x", dec_allow_eval=True, use_signals=use_signals) is None


def test_timeout_class_method_can_pickle(use_signals: bool) -> None:
    my_object = ClassTest2(0.1)
    with pytest.raises(TimeoutError, match=r"Function test_method timed out after 0\.1 seconds"):
        my_object.test_method(use_signals=use_signals)
    my_object = ClassTest2(1.0)
    assert my_object.test_method(use_signals=use_signals) == "done"


def test_timeout_kwargs(use_signals: bool) -> None:
    @timeout(1, use_signals=use_signals)  # type: ignore
    def f() -> None:
        time.sleep(0.2)

    with pytest.raises(TimeoutError, match=r"Function f timed out after 0\.1 seconds"):
        f(dec_timeout=0.1)


def test_timeout_alternate_exception(use_signals: bool) -> None:
    @timeout(0.1, use_signals=use_signals, timeout_exception=StopIteration)  # type: ignore
    def f() -> None:
        time.sleep(0.2)

    with pytest.raises(StopIteration, match=r"Function f timed out after 0\.1 seconds"):
        f()


def test_no_timeout_given(use_signals: bool) -> None:
    @timeout(use_signals=use_signals)  # type: ignore
    def f() -> None:
        time.sleep(0.1)

    f()


def test_timeout_ok_timeout_as_kwarg(use_signals: bool) -> None:
    @timeout(dec_timeout=0.2, use_signals=use_signals)  # type: ignore
    def f_test_timeout_ok_timeout_as_kwarg() -> None:
        time.sleep(0.1)

    f_test_timeout_ok_timeout_as_kwarg()


def test_timeout_ok_timeout_as_arg(use_signals: bool) -> None:
    @timeout(2, use_signals=use_signals)  # type: ignore
    def f() -> None:
        time.sleep(0.5)

    f()


def test_function_name(use_signals: bool) -> None:
    @timeout(dec_timeout=2, use_signals=use_signals)  # type: ignore
    def func_name() -> None:
        pass

    func_name()
    assert func_name.__name__ == "func_name"


def test_timeout_pickle_error() -> None:
    """Test that when a pickle error occurs a pickling error is raised"""
    # codecov start ignore
    @timeout(dec_timeout=1, use_signals=False)  # type: ignore
    def f() -> object:
        time.sleep(0.1)

        class Test(object):
            pass

        return Test()

    # codecov end ignore
    with pytest.raises(PicklingError):
        f()


def test_timeout_custom_exception_message() -> None:
    @timeout(dec_timeout=1, exception_message="Custom fail message")  # type: ignore
    def f() -> None:
        time.sleep(2)

    with pytest.raises(TimeoutError, match="Custom fail message"):
        f()


def test_timeout_default_exception_message() -> None:
    @timeout(dec_timeout=1)  # type: ignore
    def f() -> None:
        time.sleep(2)

    with pytest.raises(TimeoutError, match=r"Function f timed out after 1.0 seconds"):
        f()


def test_timeout_eval(use_signals: bool) -> None:
    """Test Eval"""

    @timeout(dec_timeout="args[0] * 2", use_signals=use_signals, dec_allow_eval=True)  # type: ignore
    def f(x: float) -> None:
        time.sleep(0.4)

    assert f(0.6) is None
    with pytest.raises(TimeoutError):
        f(0.1)


def test_exception(use_signals: bool) -> None:
    """Test Exception"""

    @timeout(1.0, use_signals=use_signals)  # type: ignore
    def f() -> None:
        raise AssertionError("test")

    with pytest.raises(AssertionError, match="test"):
        f()


def test_no_function_name(use_signals: bool) -> None:
    @timeout(0.1, use_signals=use_signals)  # type: ignore
    def f() -> None:
        time.sleep(1)

    with pytest.raises(TimeoutError, match=r"Function \(unknown name\) timed out after 0.1 seconds"):
        f.__name__ = ""
        f()


def test_custom_exception(use_signals: bool) -> None:
    @timeout(0.1, use_signals=use_signals, timeout_exception=ValueError, exception_message="custom exception message")  # type: ignore
    def f() -> None:
        time.sleep(1)

    with pytest.raises(ValueError, match="custom exception message"):
        f()


def test_not_main_thread(use_signals: bool) -> None:
    @timeout(0.3, use_signals=use_signals)  # type: ignore
    def f(x: float) -> None:
        time.sleep(x)

    # get rid of not covered because in thread
    f(0)
    # we can not check for the Exception here, it happens in the subthread
    # we would need to set up a queue to communicate.
    # but we can check if the timeout occured
    test_thread = Thread(target=f, args=(10,))
    test_thread.name = ""
    test_thread.daemon = True
    start_time = time.time()
    test_thread.start()
    test_thread.join()
    stop_time = time.time()
    # it takes quiet some time to create the thread under windows
    # especially the virtual machine on travis can be very slow.
    # we experienced a total time up to 5.5 seconds until we get the 0.3s timeout !
    assert 0.0 < (stop_time - start_time) < 9


@timeout(0.1, use_signals=use_signals)  # type: ignore
def can_not_be_pickled(x: float) -> None:
    time.sleep(x)


# get rid of not covered because can not be pickled
can_not_be_pickled(0, dec_timeout=0)


def test_pickle_detection_not_implemented_error() -> None:
    match = r"can not pickle can_not_be_pickled, "
    with pytest.raises(PicklingError, match=match):
        detect_unpickable_objects_and_reraise(can_not_be_pickled)  # type: ignore


def test_pickle_analyser() -> None:
    result = detect_unpickable_objects(can_not_be_pickled, dill_trace=True)  # type: ignore

    assert (
        str(result["bad_objects"]) == "[NotImplementedError('object proxy must define __reduce_ex__()')]"
        or "[NotImplementedError('object proxy must define __reduce_ex__()',)]"
    )

    assert (
        str(result["bad_types"]) == "[NotImplementedError('object proxy must define __reduce_ex__()')]"
        or "[NotImplementedError('object proxy must define __reduce_ex__()',)]"
    )

    assert result["object_name"] == "can_not_be_pickled"


def test_hard_timeout_windows_only() -> None:
    @timeout(dec_timeout=0.25, use_signals=use_signals)  # type: ignore
    def f_test_hard_timeout() -> str:
        time.sleep(0.1)
        return "done"

    if is_system_windows():  # type: ignore
        # test hard timeout - timeout
        with pytest.raises(TimeoutError, match=r"Function f_test_hard_timeout timed out after 0\.25 seconds"):
            f_test_hard_timeout(dec_hard_timeout=True)
        # test hard timeout - passed
        assert f_test_hard_timeout(dec_timeout=10, dec_hard_timeout=True) == "done"
        # test without hard timeout
        assert f_test_hard_timeout(dec_hard_timeout=False) == "done"


@timeout(dec_timeout=1, use_signals=use_signals)  # type: ignore
def outer() -> None:
    inner()


@timeout(dec_timeout=2, use_signals=False)  # type: ignore
def inner() -> str:
    time.sleep(3)
    return "done"


def test_nested_decorator() -> None:
    """
    >>> test_nested_decorator()
    """

    with pytest.raises(TimeoutError, match=r"Function outer timed out after 1.0 seconds"):
        outer()


def test_dec_timeout_is_none() -> None:
    @timeout(dec_timeout=None, use_signals=use_signals)  # type: ignore
    def f() -> None:
        time.sleep(0.1)

    f()


def test_dec_timeout_is_invalid() -> None:
    @timeout(dec_timeout="invalid", use_signals=use_signals)  # type: ignore
    def f() -> None:
        time.sleep(0.1)  # pragma: no cover

    with pytest.raises(ValueError, match=r'the given or evaluated value for the timeout can not be converted to float : "invalid"'):
        f()


def test_exception_is_none() -> None:
    @timeout(dec_timeout=0.1, use_signals=use_signals, timeout_exception=None)  # type: ignore
    def f() -> None:
        time.sleep(3)

    with pytest.raises(TimeoutError, match=r"Function f timed out after 0.1 seconds"):
        f()


def test_get_object_name() -> None:
    my_object = ClassTest1()
    assert get_object_name(my_object) == "object"  # type: ignore
    my_object.__name__ = "test"  # type: ignore
    assert get_object_name(my_object) == "test"  # type: ignore
    my_object.__name__ = ""  # type: ignore
    assert get_object_name(my_object) == "object"  # type: ignore
