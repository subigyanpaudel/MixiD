<img width="1330" height="887" alt="Screenshot From 2025-12-17 02-36-46" src="https://github.com/user-attachments/assets/af8ae915-9656-4139-ad9c-05965a8cdb66" />

# iD Mixer (MixiD)

Unofficial Linux control panel and mixer for the Audient iD series audio interfaces based on libusb, GLFW, and Dear ImGui.

## Features

- **Native Linux GUI**: Lightweight, responsive interface for Audient iD series audio interfaces.
- **Auto-Connect**: Automatically discovers and connects to your attached Audient device on startup.
- **Desktop Integration**: App launcher (`iD Mixer`) for Ubuntu/GNOME "Show Applications" with custom icon.
- **udev Permissions Included**: Debian package configures udev rules automatically so non-root users can access the interface directly.

## Installation

### Option 1: Install Debian Package (.deb)

If you downloaded or built the `.deb` package, install it with:

```bash
sudo dpkg -i id-mixer_0.1.6_amd64.deb
sudo apt-get install -f  # resolves any missing dependencies
```

This installs:
- The binary to `/usr/bin/MixiD` (and symlink `/usr/bin/id-mixer`)
- Desktop entry to `/usr/share/applications/id-mixer.desktop` (searchable as "iD Mixer" in Show Applications)
- Scalable and high-resolution icons (16x16 up to 512x512)
- Udev rules to `/lib/udev/rules.d/84-audient.rules`

### Option 2: Build & Package from Source

#### Dependencies
* CMake (>= 3.15)
* libglew-dev
* libglfw3-dev
* libusb-1.0-0-dev
* GCC or Clang
* Inkscape (for icon generation)

#### Build & Create .deb
```bash
./build_deb.sh
```
Or with CMake directly:
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)
(cd build && cpack -G DEB)
```

## Usage

* With udev rules installed (or via the `.deb` package), simply open **iD Mixer** from Ubuntu's **Show Applications** or run `MixiD` / `id-mixer` from terminal.
* The application will automatically probe and connect to your plugged-in Audient audio interface on launch.

### udev rules

Since by default, the audio interface is grabbed by the kernel module, and we require exclusive device grab to send information, we need to setup udev rules to allow not needing to use root permissions when opening MixiD.
Luckily, all we have to do is add the Audient vendor id to the udev rules.
The specific user might be different for your distro, but "plugdev" and "audio" seem to be the most commonly used.

Either:
```
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2708", MODE="0666", GROUP="audio"' >> /etc/udev/rules.d/84-audient.rules
```
or
```
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2708", MODE="0666", GROUP="plugdev"' >> /etc/udev/rules.d/84-audient.rules
```
depending on your distro's permission group.

Then either reboot or use the following command to reload the udev rules for the running system.
```
udevadm control --reload-rules
```
All done!

## Authors

[@TheOnlyJoey](https://mastodon.online/@TheOnlyJoey)

## Version History

* 0.1.6
   * All known iD usb-id's are now known and implemented, MixiD should work on every known interface!
* 0.1.4
    * Now probes usb devices based on the supported id list and selects if possible
    * Auto disconnects and re-attach to kernel when quitting the application (no more having to manually disconnect before closing)
    * Now should properly set all faders depending on the individual device inputs
    * Small UI Fixes
* 0.1
    * Initial Release based around the iD14 and iD14 MKII with most essential features implemented.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* [mymixer](https://github.com/r00tman/mymixer), prior attempt to reverse engineer the original iD14 with some minimal functionality.
* [imgui](https://github.com/ocornut/imgui), my favorite modern lightweight gui
