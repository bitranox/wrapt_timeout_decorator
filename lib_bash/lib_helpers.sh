#!/bin/bash

function include_dependencies {
    local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
    source "${my_dir}/lib_color.sh"
}

include_dependencies  # we need to do that via a function to have local scope of my_dir


function fail {
  clr_bold clr_red "${1}" >&2
  exit 1
}

function get_linux_codename {
    local linux_codename=`lsb_release --codename | cut -f2`
    echo "${linux_codename}"
}

function export_linux_codename {
    local linux_codename=`lsb_release --codename | cut -f2`
    export ${linux_codename}
}



## make it possible to call functions without source include
# Check if the function exists (bash specific)
if [[ ! -z "$1" ]]
    then
        if declare -f "${1}" > /dev/null
        then
          # call arguments verbatim
          "$@"
        else
          # Show a helpful error
          function_name="${1}"
          library_name="${0}"
          fail "\"${function_name}\" is not a known function name of \"${library_name}\""
        fi
	fi
