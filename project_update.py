"""

Usage:
    project_update.py [ --get_registered_shell_command ]

this module exposes no other useful functions to the commandline

"""
# stdlib
import pathlib
import shutil
from typing import Dict, List, Union

# EXT
from docopt import docopt   # type: ignore

# OWN
import project_conf


def format_commandline_help_file() -> None:
    source_file = pathlib.Path(__file__).parent / '.docs/commandline_help.txt'
    if source_file.is_file():
        with open(source_file, 'r') as f_sourcefile:
            commandline_help_txt_lines = f_sourcefile.readlines()
        with open(source_file, 'w') as f_targetfile:
            target_lines = list()
            target_lines.append('.. code-block:: bash\n\n')
            target_lines.append('')
            for commandline_help_txt_line in commandline_help_txt_lines:
                target_lines.append('   ' + commandline_help_txt_line)
            f_targetfile.writelines(target_lines)
    else:
        with open(str(source_file), 'w') as f_targetfile:
            f_targetfile.write('.. code-block:: bash\n\n    there are no commandline options\n')


def create_commandline_help_file() -> None:
    """
    >>> create_commandline_help_file()

    """
    import subprocess
    import sys
    module_path = pathlib.Path('./{src_dir}/{module_name}.py'.format(src_dir=project_conf.src_dir, module_name=project_conf.module_name))
    if module_path.is_file():
        module_path = module_path.resolve()
        command = '{sys_executable} {module_path} -h > ./.docs/commandline_help.txt'.format(sys_executable=sys.executable, module_path=module_path)
        subprocess.run(command, shell=True)
    format_commandline_help_file()


def create_init_config_file() -> None:
    path_source_dir = get_path_template_dir_local() / 'templates'
    path_target_dir = pathlib.Path(__file__).parent.resolve() / project_conf.src_dir

    path_target_dir.mkdir(parents=True, exist_ok=True)

    # overwrite __init__conf__py from template
    path_targetfile = path_target_dir / '__init__conf__.py'
    path_sourcefile = path_source_dir / '__init__conf__.py'
    shutil.copy(str(path_sourcefile), str(path_targetfile))

    # replace the markers
    with open(path_targetfile, 'r') as f_targetfile:
        text = f_targetfile.read()
    text = text.replace('{version}', project_conf.version)
    text = text.replace('{title}', project_conf.init_config_title)
    text = text.replace('{name}', project_conf.init_config_name)
    text = text.replace('{url}', project_conf.url)
    text = text.replace('{author}', project_conf.author)
    text = text.replace('{author_email}', project_conf.author_email)
    text = text.replace('{shell_command}', project_conf.shell_command)
    with open(path_targetfile, 'w') as f_targetfile:
        f_targetfile.write(text)

    # copy __init__.py if not there from template
    path_targetfile = path_target_dir / '__init__.py'
    if not path_targetfile.is_file():
        path_sourcefile = path_source_dir / '__init__.py'
        shutil.copy(str(path_sourcefile), str(path_targetfile))

    # copy main.py if not there from template
    path_targetfile = path_target_dir / (project_conf.module_name + '.py')
    if not path_targetfile.is_file():
        path_sourcefile = path_source_dir / 'main.py'
        shutil.copy(str(path_sourcefile), str(path_targetfile))

    # copy __doc__.py if not there from template
    path_targetfile = path_target_dir / '__doc__.py'
    if not path_targetfile.is_file():
        path_sourcefile = path_source_dir / '__doc__.py'
        shutil.copy(str(path_sourcefile), str(path_targetfile))


def is_in_own_project_folder() -> bool:
    if pathlib.Path(__file__).parts[-2] == 'lib_travis_template':
        return True
    else:
        return False


def get_path_template_dir_local() -> pathlib.Path:
    path_current_dir = pathlib.Path(__file__).parent.resolve()
    while True:
        path_current_dir = path_current_dir.parent
        path_current_subdirs = path_current_dir.glob('**/')
        for subdir in path_current_subdirs:
            if subdir.parts[-1] == 'lib_travis_template':
                return subdir


