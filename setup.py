"""Setuptools entry point."""
import codecs
import os
import pathlib
from typing import List

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

package_name = 'wrapt_timeout_decorator'
required = ['dill', 'multiprocess', 'wrapt']    # type: ignore  # required for python 3.4
required_for_tests = list()                     # type: ignore  # required for python 3.4
entry_points = dict()                           # type: ignore  # required for python 3.4


# python 3.4 Version needs str type for open
def get_version(dist_directory: str) -> str:
    with open(str(pathlib.Path(__file__).parent / '{dist_directory}/version.txt'.format(dist_directory=dist_directory)), mode='r') as version_file:
        version = version_file.readline()
    return version


def is_travis_deploy() -> bool:
    if 'travis_deploy' in os.environ:
        if os.environ['travis_deploy'] == 'True':
            return True
    return False


def strip_links_from_required(l_required: List[str]) -> List[str]:
    """
    >>> required = ['lib_regexp @ git+https://github.com/bitranox/lib_regexp.git', 'test']
    >>> assert strip_links_from_required(required) == ['lib_regexp', 'test']

    """
    l_req_stripped = list()                                        # type: List[str]
    for req in l_required:
        req_stripped = req.split('@')[0].strip()
        l_req_stripped.append(req_stripped)
    return l_req_stripped


if is_travis_deploy():
    required = strip_links_from_required(required)


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

path_readme = pathlib.Path(__file__).parent / 'README.rst'
long_description = package_name
if path_readme.exists():
    # noinspection PyBroadException
    try:
        readme_content = codecs.open(str(path_readme), encoding='utf-8').read()
        long_description = readme_content
    except Exception:
        pass


setup(name=package_name,
      version=get_version(package_name),
      url='https://github.com/bitranox/{package_name}'.format(package_name=package_name),
      packages=[package_name],
      package_data={package_name: ['version.txt']},
      description=package_name,
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='Robert Nowotny',
      author_email='rnowotny1966@gmail.com',
      classifiers=CLASSIFIERS,
      entry_points=entry_points,
      # minimally needs to run tests - no project requirements here
      tests_require=['typing ; python_version < "3.5"',
                     'pathlib',
                     'mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"',
                     'pytest',
                     'pytest-pep8 ; python_version < "3.5"',
                     'pytest-codestyle ; python_version >= "3.5"',
                     'pytest-mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"'
                     ] + required_for_tests,

      # specify what a project minimally needs to run correctly
      install_requires=['typing ; python_version < "3.5"',
                        'pathlib'] + required + required_for_tests,
      # minimally needs to run the setup script, dependencies must not put here
      setup_requires=['typing ; python_version < "3.5"',
                      'pathlib',
                      'pytest-runner']
      )
