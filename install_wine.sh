#!/bin/bash
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
sudo apt-get install --install-recommends winehq-devel
sudo apt-get install -y winetricks
