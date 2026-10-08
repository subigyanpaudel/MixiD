<img width="1330" height="887" alt="Screenshot From 2025-12-17 02-36-46" src="https://github.com/user-attachments/assets/af8ae915-9656-4139-ad9c-05965a8cdb66" />

# iD Mixer (MixiD)

[![GitHub Release](https://img.shields.io/github/v/release/subigyanpaudel/MixiD?include_prereleases&label=release)](https://github.com/subigyanpaudel/MixiD/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

Unofficial Linux control panel and mixer for the Audient iD series audio interfaces based on libusb, GLFW, and Dear ImGui.

> [!NOTE]
> **Project Origin & Custom Tweaks**:  
> The core mixer application and driver were originally created by [@TheOnlyJoey](https://github.com/TheOnlyJoey/MixiD). This fork provides the installation with additional tweaks and system packaging (desktop launcher, high-resolution icons, automatic udev rule configuration, and Debian packages).  
> The installation and packaging are maintained and tested on this local system by [@subigyanpaudel](https://github.com/subigyanpaudel), and will be updated sooner or later with further refinements and driver improvements.

---

## Features

- **Native Linux GUI**: Lightweight, responsive interface for Audient iD series audio interfaces.
- **Auto-Connect**: Automatically discovers and connects to your attached Audient device on startup.
- **Desktop Integration**: App launcher (`MixID`) for Ubuntu/GNOME "Show Applications" with custom icon.
- **Ready-to-use Packaging**: Pre-built `.deb` and `.tar.gz` packages available for easy installation.
- **udev Permissions Included**: Debian package configures udev rules automatically so non-root users can access the interface directly.

---

## Installation

### Option 1: Install Pre-built Package (.deb)

Pre-built packages are available on the [**Releases**](https://github.com/subigyanpaudel/MixiD/releases) page.

1. Download the latest `mixid_*.deb` package.
2. Install with `apt` (which resolves dependencies automatically):
   ```bash
   sudo apt install ./mixid_*_amd64.deb
   ```
   *Alternatively, using `dpkg`:*
   ```bash
   sudo dpkg -i mixid_*_amd64.deb
   sudo apt-get install -f  # resolves any missing dependencies
   ```

This automatically installs:
- The binary to `/usr/bin/MixiD` (with symlinks `/usr/bin/mixid` and `/usr/bin/id-mixer`)
- Desktop entries `mixid.desktop` and `id-mixer.desktop` to `/usr/share/applications/` (searchable as "MixID" in Show Applications)
- Scalable SVG and multi-resolution icons (16x16 up to 512x512)
- Udev rules to `/lib/udev/rules.d/84-audient.rules` and reloads udev rules automatically

> [!TIP]
> **Non-Debian distributions**: Download the portable `mixid-*-Linux.tar.gz` archive from the Releases page, extract it, and copy or run the binary from `usr/local/bin/MixiD`.

---

### Option 2: Build & Package from Source

#### Prerequisites & Dependencies
On Ubuntu / Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    libglew-dev \
    libglfw3-dev \
    libusb-1.0-0-dev \
    libgl1-mesa-dev \
    inkscape \
    python3-pil
```

#### Build & Create Packages (.deb & .tar.gz)
Run the packaging script:
```bash
./build_deb.sh
```

Or configure and build manually with CMake and CPack:
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)
(cd build && cpack)
```
This produces both `mixid_*_amd64.deb` and `mixid-*-Linux.tar.gz` inside the `build/` directory and project root.

---

## Usage

* With udev rules installed (automatically done via `.deb` package), simply open **MixID** from your desktop's **Show Applications** menu or run `MixiD` / `mixid` from your terminal.
* The application will automatically probe and connect to your plugged-in Audient audio interface on launch.

### Manual udev rules (if not using .deb)

Since by default the audio interface is grabbed by the kernel module, exclusive device access is needed to send mixer control information without root permissions.
Add the Audient vendor ID to udev rules:

For user in `audio` group:
```bash
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2708", MODE="0666", GROUP="audio"' | sudo tee /etc/udev/rules.d/84-audient.rules
```
Or for `plugdev` group:
```bash
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2708", MODE="0666", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/84-audient.rules
```

Reload the rules:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## Authors & Credits

* **Original Author**: Joey Ferweda ([@TheOnlyJoey](https://github.com/TheOnlyJoey/MixiD) / [Mastodon](https://mastodon.online/@TheOnlyJoey)) — reverse engineering, mixer UI, and device driver logic.
* **Packaging, Desktop Integration & Tweaks**: Subigyan Paudel ([@subigyanpaudel](https://github.com/subigyanpaudel/MixiD)) — desktop integration, icons, Debian & TGZ packaging, with ongoing updates on this system.

---

## Version History

* 0.1.6
   * Added desktop application launcher (`.desktop`) and full icon set (16x16 to 512x512 + SVG).
   * Added Debian packaging (`.deb`) and generic archive (`.tar.gz`) via CPack.
   * All known iD USB IDs implemented.
* 0.1.4
   * Probes USB devices based on supported ID list.
   * Auto disconnects and re-attaches to kernel when quitting application.
   * Properly sets faders depending on individual device inputs.
   * UI bugfixes.
* 0.1
   * Initial release based around iD14 and iD14 MKII.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* [mymixer](https://github.com/r00tman/mymixer), prior attempt to reverse engineer the original iD14 with minimal functionality.
* [imgui](https://github.com/ocornut/imgui), modern lightweight GUI framework.
