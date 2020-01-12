# Fereda

[TO DO add badge issues]

[TO DO add badge release]

![Platform](https://img.shields.io/badge/Platform-all-RED)
![Python](https://img.shields.io/badge/Python-3.7|3.8-BLUE)
![Version](https://img.shields.io/badge/Version-v0.1-BRIGHTGREEN)
![License](https://img.shields.io/badge/License-GPLv3.0-Yellow)

[![Discord](https://user-images.githubusercontent.com/7288322/34429117-c74dbd12-ecb8-11e7-896d-46369cd0de5b.png)](https://discord.gg/zPxXhr)

Cyber security tool of mobile forensics for restoring hide and removed images from gallery and different messengers on Android.

```lang
Methods of the donation to the development of the project:

Bitcoin: bc1qwcp93tr7t7rlwe86zpglusstaq8j50dag0q6ll
```

**`Supporting devices`**:

* Samsung Note 8
* RedmiGo 7A
* Micromax

**`Supporting messengers`**:

* Telegram
* VK (added , but not tested yet)

```lang
NOTE:
The list of supported devices means that the utility has been tested on these devices, but it can work correctly on many other devices.
```

## Installation

> git clone https://github.com/mkbeh/Fereda.git && cd Fereda

### **Linux**

> chmod u+x install.sh && ./install.sh

### **Other OS**

> python3.7 setup.py install

## Usage

[TO DO youtube screen cast]

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

* Add support for other devices.

* Add search and recovery images from the entire storage
(if device is rooted) and from SDCARD.

* Add option for searching and coping / recovering of files by regex.

* Add analysis of text files and notes to the occurrence of a custom template or regex.

* Add file metadata search.

* Add support for other messengers.

* Add new options such as --exlude-dirs , --include-dirs and search in custom user directories.

* Add an option in which you can select directories or name of application for search and recovery. For example, only a gallery, only messengers, instant messengers to choose from, etc.

* Add sending the found data to the remote server.

* Сreate .apk to use the utility directly on the phone.

* Add loging.

* Other.
