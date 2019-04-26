#!/bin/bash

function include_dependencies {
    local my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"  # this gives the full path, even for sourced scripts
    chmod +x "${my_dir}"/lib_bash/*.sh
    source "${my_dir}/lib_bash/lib_color.sh"
    source "${my_dir}/lib_bash/lib_retry.sh"
    source "${my_dir}/lib_bash/lib_wine_install.sh"
}

include_dependencies  # we need to do that via a function to have local scope of my_dir

# if used outside github/travis You need to set :
# WINEARCH=win32    for 32 Bit Wine
# WINEARCH=         for 64 Bit Wine
# WINEPREFIX defaults to ${HOME}/.wine   or you need to pass it via environment variable
# if running headless, the xvfb service needs to run


clr_bold clr_green "Install Python 2.7 on WINE"
check_wine_prefix
check_wine_arch

wine_drive_c_dir=${WINEPREFIX}/drive_c
decompress_dir=${HOME}/bitranox_decompress
mkdir -p ${decompress_dir}

python_version_short=python27
python_version_doc="Python 2.7"

clr_green "Download ${python_version_doc} Binaries from https://github.com/bitranox/binaries_${python_version_short}_wine/archive/master.zip"
retry wget -nc --no-check-certificate -O ${decompress_dir}/binaries_${python_version_short}_wine-master.zip https://github.com/bitranox/binaries_${python_version_short}_wine/archive/master.zip

clr_green "Unzip ${python_version_doc} Master to ${HOME}"
unzip -nqq ${decompress_dir}/binaries_${python_version_short}_wine-master.zip -d ${decompress_dir}

if [[ "${WINEARCH}" == "win32" ]]
    then
        clr_green "Joining Multipart Zip in ${decompress_dir}/binaries_${python_version_short}_wine-master/bin"
        cat ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/python*_wine_32* > ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/joined_${python_version_short}.zip
        add_pythonpath="c:/Python27-32;c:/Python27-32/Scripts"
    else
        clr_green "Joining Multipart Zip in ${decompress_dir}/binaries_${python_version_short}_wine-master/bin"
        cat ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/python*_wine_64* > ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/joined_${python_version_short}.zip
        add_pythonpath="c:/Python27-64;c:/Python27-64/Scripts"
    fi

clr_green "Unzip ${python_version_doc} to ${wine_drive_c_dir}"
unzip -qq ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/joined_${python_version_short}.zip -d ${wine_drive_c_dir}

prepend_path_to_wine_registry ${add_pythonpath}

clr_green "done"
clr_green "******************************************************************************************************************"
clr_bold clr_green "FINISHED installing Python 2.7 on Wine Machine ${WINEPREFIX}"
clr_green "******************************************************************************************************************"