def is_ok_to_copy(path_source_file: pathlib.Path) -> bool:
    """ its ok when a file and not in the list """
    files_not_to_copy = ['requirements.txt', 'project_conf.py', '.travis.yml', 'README.rst',
                         'CHANGES.rst', 'description.rst', 'usage.rst', 'installation.rst', 'acknowledgment.rst',
                         'badges_project.rst', 'badges_with_jupyter.rst', 'badges_without_jupyter.rst', '__doc__.py',
                         'index.rst', 'index_jupyter.rst', 'try_in_jupyter.rst']
    if path_source_file.is_file():
        if path_source_file.name in files_not_to_copy:
            return False
        else:
            return True
    else:
        return False


def get_paths_to_copy(path_source_dir: pathlib.Path) -> List[pathlib.Path]:
    paths_source = list(path_source_dir.glob('*'))
    paths_source = paths_source + list(path_source_dir.glob('**/.docs/*'))
    paths_source = paths_source + list(path_source_dir.glob('**/tests/*'))
    paths_source = sorted(paths_source)
    return paths_source


def copy_project_files() -> None:
    """
    copy the template files to the current project on the local development machine
    we dont overwrite some files, see code
    """
    path_source_dir = get_path_template_dir_local()
    path_target_dir = pathlib.Path(__file__).parent.resolve()
    s_path_source_dir = str(path_source_dir)
    s_path_target_dir = str(path_target_dir)

    l_path_sourcefiles = get_paths_to_copy(path_source_dir)

    for path_sourcefile in l_path_sourcefiles:
        if is_ok_to_copy(path_sourcefile):
            s_path_sourcefile = str(path_sourcefile)
            s_path_targetfile = s_path_sourcefile.replace(s_path_source_dir, s_path_target_dir, 1)
            path_targetfile = pathlib.Path(s_path_targetfile)

            if not path_targetfile.parent.is_dir():
                path_targetfile.parent.mkdir(exist_ok=True)

            shutil.copy(s_path_sourcefile, s_path_targetfile)


def copy_template_files() -> None:
    path_source_dir = get_path_template_dir_local()
    path_target_dir = pathlib.Path(__file__).parent.resolve()

    # copy CHANGES.rst template if not there
    path_targetfile = path_target_dir / 'CHANGES.rst'
    if not path_targetfile.is_file():
        path_sourcefile = path_source_dir / 'templates/CHANGES.rst'
        shutil.copy(str(path_sourcefile), str(path_targetfile))

    # copy usage.rst template if not there
    path_targetfile = path_target_dir / '.docs/usage.rst'
    if not path_targetfile.is_file():
        path_sourcefile = path_source_dir / 'templates/usage.rst'
        shutil.copy(str(path_sourcefile), str(path_targetfile))

    # copy description.rst template if not there
    path_targetfile = path_target_dir / '.docs/description.rst'
    if not path_targetfile.is_file():
        path_sourcefile = path_source_dir / 'templates/description.rst'
        shutil.copy(str(path_sourcefile), str(path_targetfile))

    # copy acknowledgment.rst template if not there
    path_targetfile = path_target_dir / '.docs/acknowledgment.rst'
    if not path_targetfile.is_file():
        path_sourcefile = path_source_dir / 'templates/acknowledgment.rst'
        shutil.copy(str(path_sourcefile), str(path_targetfile))

    # copy index.rst template if not there
    path_targetfile = path_target_dir / '.docs/index.rst'
    if not path_targetfile.is_file():
        if project_conf.badges_with_jupiter:
            path_sourcefile = path_source_dir / 'templates/index_jupyter.rst'
        else:
            path_sourcefile = path_source_dir / 'templates/index.rst'
        shutil.copy(str(path_sourcefile), str(path_targetfile))

    # copy try_in_jupyter.rst template if not there
    path_targetfile = path_target_dir / '.docs/try_in_jupyter.rst'
    if project_conf.badges_with_jupiter:
        path_sourcefile = path_source_dir / 'templates/try_in_jupyter.rst'
        shutil.copy(str(path_sourcefile), str(path_targetfile))
    else:
        path_targetfile.unlink(missing_ok=True)

    # overwrite badges template
    if project_conf.badges_with_jupiter:
        path_sourcefile = path_source_dir / '.docs/badges_with_jupyter.rst'
    else:
        path_sourcefile = path_source_dir / '.docs/badges_without_jupyter.rst'
    path_targetfile = path_target_dir / '.docs/badges_project.rst'
    shutil.copy(str(path_sourcefile), str(path_targetfile))
    # overwrite installation.rst template
    path_targetfile = path_target_dir / '.docs/installation.rst'
    path_sourcefile = path_source_dir / 'templates/installation.rst'
    shutil.copy(str(path_sourcefile), str(path_targetfile))


