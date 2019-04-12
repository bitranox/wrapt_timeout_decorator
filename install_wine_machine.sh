#!/bin/bash
save_path="`dirname \"$0\"`"

echo "Check if we run headless and xvfb Server is running"
xvfb_framebuffer_service_active="False"
systemctl is-active --quiet xvfb && xvfb_framebuffer_service_active="True"
# run winetricks with xvfb if needed
if [[ ${xvfb_framebuffer_service_active} == "True" ]]
	then
		echo "we run headless, xvfb service is running"
	else
	    echo "we run on normal console, xvfb service is not running"
	fi


if [[ -z ${wine_windows_version} ]]
    then
        echo "WARNING - no wine_windows_version in environment - set now to win10"
        echo "available Versions: win10, win2k, win2k3, win2k8, win31, win7, win8, win81, win95, win98, winxp"
        wine_windows_version="win10"
    fi

if [[ -z ${WINEARCH} ]]
    then
        echo "WARNING - no WINEARCH in environment - will install 64 Bit Wine"
        echo "in Order to install 32Bit You need to set WINEARCH=\"win32\""
        echo "in Order to install 64Bit You need to set WINEARCH=\"\""
    fi


echo "Setup Wine Machine at ${WINEPREFIX}, WINEARCH=${WINEARCH}, wine_windows_version=${wine_windows_version}"
mkdir -p ${WINEPREFIX}
wine_drive_c_dir=${WINEPREFIX}/drive_c
# xvfb-run --auto-servernum winecfg # fails marshal_object couldnt get IPSFactory buffer for interface ...

if [[ ${xvfb_framebuffer_service_active} == "True" ]]; then sudo service xvfb stop ; fi   # winecfg fails if xvfb server is running
winecfg
if [[ ${xvfb_framebuffer_service_active} == "True" ]]; then sudo service xvfb start ; fi     # winecfg fails if xvfb server is running

echo "Disable GUI Crash Dialogs"
winetricks nocrashdialog

echo "Set Windows Version to ${wine_windows_version}"
winetricks -q ${wine_windows_version}

echo "Install common Packets"

winetricks -q windowscodecs
winetricks -q msxml3

cd ${save_path}
