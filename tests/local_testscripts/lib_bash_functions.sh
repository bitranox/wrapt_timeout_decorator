#!/bin/bash
save_dir="$PWD"
own_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit && pwd -P)" # this gives the full path, even for sourced scripts

# shellcheck disable=SC2050
if [[ "True" != "True" ]]; then
    echo "exit - ${BASH_SOURCE[0]} is not configured by PizzaCutter"
    exit 0
fi

sleeptime_on_error=5
sudo_askpass="$(command -v ssh-askpass)"
export SUDO_ASKPASS="${sudo_askpass}"
export NO_AT_BRIDGE=1                        # get rid of (ssh-askpass:25930): dbind-WARNING **: 18:46:12.019: Couldn't register with accessibility bus: Did not receive a reply.

tests_dir="$(dirname "${own_dir}")"          # one level up
project_root_dir="$(dirname "${tests_dir}")" # one level up

cd "$own_dir"||exit
# shellcheck disable=SC2155
export PYTHONPATH="$(python3 ./testing_tools.py append_directory_to_python_path "${project_root_dir}")"
# following lines are not only a comment, they get actually replaced
export PYTHONPATH="$(python3 ./testing_tools.py append_directory_to_python_path "/media/srv-main-softdev/rotek-apps/lib")"
export MYPYPATH="$(python3 ./testing_tools.py append_immediate_subdirs_to_mypy_path "/media/srv-main-softdev/rotek-apps/lib/bitranox")"
export MYPYPATH="$(python3 ./testing_tools.py append_immediate_subdirs_to_mypy_path "/media/srv-main-softdev/rotek-apps/lib/libs_local")"
cd "$save_dir"||exit

function install_or_update_lib_bash() {
  if [[ ! -f /usr/local/lib_bash/install_or_update.sh ]]; then
    sudo git clone https://github.com/bitranox/lib_bash.git /usr/local/lib_bash 2>/dev/null
    sudo chmod -R 0755 /usr/local/lib_bash 2>/dev/null
    sudo chmod -R +x /usr/local/lib_bash/*.sh 2>/dev/null
    sudo /usr/local/lib_bash/install_or_update.sh 2>/dev/null
  else
    /usr/local/lib_bash/install_or_update.sh
  fi
}

install_or_update_lib_bash

source /usr/local/lib_bash/lib_helpers.sh

function my_banner() {
  banner "${project_root_dir}: ${1}"
}

function my_banner_warning() {
  banner_warning "${project_root_dir}: ${1}"
}

function clean_caches() {
  # mypy and pytest caches should be deleted, because sometimes problems on collecting if not
  clr_green "clean caches and distribution directories in ${project_root_dir}"
  sudo find "${project_root_dir}" -name ".eggs" -type d -exec rm -rf {} \; 2>/dev/null
  sudo find "${project_root_dir}" -name ".mypy_cache" -type d -exec rm -rf {} \; 2>/dev/null
  sudo find "${project_root_dir}" -name ".pytest_cache" -type d -exec rm -rf {} \; 2>/dev/null
  sudo find "${project_root_dir}" -name "build" -type d -exec rm -rf {} \; 2>/dev/null
  sudo find "${project_root_dir}" -name "dist" -type d -exec rm -rf {} \; 2>/dev/null
  sudo find "${project_root_dir}" -name "*.egg-info" -type d -exec rm -rf {} \; 2>/dev/null
  sudo find "${project_root_dir}" -name "__pycache__" -type d -exec rm -rf {} \; 2>/dev/null
  sudo rm -rf "$HOME/.eggs/*"
  sudo rm -rf "$HOME/.mypy_cache"
}

function install_virtualenv_debian() {
  if ! is_package_installed python3-virtualenv; then
    banner "python3-virtualenv is not installed, I will install it for You"
    wait_for_enter
    install_package_if_not_present python3-virtualenv
  fi
}

function install_test_requirements() {
  # this should be already installed, but it happens that pycharm ide venv does not have it
  clr_green "installing/updating pip, setuptools, wheel"
  sudo chmod -R 0777 ~/.eggs # make already installed eggs accessible, just in case they were installed as root

  python3 -m pip install --upgrade pip
  python3 -m pip install --upgrade setuptools
  python3 -m pip install --upgrade wheel
  # this we need for local testscripts
  python3 -m pip install --upgrade click

  if test -f "${project_root_dir}/requirements_test.txt"; then
    clr_green "installing/updating test requirements from \"requirements_test.txt\""
    python3 -m pip install --upgrade -r "${project_root_dir}/requirements_test.txt"
  else
    clr_red "requirements_test.txt not found"
  fi
}

function install_dependencies() {
  banner "installing dependencies"
  install_virtualenv_debian
  install_test_requirements
}

function delete_virtual_environment() {
  sudo rm -rf ~/venv
}

function install_clean_virtual_environment() {
  clr_green "installing venv"
  delete_virtual_environment
  virtualenv ~/venv
}


function cleanup() {
  trap '' 2 # disable Ctrl+C
  delete_virtual_environment
  clean_caches
  cd "${save_dir}" || exit
  trap 2 # enable Ctrl+C
}


function run_black() {
  # run black for *.py files
  my_banner "running black with settings from ${project_root_dir}/pyproject.toml"
  if ! python3 -m black "${project_root_dir}"/**/*.py; then
    my_banner_warning "black ERROR"
    beep
    sleep "${sleeptime_on_error}"
    return 1
  fi
}


