""" Build the README.rst either locally, or on Github for tagged commits.

Usage:
    build_docs.py <TRAVIS_REPO_SLUG>
    build_docs.py (-h | --help)

The TRAVIS_REPO_SLUG has following Format : "github_username/github_repository"

Options:
    -h --help   Show this screen
"""


# STDLIB
import datetime
import errno
import logging
import pathlib
import sys
from typing import Dict

# ext
from docopt import docopt       # type: ignore

# OWN
import lib_log_utils            # type: ignore
import rst_include              # type: ignore

# PROJ
import project_conf


def project_specific(repository_slug: str, repository: str, repository_dashed: str) -> None:
    # PROJECT SPECIFIC
    logger = logging.getLogger('project_specific')
    pass


def main(args: Dict[str, str]) -> None:
    logger = logging.getLogger('build_docs')
    logger.info('create the README.rst')
    travis_repo_slug = args['<TRAVIS_REPO_SLUG>']
    repository = travis_repo_slug.split('/')[1]
    repository_dashed = repository.replace('_', '-')

    project_specific(travis_repo_slug, repository, repository_dashed)

    """
    paths absolute, or relative to the location of the config file
    the notation for relative files is like on windows or linux - not like in python.
    so You might use ../../some/directory/some_document.rst to go two levels back.
    avoid absolute paths since You never know where the program will run.
    """

    if project_conf.badges_with_jupiter:
        rst_include.rst_str_replace(source='./.docs/README_template.rst', target='', str_pattern='{try_in_jupyter}',
                                    str_replace='.. include:: ./try_in_jupyter.rst', inplace=True)
    else:
        rst_include.rst_str_replace(source='./.docs/README_template.rst', target='', str_pattern='{try_in_jupyter}', str_replace='', inplace=True)

    logger.info('include the include blocks')
    rst_include.rst_inc(source='./.docs/README_template.rst',
                        target='./README.rst')

    logger.info('replace repository related strings')
    rst_include.rst_str_replace(source='./README.rst', target='', str_pattern='{repository_slug}', str_replace=travis_repo_slug, inplace=True)
    rst_include.rst_str_replace(source='./README.rst', target='', str_pattern='{repository}', str_replace=repository, inplace=True)
    rst_include.rst_str_replace(source='./README.rst', target='', str_pattern='{double_underline_repository}', str_replace='=' * len(repository), inplace=True)
    rst_include.rst_str_replace(source='./README.rst', target='', str_pattern='{repository_dashed}', str_replace=repository_dashed, inplace=True)
    rst_include.rst_str_replace(source='./README.rst', target='', str_pattern='{last_update_yyyy}', str_replace=str(datetime.date.today().year + 1), inplace=True)
    rst_include.rst_str_replace(source='./README.rst', target='', str_pattern='{codeclimate_link_hash}', str_replace=project_conf.codeclimate_link_hash, inplace=True)

    logger.info('done')
    sys.exit(0)


if __name__ == '__main__':

    if sys.version_info < (3, 6):
        lib_log_utils.log_error('only Python Versions from 3.6 are supported')
        sys.exit(1)

    lib_log_utils.log_handlers.add_stream_handler()          # type: ignore      # in order to pass mypy in the lib_log_utils package
    main_logger = logging.getLogger('main')
    try:
        _args = docopt(__doc__)
        main(_args)
    except FileNotFoundError:
        # see https://www.thegeekstuff.com/2010/10/linux-error-codes for error codes
        sys.exit(errno.ENOENT)      # No such file or directory
    except FileExistsError:
        sys.exit(errno.EEXIST)      # File exists
    except TypeError:
        sys.exit(errno.EINVAL)      # Invalid Argument
    except ValueError:
        sys.exit(errno.EINVAL)      # Invalid Argument
