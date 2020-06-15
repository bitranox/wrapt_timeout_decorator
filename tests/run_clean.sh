#!/bin/bash
own_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit && pwd -P )" # this gives the full path, even for sourced scripts

# shellcheck disable=SC1090
source "${own_dir}/lib_bash_functions.sh"

clean_caches
