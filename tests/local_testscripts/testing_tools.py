# stdlib
import logging
import os
import pathlib

# EXT
import click

# CONSTANTS
CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
logger = logging.getLogger()
logger.level = logging.INFO


def append_subdirs_to_mypy_paths(root_directory: str) -> str:
    """
    Appends all immediate sudirs of the root_directory to the MYPYPATH , separated by column ':' TODO: Windows ?
    in order to be able to use that in a shellscript (because the ENV of the subshell gets lost)
    we also return it as a string. This is already in preparation to remove the testloop shellscript
    with a python script.

    >>> # Setup
    >>> save_mypy_path = get_env_data(env_variable='MYPYPATH')

    >>> # Test
    >>> append_subdirs_to_mypy_paths(str(pathlib.Path(__file__).parent.parent.resolve()))
    '...'
    >>> assert str(pathlib.Path(__file__).parent.resolve()) in get_env_data(env_variable='MYPYPATH')
    >>> append_subdirs_to_mypy_paths('non_existing')
    ''

    >>> # Teardown
    >>> set_env_data(env_variable='MYPYPATH', env_str=save_mypy_path)

    """
    path_root_directory = pathlib.Path(root_directory).resolve()
    if not path_root_directory.is_dir():
        logger.warning(f'add mypy paths : the given root directory "{path_root_directory}" does not exist')
        return ''
    l_subdirs = [str(path_root_directory / _dir) for _dir in next(os.walk(path_root_directory))[1]]
    str_current_mypy_paths = get_env_data(env_variable='MYPYPATH')
    if str_current_mypy_paths:
        l_subdirs.insert(0, str_current_mypy_paths)
    str_new_mypy_paths = ':'.join(l_subdirs)
    set_env_data(env_variable='MYPYPATH', env_str=str_new_mypy_paths)
    return str_new_mypy_paths


def append_directory_to_env_path_variable(env_variable: str, directory: str) -> str:
    """
    Appends a directory to the env_variable, separated by column ':' TODO: Windows ?
    in order to be able to use that in a shellscript (because the ENV of the subshell gets lost)
    we also return it as a string. This is already in preparation to remove the testloop shellscript
    with a python script.

    >>> # Setup
    >>> save_mypy_path = get_env_data(env_variable='MYPYPATH')

    >>> # Test
    >>> append_directory_to_env_path_variable(env_variable='MYPYPATH', directory=str(pathlib.Path(__file__).parent.parent.resolve()))
    '...tests'
    >>> assert str(pathlib.Path(__file__).parent.parent.resolve()) in get_env_data(env_variable='MYPYPATH')
    >>> append_directory_to_env_path_variable(env_variable='MYPYPATH', directory='non_existing')
    ''

    >>> # Teardown
    >>> set_env_data(env_variable='MYPYPATH', env_str=save_mypy_path)

    """
    path_directory = pathlib.Path(directory).resolve()
    if not path_directory.is_dir():
        logger.warning('can not add to env "{}" : the given directory "{}" does not exist'.format(env_variable, directory))
        return ''
    l_subdirs = [str(path_directory)]
    str_current_paths = get_env_data(env_variable=env_variable)
    if str_current_paths:
        l_subdirs.insert(0, str_current_paths)
    str_new_mypy_paths = ':'.join(l_subdirs)
    set_env_data(env_variable=env_variable, env_str=str_new_mypy_paths)
    return str_new_mypy_paths


def get_env_data(env_variable: str) -> str:
    """
    >>> # Setup
    >>> save_mypy_path = get_env_data('MYPYPATH')

    >>> # Test
    >>> set_env_data('MYPYPATH', 'some_test')
    >>> assert get_env_data('MYPYPATH') == 'some_test'

    >>> # Teardown
    >>> set_env_data('MYPYPATH', save_mypy_path)

    """
    if env_variable in os.environ:
        env_data = os.environ[env_variable]
    else:
        env_data = ''
    return env_data


def set_env_data(env_variable: str, env_str: str) -> None:
    os.environ[env_variable] = env_str


@click.group(context_settings=CLICK_CONTEXT_SETTINGS)
def cli_main() -> None:                     # pragma: no cover
    """ testing tools """
    pass                                    # pragma: no cover


@cli_main.command('append_immediate_subdirs_to_mypy_path', context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument('root_directory', type=click.Path(exists=False, file_okay=False, dir_okay=True))
def cli_append_immediate_subdirs_to_mypy_path(root_directory: str) -> None:                        # pragma: no cover
    """ adds all immediate subdirs to MYPYPATH, and returns the result as string """
    response = append_subdirs_to_mypy_paths(root_directory)                                        # pragma: no cover
    print(response)


@cli_main.command('append_directory_to_mypy_path', context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument('directory', type=click.Path(exists=False, file_okay=False, dir_okay=True))
def cli_append_directory_to_mypy_path(directory: str) -> None:                                      # pragma: no cover
    """ adds directory to MYPYPATH, and returns the result as string """
    response = append_directory_to_env_path_variable(env_variable='MYPYPATH', directory=directory)  # pragma: no cover
    print(response)


@cli_main.command('append_directory_to_python_path', context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument('directory', type=click.Path(exists=False, file_okay=False, dir_okay=True))
def cli_append_directory_to_python_path(directory: str) -> None:                                     # pragma: no cover
    """ adds directory to PYTHONPATH, and returns the result as string """
    response = append_directory_to_env_path_variable(env_variable='PYTHONPATH', directory=directory)         # pragma: no cover
    print(response)


# entry point if main
if __name__ == '__main__':
    cli_main()
