#!/bin/bash

function install_lib_bash_wine_if_not_exist {
    local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
    if [[ ! -d "${my_dir}/lib_bash_wine" ]]; then
        git clone https://github.com/bitranox/lib_bash_wine.git ${my_dir}/lib_bash_wine > /dev/null 2>&1
        chmod -R +x ${my_dir}/lib_bash_wine/*.sh
    fi
}

function update_lib_bash_wine_if_exist {
    local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
    if [[ -d "${my_dir}/lib_bash_wine" ]]; then
        cd lib_bash_wine
        local git_remote_hash=$(git --no-pager ls-remote --quiet | grep HEAD | awk '{print $1;}' )
        local git_local_hash=$(git --no-pager log --decorate=short --pretty=oneline -n1 | grep HEAD | awk '{print $1;}' )
        git fetch --all  > /dev/null 2>&1
        git reset --hard origin/master  > /dev/null 2>&1
        chmod -R +x ./*.sh
        cd ..
    fi
}

update_lib_bash_wine_if_exist
install_lib_bash_wine_if_not_exist