function run_flake8_tests() {
  # run flake8, settings from setup.cfg
  my_banner "running flake8 with settings from ${project_root_dir}/setup.cfg"
  if ! python3 -m flake8 --append-config="${project_root_dir}/setup.cfg" "$@" "${project_root_dir}"; then
    my_banner_warning "flake8 ERROR"
    beep
    sleep "${sleeptime_on_error}"
    return 1
  fi
}


function run_mypy_tests() {
  my_banner "mypy tests"
  if ! python3 -m mypy "${project_root_dir}" --follow-imports=normal --ignore-missing-imports --implicit-reexport --install-types --no-warn-unused-ignores --non-interactive --strict; then
    my_banner_warning "mypy tests ERROR"
    beep
    sleep "${sleeptime_on_error}"
    return 1
  fi
}


function run_pytest() {
  # run pytest, accepts additional pytest parameters like --disable-warnings and so on
  my_banner "running pytest with settings from pytest.ini, mypy.ini and conftest.py"
  if ! python3 -m pytest "${project_root_dir}" "$@" --cov="${project_root_dir}" --cov-config=.coveragerc; then
    my_banner_warning "pytest ERROR"
    beep
    sleep "${sleeptime_on_error}"
    return 1
  fi
}


function install_pip_requirements_venv() {
  if test -f "${project_root_dir}/requirements.txt on virtual environment"; then
    my_banner "pip install -r requirements.txt"
    install_clean_virtual_environment
    if ! ~/venv/bin/python3 -m pip install -r "${project_root_dir}/requirements.txt"; then
      my_banner_warning "pip install -r requirements.txt ERROR"
      beep
      sleep "${sleeptime_on_error}"
      return 1
    fi
  fi
}


function setup_install_venv() {
  if test -f "${project_root_dir}/setup.py"; then
    my_banner "setup.py install on virtual environment"
    install_clean_virtual_environment
    cd "${project_root_dir}" || exit
    if ! ~/venv/bin/python3 "${project_root_dir}/setup.py" install; then
      my_banner_warning "setup.py install ERROR"
      beep
      sleep "${sleeptime_on_error}"
      return 1
    fi
  fi
}


function setup_test_venv() {
  if test -f "${project_root_dir}/setup.py"; then
    my_banner "setup.py test on virtual environment"
    install_clean_virtual_environment
    cd "${project_root_dir}" || exit
    if ! ~/venv/bin/python3 "${project_root_dir}/setup.py" test; then
      my_banner_warning "setup.py test ERROR"
      beep
      sleep "${sleeptime_on_error}"
      return 1
    fi
  fi
}


function test_commandline_interface_venv() {
  # this will fail if rotek lib directory is in the path - keep this as a reminder
  my_banner "test commandline interface on virtual environment"

  clr_green "issuing command : $HOME/venv/bin/wrapt_timeout_decorator --version"
  if ! "$HOME/venv/bin/wrapt_timeout_decorator" --version; then
    my_banner_warning "test commandline interface on virtual environment ERROR"
    beep
    sleep "${sleeptime_on_error}"
    return 1
  fi
}


function test_setup_test_venv() {
  if test -f "${project_root_dir}/setup.py"; then
    my_banner "setup.py test"
    install_clean_virtual_environment
    cd "${project_root_dir}" || exit
    if ! ~/venv/bin/python3 "${project_root_dir}/setup.py" test; then
      my_banner_warning "setup.py test ERROR"
      beep
      sleep "${sleeptime_on_error}"
      return 1
    fi
  fi
}


# cleanup on cntrl-c
trap cleanup EXIT