def replace_marker(text: str, marker: str, src_filename: str, replace_marker_with_src_file: bool = True) -> str:
    """ replace a marker in the text with the content of a file, or with '' """
    if replace_marker_with_src_file:
        path_base_dir = pathlib.Path(__file__).parent
        path_src_filename = path_base_dir / src_filename
        with open(str(path_src_filename), 'r') as f_src_filename:
            s_src = f_src_filename.read()
            text = text.replace(marker, s_src)
    else:
        text = text.replace(marker, '')
    return text


def create_travis_file() -> None:

    if not project_conf.travis_pypi_secure_code:
        travis_pypi_secure_code = '# - secure: "none"'
    else:
        travis_pypi_secure_code = '- secure: "{code}"'.format(code=project_conf.travis_pypi_secure_code)

    path_base_dir = pathlib.Path(__file__).parent
    text = '{travis_template}\n'
    text = replace_marker(text=text, marker='{travis_template}', src_filename='.travis_template.yml')
    text = replace_marker(text=text, marker='{travis_template_linux_addon}',
                          src_filename='.travis_template_linux_addon.yml', replace_marker_with_src_file=project_conf.linux_tests)
    text = replace_marker(text=text, marker='{travis_template_osx_addon}',
                          src_filename='.travis_template_osx_addon.yml', replace_marker_with_src_file=project_conf.osx_tests)
    text = replace_marker(text=text, marker='{travis_template_pypy_addon}',
                          src_filename='.travis_template_pypy_addon.yml', replace_marker_with_src_file=project_conf.pypy_tests)
    text = replace_marker(text=text, marker='{travis_template_windows_addon}',
                          src_filename='.travis_template_windows_addon.yml', replace_marker_with_src_file=project_conf.windows_tests)
    text = replace_marker(text=text, marker='{travis_template_wine_addon}',
                          src_filename='.travis_template_wine_addon.yml', replace_marker_with_src_file=project_conf.wine_tests)
    text = text.replace('{package_name}', project_conf.package_name)
    text = text.replace('{cc_test_reporter_id}', project_conf.cc_test_reporter_id)
    text = text.replace('{travis_pypi_secure_code}', travis_pypi_secure_code)
    text = text.replace('{travis_repo_slug}', project_conf.travis_repo_slug)
    text = text.replace('{github_master}', project_conf.github_master)
    target_file = path_base_dir / '.travis.yml'
    with open(target_file, 'w') as f_target_file:
        f_target_file.write(text)

    if not is_in_own_project_folder():
        (path_base_dir / '.travis_template.yml').unlink()
        (path_base_dir / '.travis_template_linux_addon.yml').unlink()
        (path_base_dir / '.travis_template_osx_addon.yml').unlink()
        (path_base_dir / '.travis_template_pypy_addon.yml').unlink()
        (path_base_dir / '.travis_template_windows_addon.yml').unlink()
        (path_base_dir / '.travis_template_wine_addon.yml').unlink()


def main(docopt_args: Dict[str, Union[bool, str]]) -> None:

    if docopt_args['--get_registered_shell_command']:
        print(project_conf.shell_command)
    else:
        create_init_config_file()

        # copy files from template folder to current project
        if not is_in_own_project_folder():  # we dont want to copy if we run this in the template project itself
            copy_project_files()
            copy_template_files()

        # create travis file
        create_travis_file()

        # create readme.rst
        create_commandline_help_file()
        import build_docs
        build_docs_args = dict()
        build_docs_args['<TRAVIS_REPO_SLUG>'] = '{}/{}'.format(project_conf.github_account, project_conf.package_name)
        build_docs.main(build_docs_args)


# entry point via commandline
def main_commandline() -> None:
    """
    >>> main_commandline()  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    docopt.DocoptExit: ...

    """
    docopt_args = docopt(__doc__)
    main(docopt_args)       # pragma: no cover


# entry point if main
if __name__ == '__main__':
    main_commandline()
