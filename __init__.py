# -*- coding: utf-8 -*-

# this is only for local development when the package is actually not installed
# noinspection PyBroadException
try:
    from .wrapt_timeout_decorator.wrapt_timeout_decorator import timeout
except ImportError:
    pass

__title__ = 'wrapt_timeout_decorator'
__version__ = '1.0.9'
