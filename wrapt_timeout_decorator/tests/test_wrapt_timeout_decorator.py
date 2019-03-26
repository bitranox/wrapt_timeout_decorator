"""Timeout decorator tests."""
from wrapt_timeout_decorator import *
import pytest
import sys
import time
from dill import PicklingError
from .lib_test_helper import *

if sys.version_info < (3, 3):             # there is no TimeoutError < Python 3.3
    TimeoutError = AssertionError


@pytest.fixture(params=[False, True])
def use_signals(request):
    """Use signals for timing out or not."""
    return request.param


def test_timeout_decorator_arg(use_signals):
    @timeout(1, use_signals=use_signals)
    def f():
        time.sleep(2)
    with pytest.raises(TimeoutError):
        f()


def test_timeout_class_method_use_signals():
    with pytest.raises(TimeoutError):
        ClassTest1().f()


def test_timeout_class_method_dont_use_signals_can_pickle1():
    with pytest.raises(TimeoutError):
        ClassTest2().f()


def test_timeout_class_method_dont_use_signals_can_pickle2():
    with pytest.raises(TimeoutError):
        ClassTest3().f()
    my_object = ClassTest3()
    assert my_object.f(dec_timeout=3, dec_allow_eval=False) == 'done'


def test_timeout_class_method_dont_use_signals_can_pickle3():
    my_object = ClassTest4(1)
    with pytest.raises(TimeoutError):
        my_object.test_method()
    my_object = ClassTest4(3)
    assert my_object.test_method() == 'done'


def test_timeout_kwargs(use_signals):
    @timeout(3, use_signals=use_signals)
    def f():
        time.sleep(2)
    with pytest.raises(TimeoutError):
        f(dec_timeout=1)


def test_timeout_alternate_exception(use_signals):
    @timeout(3, use_signals=use_signals, timeout_exception=StopIteration)
    def f():
        time.sleep(2)
    with pytest.raises(StopIteration):
        f(dec_timeout=1)


def test_timeout_no_seconds(use_signals):
    @timeout(use_signals=use_signals)
    def f():
        time.sleep(0.1)
    f()


def test_timeout_partial_seconds(use_signals):
    @timeout(0.2, use_signals=use_signals)
    def f():
        time.sleep(0.5)

    with pytest.raises(TimeoutError):
        f()


def test_timeout_ok_timeout_as_kwarg(use_signals):
    @timeout(dec_timeout=2, use_signals=use_signals)
    def f_test_timeout_ok_timeout_as_kwarg():
        time.sleep(0.5)

    f_test_timeout_ok_timeout_as_kwarg()


def test_timeout_ok_timeout_as_arg(use_signals):
    @timeout(2, use_signals=use_signals)
    def f():
        time.sleep(0.5)
    f()


def test_function_name(use_signals):
    @timeout(dec_timeout=2, use_signals=use_signals)
    def func_name():
        pass

    func_name()
    assert func_name.__name__ == 'func_name'


def test_timeout_pickle_error():
    """Test that when a pickle error occurs a pickling error is raised"""
    # codecov start ignore
    @timeout(dec_timeout=1, use_signals=False)
    def f():
        time.sleep(0.1)

        class Test(object):
            pass
        return Test()
    # codecov end ignore
    with pytest.raises(PicklingError):
        f()


def test_timeout_custom_exception_message():
    @timeout(dec_timeout=1, exception_message="Custom fail message")
    def f():
        time.sleep(2)
    with pytest.raises(TimeoutError, match="Custom fail message"):
        f()


def test_timeout_default_exception_message():
    @timeout(dec_timeout=1)
    def f():
        time.sleep(2)
    with pytest.raises(TimeoutError, match="Function f timed out after 1 seconds"):
        f()


def test_timeout_eval(use_signals):
    """ Test Eval """
    @timeout(dec_timeout='args[0] * 2', use_signals=use_signals, dec_allow_eval=True)
    def f(x):
        time.sleep(0.4)

    assert f(0.6) is None
    with pytest.raises(TimeoutError):
        f(0.1)


def test_exception(use_signals):
    """ Test Exception """
    @timeout(1.0, use_signals=use_signals)
    def f():
        raise AssertionError('test')

    with pytest.raises(AssertionError, match='test'):
        f()
