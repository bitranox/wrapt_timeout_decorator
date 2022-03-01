#!/bin/bash
# test the shellscripts in the current directory

save_dir="$PWD"

# install bash helper scripts
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


function check_shellcheck_installed {
  # check if shellcheck is installed, otherwise install it
  if ! is_package_installed shellcheck; then
      banner "shellcheck is not installed, I will install it for You"
      wait_for_enter
      install_package_if_not_present shellcheck
  fi
}


function shell_check {
    banner "checking shellscripts"
    # exclude Codes :
    # SC1091 not following external sources -> so we dont check /usr/local/lib_bash/lib_helpers.sh
    if shellcheck --shell=bash --color=always \
                  --exclude=SC1091 \
                  ./*.sh \
                  ; then
        banner "finished shellcheck without errors"
    else
        banner_warning "finished shellcheck, some errors occured, check the output"
    fi

}

check_shellcheck_installed
shell_check
cd "${save_dir}"||exit
