"""Timeout decorator tests."""

from dill import PicklingError
from .lib_test_helper import *
import pytest
from threading import Thread
import time
from wrapt_timeout_decorator import *
from wrapt_timeout_decorator.wrapt_timeout_decorator.wrap_helper import *
from wrapt_timeout_decorator.wrapt_timeout_decorator.wrap_function_multiprocess import *
import sys


if sys.version_info < (3, 3):             # there is no TimeoutError < Python 3.3
    TimeoutError = AssertionError


@pytest.fixture(params=[False, True])
def use_signals(request):
    """Use signals for timing out or not."""
    return request.param


def test_timeout_decorator_arg(use_signals):
    @timeout(0.1, use_signals=use_signals)
    def f():
        time.sleep(0.2)
    with pytest.raises(TimeoutError):
        f()


def test_timeout_class_method(use_signals):
    with pytest.raises(TimeoutError, match=r'Function f timed out after 0\.1 seconds'):
        ClassTest1().f(use_signals=use_signals)
    if not is_python_27_under_windows():
        assert ClassTest1().f(dec_timeout='instance.x', dec_allow_eval=True, use_signals=use_signals) is None
    else:
        with pytest.raises(Exception):
            ClassTest1().f(dec_timeout='instance.x', dec_allow_eval=True, use_signals=use_signals)


def test_timeout_class_method_can_pickle(use_signals):
    my_object = ClassTest2(0.1)
    if not is_python_27_under_windows():
        with pytest.raises(TimeoutError, match=r'Function test_method timed out after 0\.1 seconds'):
            my_object.test_method(use_signals=use_signals)
        my_object = ClassTest2(1.0)
        assert my_object.test_method(use_signals=use_signals) == 'done'
    else:
        with pytest.raises(Exception):
            my_object.test_method(use_signals=use_signals)


def test_timeout_kwargs(use_signals):
    @timeout(1, use_signals=use_signals)
    def f():
        time.sleep(0.2)
    with pytest.raises(TimeoutError, match=r'Function f timed out after 0\.1 seconds'):
        f(dec_timeout=0.1)


def test_timeout_alternate_exception(use_signals):
    @timeout(0.1, use_signals=use_signals, timeout_exception=StopIteration)
    def f():
        time.sleep(0.2)
    with pytest.raises(StopIteration, match=r'Function f timed out after 0\.1 seconds'):
        f()


def test_no_timeout_given(use_signals):
    @timeout(use_signals=use_signals)
    def f():
        time.sleep(0.1)
    f()


def test_timeout_ok_timeout_as_kwarg(use_signals):
    @timeout(dec_timeout=0.2, use_signals=use_signals)
    def f_test_timeout_ok_timeout_as_kwarg():
        time.sleep(0.1)

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


def test_no_function_name(use_signals):
    @timeout(0.1, use_signals=use_signals)
    def f():
        time.sleep(1)

    with pytest.raises(TimeoutError, match=r'Function \(unknown name\) timed out after 0.1 seconds'):
        f.__name__ = ''
        f()


def test_custom_exception(use_signals):
    @timeout(0.1, use_signals=use_signals, timeout_exception=ValueError, exception_message='custom exception message')
    def f():
        time.sleep(1)
    with pytest.raises(ValueError, match='custom exception message'):
        f()


def test_not_main_thread(use_signals):
    @timeout(0.3, use_signals=use_signals)
    def f(x):
        time.sleep(x)

    # get rid of not covered because in thread
    f(0)
    # we can not check for the Exception here, it happens in the subthread
    # we would need to set up a queue to communicate.
    # but we can check if the timeout occured
    test_thread = Thread(target=f, args=(10, ))
    test_thread.name = None
    test_thread.daemon = True
    start_time = time.time()
    test_thread.start()
    test_thread.join()
    stop_time = time.time()
    # it takes quiet some time to create the thread under windows
    # especially the virtual machine on travis can be very slow.
    # we experienced a total time up to 3.9 seconds until we get the 0.3s timeout !
    assert 0.0 < (stop_time - start_time) < 5


@timeout(0.1, use_signals=use_signals)
def can_not_be_pickled(x):
    time.sleep(x)


# get rid of not covered because can not be pickled
can_not_be_pickled(0, dec_timeout=0)


def test_pickle_detection_not_implemented_error():
    match = r'can not pickle can_not_be_pickled, '
    with pytest.raises(PicklingError, match=match):
        detect_unpickable_objects_and_reraise(can_not_be_pickled)


def test_pickle_analyser():
    result = detect_unpickable_objects(can_not_be_pickled, dill_trace=True)

    assert str(result['bad_objects']) == '[NotImplementedError(\'object proxy must define __reduce_ex__()\')]' or \
                                         '[NotImplementedError(\'object proxy must define __reduce_ex__()\',)]'

    assert str(result['bad_types']) == '[NotImplementedError(\'object proxy must define __reduce_ex__()\')]' or \
                                       '[NotImplementedError(\'object proxy must define __reduce_ex__()\',)]'

    assert result['object_name'] == 'can_not_be_pickled'


def test_hard_timeout_windows_only():
    @timeout(dec_timeout=0.25, use_signals=use_signals)
    def f_test_hard_timeout():
        time.sleep(0.1)
        return 'done'
    if is_system_windows():
        with pytest.raises(TimeoutError, match=r'Function f_test_hard_timeout timed out after 0\.25 seconds'):
            f_test_hard_timeout(dec_hard_timeout=True)
        assert f_test_hard_timeout(dec_hard_timeout=False) == 'done'
