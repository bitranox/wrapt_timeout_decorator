#!/bin/bash

own_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit && pwd -P )" # this gives the full path, even for sourced scripts

# shellcheck disable=SC1090
source "${own_dir}/lib_bash_functions.sh"
install_dependencies

project_root_dir="${project_root_dir}"

function pytest_loop {

    while true; do
        banner "Project Root Dir: ${project_root_dir}"
        clean_caches
        if ! pytest_codestyle_mypy; then continue; fi
        if ! mypy_strict; then continue; fi
        if ! mypy_strict_with_imports; then continue; fi
        if ! install_pip_requirements_venv; then continue; fi
        if ! setup_install_venv; then continue; fi
        if ! test_commandline_interface_venv; then continue; fi
        if ! test_setup_test_venv; then continue; fi

        banner "ALL TESTS PASSED for ${project_root_dir}"
        banner "ALL TESTS PASSED for ${project_root_dir}"
        banner "ALL TESTS PASSED for ${project_root_dir}"
        sleep 5
    done

}

# upgrade_pytest
# upgrade_mypy
pytest_loop
