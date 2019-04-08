#!/bin/bash
save_path="`dirname \"$0\"`"

if [[ -z ${wine_windows_version} ]]
    then
        echo "WARNING - no wine_windows_version in environment - set now to win10"
        echo "available Versions: win10, win2k, win2k3, win2k8, win31, win7, win8, win81, win95, win98, winxp"
        wine_windows_version="win10"
    fi

echo "Setup Wine Machine at ${WINEPREFIX}, WINEARCH=${WINEARCH}, wine_windows_version=${wine_windows_version}"
mkdir -p ${WINEPREFIX}
wine_drive_c_dir=${WINEPREFIX}/drive_c
# xvfb-run --auto-servernum winecfg # fails marshal_object couldnt get IPSFactory buffer for interface ...
winecfg

echo "Disable GUI Crash Dialogs"
winetricks nocrashdialog

echo "Set Windows Version to ${wine_windows_version}"
winetricks -q ${wine_windows_version}

echo "Install common Packets"
# winetricks -q msxml6
# winetricks -q dotnet462
# winetricks -q allfonts
winetricks -q windowscodecs

cd ${save_path}
