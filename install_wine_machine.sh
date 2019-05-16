#!/bin/bash
function include_dependencies {
    local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
    chmod +x "${my_dir}"/lib_bash/*.sh
    source "${my_dir}/lib_bash/lib_color.sh"
    source "${my_dir}/lib_bash/lib_retry.sh"
    source "${my_dir}/lib_bash/lib_wine_install.sh"
}

include_dependencies  # we need to do that via a function to have local scope of my_dir

clr_bold clr_green "Install Wine Machine"
check_wine_prefix
check_wine_arch
check_wine_windows_version
check_headless_xvfb
export_wine_version_number

clr_bold clr_green "Setup Wine Machine at ${WINEPREFIX}, WINEARCH=${WINEARCH}, wine_windows_version=${wine_windows_version}"
mkdir -p ${WINEPREFIX}
wine_drive_c_dir=${WINEPREFIX}/drive_c
# xvfb-run --auto-servernum winecfg # fails marshal_object couldnt get IPSFactory buffer for interface ...

if [[ ${xvfb_framebuffer_service_active} == "True" ]]; then sudo service xvfb stop ; fi   # winecfg fails if xvfb server is running
winecfg
if [[ ${xvfb_framebuffer_service_active} == "True" ]]; then sudo service xvfb start ; fi     # winecfg fails if xvfb server is running

clr_bold clr_green "Disable GUI Crash Dialogs"
winetricks nocrashdialog

clr_bold clr_green "Set Windows Version to ${wine_windows_version}"
winetricks -q ${wine_windows_version}

clr_bold clr_green "Install common Packets :"
clr_bold clr_green "install windowscodecs"
retry winetricks -q windowscodecs

clr_bold clr_green "******************************************************************************************************************"
clr_bold clr_green "install msxml3"
if [[ ${wine_version_number} == "wine-4.8" ]]; then clr_bold clr_red "known regression, msxml3 does not work on wine-4.8" ; else retry winetricks -q msxml3 ; fi
clr_bold clr_green "******************************************************************************************************************"
clr_bold clr_green "install msxml6"
retry winetricks -q msxml6
clr_bold clr_green "******************************************************************************************************************"
clr_bold clr_green "done"
clr_bold clr_green "******************************************************************************************************************"
clr_bold clr_green "FINISHED installing Wine Machine ${WINEPREFIX}"
clr_bold clr_green "******************************************************************************************************************"
