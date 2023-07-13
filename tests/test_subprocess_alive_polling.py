# STDLIB
import logging
import multiprocessing
import time

# EXT
import psutil
import pytest

# OWN
from wrapt_timeout_decorator import timeout

logger = logging.getLogger()


@timeout(10, use_signals=False, timeout_exception=TimeoutError)
def slow_process():
    # should have enough time to finish
    # but instead it gets terminated, and the
    logger.error("Slow process started")
    time.sleep(5)
    logger.error("Slow process done")


def fake_oomkiller():
    logger.error("Fake OOMKiller started")
    time.sleep(2)
    # kill sibling slow_process
    # hacky way to find it
    target = psutil.Process().parent().children(recursive=True)[-1]
    target.kill()
    logger.error(f"Killed {target.pid}")


def test_killed_process():
    """
    >>> test_killed_process()
    """
    oomkiller = multiprocessing.Process(target=fake_oomkiller, args=())
    oomkiller.start()
    slow_process()
    oomkiller.join()


if __name__ == '__main__':
    test_killed_process()
