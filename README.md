# Fereda

![Platform](https://img.shields.io/badge/Platform-all-RED)
![Python](https://img.shields.io/badge/Python-3.7|3.8-BRIGHTGREEN)
![Release](https://img.shields.io/github/v/release/mkbeh/Fereda)
![Issues](https://img.shields.io/github/issues/mkbeh/Fereda)
![License](https://img.shields.io/badge/License-GPLv3.0-Yellow)

[![Discord](https://user-images.githubusercontent.com/7288322/34429117-c74dbd12-ecb8-11e7-896d-46369cd0de5b.png)](https://discord.gg/Ftaynpe)

Cyber security tool of mobile forensics for restoring hide and removed images from gallery and different messengers on Android.

```lang
Methods of the donation to the development of the project:

Bitcoin: bc1qwcp93tr7t7rlwe86zpglusstaq8j50dag0q6ll
```

**`Supporting devices`**:

* Samsung
* Redmi
* Micromax

**`Supporting messengers`**:

* Telegram
* VK (added , but not tested yet)

```lang
NOTE #1:
The list of supported devices means that the utility 
has been tested on these devices, but it can work 
correctly on many other devices.

NOTE #2:
Not all devices manage to recover deleted images, 
since not all devices cache them.
```

**The following actions were performed on Debian based
distr with kernel 5.4.0+**

## **Installation and usage screen cast**

[![Fereda Screencast](https://img.youtube.com/vi/9rh5tERPF40/0.jpg)](https://www.youtube.com/watch?v=9rh5tERPF40&t=191s)

## Installation

```bash
# Bash script for downloading latest github release
# Ex. downloadGithubLatestRelease mkbeh Fereda zip true

# Download latest release from github.
# Require jq utility.
# Params: <user> <repo_name> <archieveType:(zip or tar)> <unpack:(true or false)>
function downloadGithubLatestRelease() {
        user=$1
        repoName=$2
        archieveType=$3
        unpack=$4

        url=$(curl "https://api.github.com/repos/$user/$repoName/releases/latest" | jq -r ".${archieveType}ball_url")
        wget -O "$repoName" $url
         
        if [[ $unpack = "false" ]]; then
                return 0
        fi


        if [[ $archieveType == "zip" ]]; then
                unzip $repoName
        else
                tar -xzf $repoName
        fi

        rm $repoName && mv $(ls | grep $repoName) $repoName
}
```

> downloadGithubLatestRelease mkbeh Fereda zip true && cd Fereda

### **Linux**

> chmod u+x install.sh && $SHELL install.sh

### **Other OS**

> python3.7 setup.py install

## Usage

### **Options**

* --restore-data - Will copy found files into output directory. Without this option, it will simply show how many files were found and in what places.
* --self-destruction - Will remove utility from path ~/.local/bin&&lib. Works only on Linux.
* --move-files - Will move found files from its places into output directory. Works with option `--restore-data`.
* --off-progress-bar - It will improve performance.
* --output-dir - Directory where will be copied or moved found files. By default it named `Fereda` and it will be located in the same directory where the utility was launched.

### **Examples**

**`First step`**

```bash
# ---- Plug in your phone via usb,
# ---- Enable USB debugging in Developer Settings
# ---- Install ADB (Android Debug Bridge)
# ---- Run following commands:
adb devices
adb pull /path/to/user/folder .

# Next, go to the second step.

IMPORTANT NOTE:
User folder contains directories such as DCIM Pictures and etc.
```

**`Second step`**

```bash
# ---- Show help message ----
fereda -h

# ---- Simple run. Only shows how many files were found and in what places ----
fereda

# ---- Restore (copy) found files to output directory ----
fereda -r

# ---- Restore (move) found files from its location to output directory ----
fereda -rm
```

## Roadmap

* [ ] Text files analysis by regex.
* [ ] Databases analysis: including raw SQL request, 
by tables, columns names and fields values using regex.
* [ ] Restore hidden and removed images from gallery and
messengers from the file system , including SDCARD.
* [ ] Dump data:
    * [ ] Calls
    * [ ] Messages
    * [ ] Contacts
    * [ ] Coordinates
    * [ ] Backups
    * [ ] Accounts (Experimental)
    * [ ] Browser cookies
    * [ ] Browser history