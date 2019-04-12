#!/bin/bash
save_path="`dirname \"$0\"`"

# if used outside github/travis You need to set :
# WINEARCH=win32    for 32 Bit Wine
# WINEARCH=""       for 64 Bit Wine
# WINEPREFIX defaults to ${HOME}/.wine   or you need to pass it via environment variable

# if running headless, the xvfb service needs to run

## set wine prefix to ${HOME}/.wine if not given by environment variable
if [[ -z ${WINEPREFIX} ]]
    then
        echo "WARNING - no WINEPREFIX in environment - set now to ${HOME}/.wine"
        WINEPREFIX=${HOME}/.wine
    fi


if [[ -z ${WINEARCH} ]]
    then
        echo "WARNING - no WINEARCH in environment - will install 64 Bit Python"
        echo "in Order to install 32Bit You need to set WINEARCH=\"win32\""
        echo "in Order to install 64Bit You need to set WINEARCH=\"\""
    fi


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


wine_drive_c_dir=${WINEPREFIX}/drive_c
decompress_dir=${HOME}/bitranox_decompress
mkdir -p ${decompress_dir}

python_version_short=python37
python_version_doc="Python 3.7"

echo "Download ${python_version_doc} Binaries"
https://github.com/bitranox/binaries_${python_version_short}_wine/archive/master.zip
wget -nc --no-check-certificate -O ${decompress_dir}/binaries_${python_version_short}_wine-master.zip https://github.com/bitranox/binaries_${python_version_short}_wine/archive/master.zip

echo "Unzip ${python_version_doc} Master to ${HOME}"
unzip -nqq ${decompress_dir}/binaries_${python_version_short}_wine-master.zip -d ${decompress_dir}

if [[ "${WINEARCH}" == "win32" ]]
    then
        echo "Joining Multipart Zip in ${decompress_dir}/binaries_${python_version_short}_wine-master/bin"
        cat ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/python*_wine_32* > ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/joined_${python_version_short}.zip
        add_pythonpath="c:/Python37-32;c:/Python37-32/Scripts"
    else
        echo "Joining Multipart Zip in ${decompress_dir}/binaries_${python_version_short}_wine-master/bin"
        cat ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/python*_wine_64* > ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/joined_${python_version_short}.zip
        add_pythonpath="c:/Python37-64;c:/Python37-64/Scripts"
    fi

echo "Unzip ${python_version_doc} to ${wine_drive_c_dir}"
unzip -qq ${decompress_dir}/binaries_${python_version_short}_wine-master/bin/joined_${python_version_short}.zip -d ${wine_drive_c_dir}

echo "add Path Settings to Registry"
wine_current_reg_path="`wine reg QUERY \"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\" /v PATH | grep REG_SZ | sed 's/^.*REG_SZ\s*//'`"
wine_new_reg_path="${add_pythonpath};${wine_current_reg_path}"
wine reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /t REG_SZ /v PATH /d "${wine_new_reg_path}" /f
wine_actual_reg_path="`wine reg QUERY \"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\" /v PATH | grep REG_SZ | sed 's/^.*REG_SZ\s*//'`"

rm -r ${decompress_dir}

cd ${save_path}
echo "******************************************************************************************************************"
echo "******************************************************************************************************************"
echo "FINISHED installing Python 3.7 on WINE, Wine Registry PATH=${wine_actual_reg_path}"
echo "******************************************************************************************************************"
