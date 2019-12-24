#!/bin/bash


##! if this - it means remove comment

# echo "export PYTHONPATH=/path/to/tool" >> ~/.bashrc && . ~/.bashrc
# chmod u+x run.sh


OPERATION_SYSTEM=""


function installRequirements {
    echo "Installing python or requirements..."
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

    supportVersions=(3.7 3.8)
    installedVersionNum=$(echo "$1" | cut -d' ' -f2) 

    for rVer in "${supportVersions[@]}"; do
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
    else 
        echo "[+] Found installed $pythonVersion"
        isPythonVersionSupport "$pythonVersion"
    fi
}


function debug {
    echo "::> Running debug mode..."
    isPythonInstalled
}


function battle {
    echo "::> Running battle mode..."
    echo 'Installing termux packages...'
    isPythonInstalled
}


function modesHandler {
    OPERATION_SYSTEM=$(uname -o)

    if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
        battle
    else
        debug
    fi
}


modesHandler