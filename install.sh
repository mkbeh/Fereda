#!/bin/bash


# echo "export PYTHONPATH=/path/to/tool" >> ~/.bashrc && . ~/.bashrc
# chmod u+x run.sh


 OPERATION_SYSTEM=$(uname -o)


function installRequirements {
    echo "::> Installing requirements for $OPERATION_SYSTEM..."

    if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
        echo installing termux packages.........
    else
        sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
        libncursesw5-dev xz-utils tk-dev

        wget https://www.python.org/ftp/python/3.6.5/Python-3.7.6.tgz && tar xvf Python-3.6.5.tgz && 'cd Python-3.7.6 || exit'
        ./configure --enable-optimizations --with-ensurepip=install && make -j 8
    fi

    installUtil
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
    isPythonInstalled
}


if [[ "$OPERATION_SYSTEM" == "Android" ]]; then
    battle
else
    debug
fi
