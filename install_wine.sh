#!/bin/bash

function include_dependencies {
    local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
    chmod +x "${my_dir}/lib_bash/*.sh"
    source "${my_dir}/lib_bash/lib_color.sh"
    source "${my_dir}/lib_bash/lib_retry.sh"
    source "${my_dir}/lib_bash/lib_wine_install.sh"
}

include_dependencies  # me need to do that via a function to have local scope of my_dir




clr_bold clr_green "Install WINE"
check_wine_version

clr_green "add 386 Architecture"
retry sudo dpkg --add-architecture i386
clr_green "add Wine Keys"
retry wget https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
clr_green "Wine Packages Update"
retry sudo apt-get update
clr_green "Wine Packages Install"
retry sudo apt-get install --install-recommends winehq-${wine_version}
retry sudo apt-get install -y cabextract
retry sudo apt-get install -y libxml2
retry sudo apt-get install -y libpng-dev

clr_green "Install latest Winetricks"
sudo rm -f /usr/bin/winetricks
retry sudo wget --directory-prefix=/usr/bin/ https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
sudo chmod +x /usr/bin/winetricks
retry sudo winetricks -q --self-update
clr_green "Install latest Winetricks - done"

clr_green "done"
clr_green "******************************************************************************************************************"
clr_bold clr_green "FINISHED installing WINE and WINETRICKS"
clr_green "******************************************************************************************************************"
