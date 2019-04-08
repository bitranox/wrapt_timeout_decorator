#!/bin/bash
save_path="`dirname \"$0\"`"

if [[ -z ${wine_version} ]]
    then
        echo "WARNING - no wine_version in environment - set now to devel"
        echo "available Versions: stable, devel, staging"
        wine_version="devel"
    fi


echo "Build Start"
echo "add 386 Architecture"
sudo dpkg --add-architecture i386
echo "add Wine Keys"
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
echo "Wine Packages Update"
sudo apt-get update
echo "Wine Packages Install"
sudo apt-get install --install-recommends winehq-${wine_version}
# sudo apt-get install -y winetricks

echo "Install latest Winetricks"
cd /usr/bin
sudo rm winetricks
sudo wget  https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
sudo chmod +x winetricks
sudo winetricks -q --self-update
echo "Install latest Winetricks - done"

cd ${save_path}
