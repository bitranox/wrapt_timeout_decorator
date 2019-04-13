#!/bin/bash
my_dir="$(dirname "${0}")"
chmod +x ${my_dir}/lib_bash/*.sh
source ${my_dir}/lib_bash/lib_color.sh
source ${my_dir}/lib_bash/lib_retry.sh

function fail {
  clr_bold clr_red "${1}" >&2
  exit 1
}


function check_wine_version {
    if [[ -z ${wine_version} ]]
        then
            crl_bold clr_red "WARNING - no wine_version in environment set - set now to default: devel"
            echo "available Versions: stable, devel, staging"
            export wine_version="devel"
        fi
}


function check_wine_prefix {
    ## set wine prefix to ${HOME}/.wine if not given by environment variable
    if [[ -z ${WINEPREFIX} ]]
        then
            crl_bold clr_red "WARNING - no WINEPREFIX in environment - set now to ${HOME}/.wine"
            export WINEPREFIX=${HOME}/.wine
        fi
}

function check_wine_arch {
    if [[ -z ${WINEARCH} ]]
        then
            crl_bold clr_red "WARNING - no WINEARCH in environment - will install 64 Bit Wine"
            crl_bold clr_red "in Order to install 32Bit You need to set WINEARCH=\"win32\""
            crl_bold clr_red "in Order to install 64Bit You need to set WINEARCH=\"\""
        fi
}


function check_wine_windows_version {
    if [[ -z ${wine_windows_version} ]]
        then
            crl_bold clr_red "WARNING - no wine_windows_version in environment - set now to win10"
            crl_bold clr_red "available Versions: win10, win2k, win2k3, win2k8, win31, win7, win8, win81, win95, win98, winxp"
            export wine_windows_version="win10"
        fi
}


function check_headless_xvfb {
    clr_green "Check if we run headless and xvfb Server is running"
    export xvfb_framebuffer_service_active="False"
    systemctl is-active --quiet xvfb && export xvfb_framebuffer_service_active="True"
    # run winetricks with xvfb if needed
    if [[ ${xvfb_framebuffer_service_active} == "True" ]]
        then
            clr_green "we run headless, xvfb service is running"
        else
            clr_green "we run on normal console, xvfb service is not running"
        fi
}

function prepend_path_to_wine_registry {
    add_pythonpath=${1}
    clr_green "add Path Settings to Registry"
    wine_current_reg_path="`wine reg QUERY \"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\" /v PATH | grep REG_SZ | sed 's/^.*REG_SZ\s*//'`"
    wine_new_reg_path="${add_pythonpath};${wine_current_reg_path}"
    wine reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /t REG_SZ /v PATH /d "${wine_new_reg_path}" /f
    wine_actual_reg_path="`wine reg QUERY \"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\" /v PATH | grep REG_SZ | sed 's/^.*REG_SZ\s*//'`"
    crl_green "adding Path done"
    crl_bold crl_green "Wine Registry PATH=${wine_actual_reg_path}"
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
