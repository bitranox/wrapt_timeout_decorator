#!/bin/bash
save_dir="$PWD"
# this gives the full path, even for sourced scripts
dir_own="$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit && pwd -P)"

sudo_askpass="$(command -v ssh-askpass)"
export SUDO_ASKPASS="${sudo_askpass}"
# get rid of (ssh-askpass:25930): dbind-WARNING **: 18:46:12.019: Couldn't register with accessibility bus: Did not receive a reply.
export NO_AT_BRIDGE=1

dir_travis_secrets="${dir_own}"
# one level up
project_root_dir="$(dirname "${dir_travis_secrets}")"

# CONSTANTS
True=0
False=1

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

function purge_linux_package_ruby() {
    # purges ruby and all ruby gems
    sudo apt-get purge ruby -y
    sudo apt-get purge ruby-dev -y
    sudo rm -rf /usr/share/rubygems-integration
    sudo rm -rf /var/lib/gems
    sudo rm -rf /usr/bin/gems
    sudo rm -rf /usr/share/ri
}


function is_travis_gem_installed() {
  if [[ $(sudo gem list | grep -c travis) == 0 ]]; then
    return $False
  else
    return $True
  fi
}


function install_travis_gem() {
  sudo gem install travis
}


function check_install_travis_gem() {
    if ! is_travis_gem_installed ; then
        banner "Ruby Travis Gem is not installed, I will install it for You"
        wait_for_enter
        install_travis_gem
    fi
}


function check_install_ruby_dev() {
    if ! is_package_installed ruby-dev; then
        banner "Linux Package ruby-dev is not installed, I will install it for You"
        wait_for_enter
        install_package_if_not_present ruby-dev
    fi
}

function install_dependencies() {
  clr_green "installing dependencies"
  check_install_ruby_dev
  check_install_travis_gem
}

cd "${save_dir}"||exit
