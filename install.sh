#!/bin/bash
set -e
shopt -s extglob


chmod u+x install.sh
declare -r BASHRC_LOC="$HOME/.bashrc"


 OPERATION_SYSTEM=$(uname -o)
 SUPPORTED_PYTHON_VERSIONS=(3.7 3.8)


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


function installRequirements {
    if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
        echo "::> Installing requirements for $OPERATION_SYSTEM..."
        installUtil
    else
        echo "::> To installing Fereda util in debug mode previously you need to install Python (supported versions: ${SUPPORTED_PYTHON_VERSIONS[*]})." \
             "Use this guidehttps://realpython.com/installing-python/#ubuntu to istall Python."
    fi
}


function getLatestPackageInDir {
    local package=$(ls dist/ | sort -V | tail -n 1)
    echo "${package}"
}


function installUtil {
    python3.7 setup.py bdist_egg --exclude-source-files
    package=$(getLatestPackageInDir)
    python3.7 -m easy_install --user dist/"${package}"

    echo "[+] Util was successfully installed. To use it run command: 'fereda -h'"
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

    printf "::> Installed Python %s not supported. Installing latest Python...\n" "$installedVersionNum"
}


function isPythonInstalled {
    pythonVersions=("$(python --version 2>&1)" "$(python3 --version 2>&1)")
    installedPythonVersion=""

    for pythonVersion in "${pythonVersions[@]}"; do
        if [[ "$pythonVersion" =~ ^Python\ 3 ]]; then
            installedPythonVersion="$pythonVersion"
            break
        fi
    done

    if test -z "$installedPythonVersion"; then
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
}


if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
    battle
else
    debug
fi
