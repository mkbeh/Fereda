#!/bin/bash
set -e
shopt -s extglob


# TODO: добавить цветной вывод и слипы


declare -r BASHRC_LOC="$HOME/.bashrc"


 OPERATION_SYSTEM=$(uname -o)
 SUPPORTED_PYTHON_VERSIONS=(3.7 3.8)
 INSTALLED_PYTHON_VERSION=""


function addPYTHONPATH {
    requireStr="export PYTHONPATH=\"$(pwd | sed 's/\ /\\\ /g')\""
    compareResult=false

    echo "::> Cheching is PYTHONPATH in .bashrc..."

    while IFS= read -r line
    do
        if [[ $line == "$requireStr" ]]; then
            echo "[+] PYTHONPATH already added to .bashrc"

            compareResult=true
            break
        fi
    done <<< "$(tail -n5 "$BASHRC_LOC")"

    if ! $compareResult ; then
        echo "::> PYTHONPATH not added to .bashrc. Adding PYTHONPATH..."
        echo "$requireStr" >> "$BASHRC_LOC" && . "$BASHRC_LOC"
        echo "[+] PYTHON path successfully added"
    fi
}


function getLatestPackageInDir {
    local package=$(ls dist/ | sort -V | tail -n 1)
    echo "${package}"
}


function installUtil {
    $INSTALLED_PYTHON_VERSION setup.py bdist_egg --exclude-source-files
    package=$(getLatestPackageInDir)
    $INSTALLED_PYTHON_VERSION -m easy_install --user dist/"${package}"

    echo "[+] Util was successfully installed. To use it run command: ~/.local/bin/fereda -h"
}


function isPythonVersionSupport {
    echo "::> Checking is installed Python version supported..."
    installedVersionNum=$(echo "$1" | cut -d' ' -f2) 

    for rVer in "${SUPPORTED_PYTHON_VERSIONS[@]}"; do
        if [[ "$installedVersionNum" =~ ^$rVer ]]; then
            printf "[+] Installed Python version supported. Installed: Python %s\n" "$installedVersionNum"
            echo "::> Installing Fereda utility..."
            installUtil
            return         
        fi
    done

    installRequirements
}


function installAndroidRequirements {
    echo "::> Installing requirements for $OPERATION_SYSTEM..."

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
        echo "::> To installing Fereda util in debug mode previously you need to install Python (supported versions: ${SUPPORTED_PYTHON_VERSIONS[*]})." \
             "Use this guidehttps://realpython.com/installing-python/#ubuntu to istall Python."
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
        echo "::> Python is not installed, installing Python..."
        installRequirements
    else 
        echo "[+] Found installed $pythonVersion"
        isPythonVersionSupport "$pythonVersion"
    fi
}


function debug {
    echo "::> Running debug mode..."
    addPYTHONPATH
    isPythonInstalled
}


function battle {
    echo "::> Running battle mode..."
    isPythonInstalled

    cd .. && rm -rf Fereda
}


if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
    echo "battle mode not supported now..."
    # battle
elif [[ "$OPERATION_SYSTEM" == "GNU/Linux" ]]; then
    debug
else
    echo "3RROR!!!!!! You are not using Linux or Android OS." \
         "It means you are using another OS." \
         "Use supported OS or remove this utility."
fi
