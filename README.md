# Fereda

Cyber security tool for restoring removed images from gallery and messengers on Android.

`Supporting`:

[TO DO]

## How to use

Step 1:
Download Termux app from google play https://play.google.com/store/apps/details?id=com.termux&hl=ru

Step 2 (Optional):
Сonnect the victim's attacked phone to own Wi-Fi AP (you need to install several packages that consume decently Internet traffic)

Step 3:

```bash
# Run the following commands in Termux.
termux-setup-storage
```

Copy `Fereda` utility to the victim's attacked phone into the `user storage (where locate DCIM PICTURES DOWNLOADS and etc` and run the following commands:

```bash
cd storage/shared/Fereda
termux-fix-shebang install.sh
chmod u+x install.sh
bash install.sh

# Then press `y` anywhere
```
