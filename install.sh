#!/bin/bash


# This file is part of Fereda.

# Fereda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License 3 as published by
# the Free Software Foundation.

# Fereda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Fereda.  If not, see <https://www.gnu.org/licenses/>.


# Copyright (c) 2020 January mkbeh


set -e
shopt -s extglob


clear
logo="
  _________________________________  _______
  7     77     77  _  77     77    \ 7  _  7
  |  ___!|  ___!|    _||  ___!|  7  ||  _  |
  |  __| |  __|_|  _ \ |  __|_|  |  ||  7  |
  |  7   |     7|  7  ||     7|  !  ||  |  |
  !__!   !_____!!__!__!!_____!!_____!!__!__!
                                          
  _____________________________________   ____   ______________
  7  77     77     77      77  _  77  7   7  7   7     77  _  7
  |  ||  _  ||  ___!!__  __!|  _  ||  |   |  |   |  ___!|    _|
  |  ||  7  |!__   7  7  7  |  7  ||  !___|  !___|  __|_|  _ \ 
  |  ||  |  |7     |  |  |  |  |  ||     7|     7|     7|  7  |
  !__!!__!__!!_____!  !__!  !__!__!!_____!!_____!!_____!!__!__!                      
"
author="||| CREATED BY EXp0s3R3b_RTH SQUAD |> v0.1"

printf "\e[1m%s\n\e[0m" "$logo"
printf "\t\e[1;31m%s\e[0m\n\n" "$author"

declare -r BASHRC_LOC="$HOME/.bashrc"


# yellow            \e[1;33m \e[0m
# green             \e[1;32m \e[0m
# red               \e[1;31m \e[0m


 OPERATION_SYSTEM=$(uname -o)
 SUPPORTED_PYTHON_VERSIONS=(3.7 3.8)
 INSTALLED_PYTHON_VERSION=""


function addPYTHONPATH {
    requireStr="export PYTHONPATH=\"$(pwd | sed 's/\ /\\\ /g')\""
    compareResult=false

    printf "\e[1;33m::> Cheching is PYTHONPATH in .bashrc...\n\e[0m" && sleep 2s

    while IFS= read -r line
    do
        if [[ $line == "$requireStr" ]]; then
            printf "\e[1;32m[+] PYTHONPATH already added to .bashrc\n\e[0m" && sleep 2s

            compareResult=true
            break
        fi
    done <<< "$(tail -n5 "$BASHRC_LOC")"

    if ! $compareResult ; then
        printf "\e[1;33m::> PYTHONPATH not added to .bashrc. Adding PYTHONPATH...\n\e[0m" && sleep 1s
        echo "$requireStr" >> "$BASHRC_LOC" && . "$BASHRC_LOC"
        printf "\e[1;32m[+] PYTHON path successfully added\n\e[0m" && sleep 1s
    fi
}


function getLatestPackageInDir {
    local package=$(ls dist/ | sort -V | tail -n 1)
    echo "${package}"
}


function installUtil {
    $INSTALLED_PYTHON_VERSION setup.py bdist_egg --exclude-source-files
    package=$(getLatestPackageInDir)
    
    if [[ -n $VIRTUAL_ENV ]]; then
        $INSTALLED_PYTHON_VERSION -m easy_install dist/"${package}"
    else
        $INSTALLED_PYTHON_VERSION -m easy_install --user dist/"${package}"
    fi

    printf "\e[1;32m[+] Utility was successfully installed. To use it run command: ~/.local/bin/fereda -h\n\e[0m" && sleep 1s
}


function isPythonVersionSupport {
    printf "\e[1;33m::> Checking is installed Python version supported...\n\e[0m" && sleep 2s
    installedVersionNum=$(echo "$1" | cut -d' ' -f2) 

    for rVer in "${SUPPORTED_PYTHON_VERSIONS[@]}"; do
        if [[ "$installedVersionNum" =~ ^$rVer ]]; then
            printf "\e[1;32m[+] Installed Python %s version supported. \e[0m \n" "$installedVersionNum" && sleep 3s
            printf "\e[1;33m::> Installing Fereda utility...\e[0m \n" && sleep 4s
            installUtil
            return         
        fi
    done

    installRequirements
}


function installAndroidRequirements {
    printf "::> Installing requirements for %s...\n" "$OPERATION_SYSTEM"

    pkg install x11-repo
    pkg update && pkg upgrade -y
    pkg install python -y
    pkg install sox -y                           # fixed python-magic
    pkg install libjpeg-turbo clang -y           # Fixed Pillow
    pkg install clang fftw

    INSTALLED_PYTHON_VERSION=$(python --version 2>&1 | tr "[:upper:]" "[:lower:]" | sed -e 's/ //' | cut -c1-7)
}


function installRequirements {
    if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
        installAndroidRequirements
        installUtil
    else
        printf "\e[1;33m::> To installing Fereda util in debug mode previously you need to install Python (supported versions: %s).\n" \
             "Use this guidehttps://realpython.com/installing-python/#ubuntu to istall Python.\e[0m" "${SUPPORTED_PYTHON_VERSIONS[*]}"
    fi
}


function isPythonInstalled {
    pythonVersions=(
        "$(command python -V 2> /dev/null || echo Not Found)"
        "$(command python3 -V 2> /dev/null || echo Not Found)"
    )

    for pythonVersion in "${pythonVersions[@]}"; do
        if [[ "$pythonVersion" =~ ^Python\ 3 ]]; then
            INSTALLED_PYTHON_VERSION=$(echo "$pythonVersion" | tr "[:upper:]" "[:lower:]" | sed -e 's/ //' | cut -c1-7)
            break
        fi
    done

    if test -z "$INSTALLED_PYTHON_VERSION"; then
        printf "\e[1;33m::> Python is not installed, installing Python...\n\e[0m" && sleep 2s
        installRequirements
    else 
        printf "\e[1;32m[+] Found installed %s\n\e[0m" "$pythonVersion" && sleep 3s
        isPythonVersionSupport "$pythonVersion"
    fi
}


function debug {
    printf "\e[1;33m::> Running debug mode...\n\e[0m" && sleep 1s
    addPYTHONPATH
    isPythonInstalled
}


function battle {
    printf "\e[1;33m::> Running battle mode...\n\e[0m" && sleep 1s
    isPythonInstalled

    cd .. && rm -rf Fereda
}


if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
    printf "\e[1;31mbattle mode not supported now...\n\e[0m" && sleep 1s
    # battle
elif [[ "$OPERATION_SYSTEM" == "GNU/Linux" ]]; then
    debug
else
    err_msg="3RROR!!!!!! You are not using Linux or Android OS.
    It means you are using another OS.
    Use supported OS or install utility manually.
    "
    printf "\e[1;31m%s\n\e[0m" "$err_msg"
fi
