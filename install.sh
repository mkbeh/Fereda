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


## yellow            \e[1;33m \e[0m
## green             \e[1;32m \e[0m
## red               \e[1;31m \e[0m


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
  |  ||  7  |!__   7  7  7  |  7  ||  !___|  !___|  __|_|  _ \\
  |  ||  |  |7     |  |  |  |  |  ||     7|     7|     7|  7  |
  !__!!__!__!!_____!  !__!  !__!__!!_____!!_____!!_____!!__!__!
"
author="||| CREATED BY NoName |>"
slogan="With the goal of making the world better..."


set -e

clear
printf "\e[1m%s\n\e[0m" "$logo"
printf "\t\e[1;31m%s\e[0m\n\n" "$author"
printf "\t\e[1;31m%s\e[0m\n\n" "$slogan"

# Only checks for current OS and display specific message.
OPERATION_SYSTEM=$(uname -o)

if [[ "$OPERATION_SYSTEM" == "GNU/Linux" ]]; then
    printf "\e[1;33m::> Running Fereda Installer...\n\e[0m" && sleep 1s
else
    err_msg="
  3RROR!!!!!! You are not using Linux.
  It means you are using another OS.
  Use supported OS or install utility manually."
    printf "\e[1;31m%s\n\e[0m" "$err_msg"
    return 1
fi

# Checks for the presence of the environment variable PYTHONPATH which
# must contains utility clonned directory in the system shell
# configuration file and if the PYTHONPATH env variable is missing,
# it will be successfully added.
userShell=$(echo "$SHELL" | rev | cut -d'/' -f 1 | rev)
postfix="rc"
shellCfgName=$userShell$postfix
shellCfgPath="$HOME/.$shellCfgName"
requireStr="export PYTHONPATH=\"$(pwd | sed 's/\ /\\\ /g')\""
compareResult=false

printf "\e[1;33m::> Cheching is PYTHONPATH in .%s...\n\e[0m" "$shellCfgName" && sleep 1s

while IFS= read -r line
do
    if [[ $line == "$requireStr" ]]; then
        printf "\e[1;32m[+] PYTHONPATH is already added to .%s\n\e[0m" "$shellCfgName" && sleep 1s

        compareResult=true
        break
    fi
done <<< "$(tail -n5 "$shellCfgPath")"

if ! $compareResult ; then
    printf "\e[1;33m::> PYTHONPATH is not added to .%s. Adding PYTHONPATH...\n\e[0m" "$shellCfgName" && sleep 1s
    echo "$requireStr" >> "$shellCfgPath" && . "$shellCfgPath"
    printf "\e[1;32m[+] PYTHON path successfully added to %s\n\e[0m" "$shellCfgName" && sleep 1s
fi

# First, look for installed versions of Python, then check whether installed
# versions of Python in the current system are in the list of supported ones.
INSTALLED_PYTHON_VERSION=""
SUPPORTED_PYTHON_VERSIONS=(3.7 3.8)
INCORRECT_PYTHON_VERSION_ERROR=\
"\e[1;33m::> To installing Fereda utility - previously you need to install Python (supported versions: ${SUPPORTED_PYTHON_VERSIONS[*]}).
    Use this guide https://realpython.com/installing-python/#ubuntu to istall Python.\n\e[0m"

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
    echo "$INCORRECT_PYTHON_VERSION_ERROR"
    return 1
else
    printf "\e[1;32m[+] Found installed %s\n\e[0m" "$pythonVersion" && sleep 1s
fi

printf "\e[1;33m::> Checking is installed Python version supported...\n\e[0m" && sleep 1s
installedVersionNum=$(echo "$pythonVersion" | cut -d' ' -f2)
supportedFlag=false

for rVer in "${SUPPORTED_PYTHON_VERSIONS[@]}"; do
    if [[ "$installedVersionNum" =~ ^$rVer ]]; then
        printf "\e[1;32m[+] Installed Python %s version supported. \e[0m \n" "$installedVersionNum" && sleep 1s
        supportedFlag=true
        break
    fi
done

# Installing `Fereda` utility.
if [ $supportedFlag = true ];then
    printf "\e[1;33m::> Installing Fereda utility...\e[0m \n" && sleep 1s
else
    echo "$INCORRECT_PYTHON_VERSION_ERROR"
    return 1
fi

function getLatestPackageInDir {
    local package=$(ls dist/ | sort -V | tail -n 1)
    echo "${package}"
}

$INSTALLED_PYTHON_VERSION setup.py bdist_egg --exclude-source-files &> /dev/null
package=$(getLatestPackageInDir)

if [[ -n $VIRTUAL_ENV ]]; then
    $INSTALLED_PYTHON_VERSION -m easy_install dist/"${package}" > /dev/null
else
    $INSTALLED_PYTHON_VERSION -m easy_install --user dist/"${package}" > /dev/null
fi

printf "\e[1;32m[+] Utility was successfully installed. To use it run command: ~/.local/bin/fereda -h\n\e[0m"
rm -rf build/ dist/ Fereda.egg-info
