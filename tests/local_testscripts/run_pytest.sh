#!/bin/bash

own_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit && pwd -P )" # this gives the full path, even for sourced scripts

DO_PYTEST="True"


# shellcheck disable=SC2050
if [[ "True" != "True" ]]; then
    echo "exit - ${BASH_SOURCE[0]} is not configured by PizzaCutter"
    exit 0
fi

# shellcheck disable=SC1090
source "${own_dir}/lib_bash_functions.sh"
project_root_dir="${project_root_dir}"
# cleanup on cntrl-c
trap cleanup EXIT

function do_tests {
        banner "Project Root Dir: ${project_root_dir}"
        # pytest options can be passed to run_pytest like --disable-warnings
        # take care that all 3rd party stub files are in one folder and
        # that folder is in the mypy path
        # a more loose setting here would be:
        # if ! run_pytest --disable-warnings --follow-imports=silent; then
        if [ "${DO_PYTEST}" == "True" ]; then
            if ! run_pytest --disable-warnings; then
                banner_warning "TESTS FAILED for ${project_root_dir}"
                exit 1
            fi
        fi
}

do_tests
