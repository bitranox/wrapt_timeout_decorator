# -*- coding: utf-8 -*-
import logging

try:
    from .wrapt_timeout_decorator.wrapt_timeout_decorator import timeout
except ImportError:
    logger = logging.getLogger()
    logger.debug('Import Error - this __init__.py is only meant for local package development')

__title__ = 'wrapt_timeout_decorator'
__name__ = 'wrapt_timeout_decorator'
