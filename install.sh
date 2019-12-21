#!/bin/bash


##! if this - it means remove comment

# echo "export PYTHONPATH=/path/to/tool" >> ~/.bashrc && . ~/.bashrc
# chmod u+x run.sh


function install {
    echo lol
}


function isPythonVersionLowerThanRequire {
    echo "сhecking if python version is right"
}


function isPythonInstalled {
    ##! if lower than 3.7 - install latest version

    python_version=$(python --version 2>&1)

    if [[ "$python_version" =~ ^Python ]]; then
        echo "Found $python_version"
    else
        echo "Installing python..."
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
    if [[ "$(uname -o)" == "Android" ]]; then
        battle
    else
        debug
    fi
}


modesHandler
