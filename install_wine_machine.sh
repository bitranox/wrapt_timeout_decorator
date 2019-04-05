#!/bin/bash
save_path="`dirname \"$0\"`"

echo "Setup Wine Machine at ${WINEPREFIX}, WINEARCH=${WINEARCH} "
mkdir -p ${WINEPREFIX}
wine_drive_c_dir=${WINEPREFIX}/drive_c

# xvfb-run --auto-servernum winecfg # fails marshal_object couldnt get IPSFactory buffer for interface ...
winecfg

echo "Disable GUI Crash Dialogs"
winetricks nocrashdialog

echo "Install common Packets"
winetricks -q msxml6
winetricks -q dotnet462
winetricks -q allfonts
winetricks -q windowscodecs

cd ${save_path}
