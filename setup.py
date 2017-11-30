"""Setuptools entry point."""
import codecs
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

dirname = os.path.dirname(__file__)

long_description = (
    codecs.open(os.path.join(dirname, 'README.rst'), encoding='utf-8').read() + '\n' +
    codecs.open(os.path.join(dirname, 'CHANGES.rst'), encoding='utf-8').read()
)

setup(
    name='wrapt-timeout-decorator',
    version='1.0.2',
    description='Timeout decorator',
    long_description=long_description,
    author='Robert Nowotny',
    author_email='rnowotny1966@gmail.com',
    url='https://github.com/bitranox/wrapt-timeout-decorator',
    packages=['wrapt_timeout_decorator'],
    install_requires=['dill','multiprocess','wrapt'],
    classifiers=CLASSIFIERS)
