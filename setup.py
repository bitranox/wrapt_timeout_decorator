"""Setuptools entry point."""
import codecs
import pathlib
from typing import Dict, List

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

package_name = 'wrapt_timeout_decorator'
required: List = list()
required_for_tests: List = list()
entry_points: Dict = dict()


def get_version(dist_directory: str) -> str:
    with open(pathlib.Path(__file__).parent / '{dist_directory}/version.txt'.format(dist_directory=dist_directory), mode='r') as version_file:
        version = version_file.readline()
    return version


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
      description=package_name,
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='Robert Nowotny',
      author_email='rnowotny1966@gmail.com',
      classifiers=CLASSIFIERS,
      entry_points=entry_points,
      # minimally needs to run tests - no project requirements here
      tests_require=['typing',
                     'pathlib',
                     'mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"',
                     'pytest',
                     'pytest-pep8 ; python_version < "3.5"',
                     'pytest-codestyle ; python_version >= "3.5"',
                     'pytest-mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"'
                     ] + required_for_tests,

      # specify what a project minimally needs to run correctly
      install_requires=['typing', 'pathlib'] + required + required_for_tests,
      # minimally needs to run the setup script, dependencies needs also to put here for setup.py install test
      setup_requires=['typing',
                      'pathlib',
                      'pytest-runner'] + required
      )
