# -*- coding: utf-8 -*-

# this __init__.py is only meant for local package development
try:
    from .wrapt_timeout_decorator import *
# this we need for pip install --install-option test
except ImportError:
    import wrapt_timeout_decorator
