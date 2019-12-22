#!/bin/bash


##! if this - it means remove comment

# echo "export PYTHONPATH=/path/to/tool" >> ~/.bashrc && . ~/.bashrc
# chmod u+x run.sh


# ПРИ DEBUG МОДЕ ПРОБОВАТЬ ВЫЗЫВАТЬ 2 КОМАНДЫ PYTHON И PYTHON3 (с цифрой 3)


OPERATION_SYSTEM=""


function install {
    echo "Installing python or requirements..."
}


function isPythonVersionSupport {
    echo "Checking is installed Python version supported..."

    supportVersions=(3.7 3.8)
    installedVersionNum=$(echo "$1" | cut -d' ' -f2) 

    for rVer in "${supportVersions[@]}"; do
        if [[ "$installedVersionNum" =~ ^$rVer ]]; then
            printf ">> Installed Python version supported. Installed: Python %s\n" "$installedVersionNum"
            return         
        fi
    done

    printf "Installed Python %s not supported. Installing latest Python...\n" "$installedVersionNum"
}


function isPythonInstalled {
    python_version=$(python --version 2>&1)

    if [[ "$python_version" =~ ^Python ]]; then
        echo ">> Found installed $python_version"
        isPythonVersionSupport "$python_version"
    else
        echo "Python is not installed, installing Python..."
    fi
}


function debug {
    echo "Running debug mode..."
    isPythonInstalled
}


function battle {
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