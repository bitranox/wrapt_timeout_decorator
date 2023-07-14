# STDLIB
import logging
import multiprocessing
import time

# EXT
import psutil
import pytest

logger = logging.getLogger()


# OWN
# TestPolling{{{
from wrapt_timeout_decorator import timeout


@timeout(10, use_signals=False, timeout_exception=TimeoutError, dec_poll_subprocess=1)
def slow_process() -> None:
    # should have enough time to finish
    # but instead it gets terminated, and the
    # poll the subprocess every second
    logger.error(f"Slow process started at {get_str_time()}")
    time.sleep(5)
    logger.error(f"Slow process done at {get_str_time()}")


def fake_oom_killer() -> None:
    logger.error(f"Fake OOMKiller started at {get_str_time()}")
    time.sleep(2)
    # kill sibling slow_process
    # hacky way to find it
    target = psutil.Process().parent().children(recursive=True)[-1]
    target.kill()
    logger.error(f"Killed {target.pid} at {get_str_time()}")


def start_processes() -> None:
    """
    starts the 'fake_oom_killer' and 'slow_process' process -
    and kill 'slow_process' after two seconds

    >>> start_processes()
    Traceback (most recent call last):
        ...
    multiprocessing.context.ProcessError: Function slow_process was terminated or killed after ... seconds
    """
    process_oom_killer = multiprocessing.Process(target=fake_oom_killer, args=())
    process_oom_killer.start()
    slow_process()
    process_oom_killer.join()


def get_str_time() -> str:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


if __name__ == '__main__':
    start_processes()

# TestPolling}}}
