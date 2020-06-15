# single point for all configuration of the project

# stdlib
from setuptools import find_packages  # type: ignore
from typing import List, Dict

package_name = 'wrapt_timeout_decorator'  # type: str
version = '1.4.0'
# codeclimate_link_hash - get it under https://codeclimate.com/github/<user>/<project>/badges
codeclimate_link_hash = '2b2b6589f80589689c2b'  # for wrapt_timeout_decorator

# cc_test_reporter_id - get it under https://codeclimate.com/github/<user>/<project> and press "test coverage"
cc_test_reporter_id = ''    # for wrapt_timeout_decorator

# pypi_password
# to create the secret :
# cd /<repository>
# travis encrypt -r bitranox/lib_parameter pypi_password=*****
# copy and paste the encrypted password here
# replace with:
# travis_pypi_secure_code = '<code>'     # pypi secure password, without '"'
travis_pypi_secure_code = 'pWhlOU6X9EIYgQiBMluz6CMM54QXsGnxA4OoPfv+I5N+86HaP3TF0lmcAhF9NzFvEtBU3tNqeGPhTmP0UvmZlf0+vjFNbVKhkMr1HYJZ2wGjRsw/93x1SB'\
                          'XayvaUSwwvoLPn1ssVIQNMvFj5dY9VPYHn2EWfeyQxtsEStYhOLoTCBaLKm1BduRWAIj4WK6NpnKO+b1wex06fZ/qqomu0oK/+zYdAwAZelR6TWYPLmV6d'\
                          'iTHmm1Rk2HTE/rrUamNHTBSvpEB76wFq2PeDsTtZfIM0ZA493Cmvsc945M25lzoNMY6NWF4e8gwRKl5XYUPA7uCoT2aYCJcHAqY+bHHyUTOek8UkJRxs7L'\
                          'Gbw+/jLi03hfSjJ6V7JBIvGvsEH9Qzvc0OfutPRe0oAbY77DLkOOJUVnWIIrYrjKfCLtF4y+v11PqFkCF9B1pckaV4Csr5oukm1VQ8XRUeksqw2qdIaAWM'\
                          '2U+ztiPsM2TzHN3uflkjw6zGymlI+gZyu6yiDn625wniBaX3cbpsNhFs9cPNnX9QHwHgoQ4SBty4bLBqBWhUVSNMk1KE52oV1F4gAayxhgtqrWRy0AJhvK'\
                          'ybZUjOVwstg2pplvTl/NGDL+cf3n8OsId5kj5ngAgBJffSZPw9CjRaE9tNNhwj9FetsuV3/bT1yU/79IAL/6HveixU0fk='

# include package data files
# package_data = {package_name: ['some_file_to_include.txt']}
package_data = dict()       # type: Dict[str, List[str]]

author = 'Robert Nowotny'
author_email = 'rnowotny1966@gmail.com'
github_account = 'bitranox'

linux_tests = True
osx_tests = True
pypy_tests = True
windows_tests = True
wine_tests = False
badges_with_jupiter = True

# a short description of the Package - especially if You deploy on PyPi !
description = 'there are many timeout decorators out there - that one focuses on correctness when using with '\
              'Classes, methods, class methods, static methods and so on'

# #############################################################################################################################################################
# DEFAULT SETTINGS - no need to change usually, but can be adopted
# #############################################################################################################################################################

shell_command = package_name
src_dir = package_name
module_name = package_name
init_config_title = description
init_config_name = package_name

# we ned to have a function main_commandline in module module_name - see examples
entry_points = {'console_scripts': ['{shell_command} = {src_dir}.{module_name}:main_commandline'
                .format(shell_command=shell_command, src_dir=src_dir, module_name=module_name)]}  # type: Dict[str, List[str]]

long_description = package_name  # will be overwritten with the content of README.rst if exists

packages = [package_name]

url = 'https://github.com/{github_account}/{package_name}'.format(github_account=github_account, package_name=package_name)
github_master = 'git+https://github.com/{github_account}/{package_name}.git'.format(github_account=github_account, package_name=package_name)
travis_repo_slug = github_account + '/' + package_name

CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Topic :: Software Development :: Libraries :: Python Modules']
