import pathlib
from .wrapt_timeout_decorator import timeout
from .wrap_helper import detect_unpickable_objects


def get_version() -> str:
    with open(pathlib.Path(__file__).parent / 'version.txt', mode='r') as version_file:
        version = version_file.readline()
    return version


__version__ = get_version()
__title__ = 'wrapt_timeout_decorator'
__name__ = 'wrapt_timeout_decorator'
