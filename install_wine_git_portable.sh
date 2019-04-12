#!/bin/bash
save_path="`dirname \"$0\"`"

# if used outside github/travis You need to set :
# WINEARCH=win32    for 32 Bit Wine
# WINEARCH=         for 64 Bit Wine
# WINEPREFIX defaults to ${HOME}/.wine   or you need to pass it via environment variable

# if running headless, the xvfb service needs to run

if [[ -z ${WINEPREFIX} ]]
    then
        echo "WARNING - no WINEPREFIX in environment - set now to ${HOME}/.wine"
        WINEPREFIX=${HOME}/.wine
    fi

if [[ -z ${WINEARCH} ]]
    then
        echo "WARNING - no WINEARCH in environment - will install 64 Bit Git"
        echo "in Order to install 32Bit You need to set WINEARCH=\"win32\""
        echo "in Order to install 64Bit You need to set WINEARCH=\"\""
    fi

echo "Check if we run headless and xvfb Server is running"
xvfb_framebuffer_service_active="False"
systemctl is-active --quiet xvfb && xvfb_framebuffer_service_active="True"
if [[ ${xvfb_framebuffer_service_active} == "True" ]]
	then
		echo "we run headless, xvfb service is running"
	else
	    echo "we run on normal console, xvfb service is not running"
	fi


wine_drive_c_dir=${WINEPREFIX}/drive_c
decompress_dir=${HOME}/bitranox_decompress
mkdir -p ${decompress_dir}

echo "Download Git Portable Binaries"
wget -nc --no-check-certificate -O ${decompress_dir}/binaries_portable_git-master.zip https://github.com/bitranox/binaries_portable_git/archive/master.zip

echo "Unzip Git Portable Binaries Master to ${decompress_dir}"
unzip -nqq ${decompress_dir}/binaries_portable_git-master.zip -d ${decompress_dir}

if [[ "${WINEARCH}" == "win32" ]]
    then
        echo "Joining Multipart Zip in ${decompress_dir}/binaries_portable_git-master/bin"
        cat ${decompress_dir}/binaries_portable_git-master/bin/PortableGit32* > ${decompress_dir}/binaries_portable_git-master/bin/joined_PortableGit.zip
        add_git_path="c:/PortableGit32/cmd"
    else
        echo "Joining Multipart Zip in ${decompress_dir}/binaries_portable_git-master/bin"
        cat ${decompress_dir}/binaries_portable_git-master/bin/PortableGit64* > ${decompress_dir}/binaries_portable_git-master/bin/joined_PortableGit.zip
        add_git_path="c:/PortableGit64/cmd"
    fi

echo "Unzip Git Portable Binaries to ${wine_drive_c_dir}"
unzip -qq ${decompress_dir}/binaries_portable_git-master/bin/joined_PortableGit.zip -d ${wine_drive_c_dir}

echo "add Path Settings to Registry"
wine_current_reg_path="`wine reg QUERY \"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\" /v PATH | grep REG_SZ | sed 's/^.*REG_SZ\s*//'`"
wine_new_reg_path="${add_git_path};${wine_current_reg_path}"
wine reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /t REG_SZ /v PATH /d "${wine_new_reg_path}" /f
wine_actual_reg_path="`wine reg QUERY \"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\" /v PATH | grep REG_SZ | sed 's/^.*REG_SZ\s*//'`"
echo "Wine PATH=${wine_actual_reg_path}"

rm -r ${decompress_dir}

cd ${save_path}
echo "******************************************************************************************************************"
echo "******************************************************************************************************************"
echo "FINISHED installing Git Portable on WINE, Wine Registry PATH=${wine_actual_reg_path}"
echo "******************************************************************************************************************"
