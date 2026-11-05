<div align="center">
  <img src="cvm.jpg" alt="CVM-colorBot Logo" width="200"/>

  # CVM-colorBot

  **Color-based computer vision aimbot for Windows and macOS**

  [![Original Repo](https://img.shields.io/badge/Original-asenyeroao--ct%2FCVM--colorBot-blue?style=for-the-badge&logo=github)](https://github.com/asenyeroao-ct/CVM-colorBot)
  [![Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/pJ8JkSBnMB)
</div>

---

> **Credit**: Original project by [asenyeroao-ct](https://github.com/asenyeroao-ct/CVM-colorBot). This fork adds macOS support and this rewritten guide. All core detection and aiming code is theirs. See [LICENSE](LICENSE).

---

## What This Does

CVM-colorBot reads a video feed of your game, finds player outlines by their color, and moves your mouse toward the closest target. It works two ways:

**2-PC setup** (recommended): One PC runs the game. A second machine (Windows or Mac) has a capture card reading the game video, and a USB device (MAKCU, Arduino) that acts as a mouse on the game PC. CVM runs on the second machine, processes the video, and sends mouse commands through the USB device.

**Single-PC setup**: CVM captures your own screen (MSS) and moves the mouse with software input (SendInput on Windows, Quartz on macOS). No extra hardware.

---

## Table of Contents

- [Requirements](#requirements)
- [Install on Windows](#install-on-windows)
- [Install on macOS](#install-on-macos)
- [2-PC Hardware Wiring](#2-pc-hardware-wiring)
- [First Launch](#first-launch)
- [Step 1: Connect Video](#step-1-connect-video)
- [Step 2: Connect Mouse Device](#step-2-connect-mouse-device)
- [Step 3: Set Target Color](#step-3-set-target-color)
- [Step 4: Configure Aimbot](#step-4-configure-aimbot)
- [Step 5: Configure Triggerbot](#step-5-configure-triggerbot)
- [Step 6: Recoil Control (RCS)](#step-6-recoil-control-rcs)
- [Saving Configs](#saving-configs)
- [Platform Compatibility Table](#platform-compatibility-table)
- [Troubleshooting](#troubleshooting)
- [What This Fork Changed](#what-this-fork-changed)

---

## Requirements

**Python**: 3.11, 3.12, or 3.13. Python 3.14 is not supported.

**Windows**: 10 or 11.

**macOS**: 10.15 Catalina or later.

**2-PC hardware** (skip if single-PC):
- A USB capture card
- An HDMI cable from game PC to capture card
- A mouse controller device (MAKCU, Arduino, or compatible serial adapter)

---

## Install on Windows

### Quick setup

```
git clone https://github.com/weemkvm/CVM-colorBot-macOS.git
cd CVM-colorBot-macOS
setup.bat
```

This creates a virtual environment and installs everything. Then run:

```
run.bat
```

### Manual setup

```
git clone https://github.com/weemkvm/CVM-colorBot-macOS.git
cd CVM-colorBot-macOS
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Install on macOS

### Step 1: Get Python

```bash
brew install python@3.12
```

Check it works:

```bash
python3 --version
```

### Step 2: Clone and install

```bash
git clone https://github.com/weemkvm/CVM-colorBot-macOS.git
cd CVM-colorBot-macOS
chmod +x setup.sh run.sh
./setup.sh
```

### Step 3: Grant Accessibility access

macOS blocks apps from moving the mouse unless you allow it.

1. Open **System Settings > Privacy & Security > Accessibility**
2. Click **+** and add your terminal app (Terminal, iTerm2, Warp, etc.)
3. Toggle it **on**

Without this, mouse movement will silently fail.

### Step 4: Run

```bash
./run.sh
```

Or manually:

```bash
source venv/bin/activate
python3 main.py
```

---

## 2-PC Hardware Wiring

```
 GAME PC                                AIM PC (Win or Mac)
+-----------------+                    +------------------------+
|                 |  HDMI out          |                        |
|  Game running   |────────────────────>  Capture card (USB)    |
|                 |                    |                        |
|  MAKCU plugged  |<─── USB serial ───|  CVM-colorBot running  |
|  into USB       |                    |  Sends mouse commands  |
+-----------------+                    +------------------------+
```

**Game PC side**: Plug the MAKCU (or Arduino) into a USB port. The OS sees it as a mouse. Play your game normally.

**Aim PC side**: Plug the capture card into USB. Connect HDMI from the game PC GPU output to the capture card input. Plug the other end of the MAKCU USB into this machine for serial communication.

The aim PC reads the game video through the capture card, runs color detection, and sends mouse-move commands to the MAKCU over serial. The MAKCU translates those into real mouse movements on the game PC.

---

## First Launch

When you start CVM, you get a window with tabs: **General**, **Aimbot**, **Sec Aimbot**, **Trigger**, **RCS**, **Config**. Work through these in order.

---

## Step 1: Connect Video

Open the **General** tab. At the top you see capture controls.

### Pick your capture mode

| Mode | When to use | Platform |
|------|-------------|----------|
| **CaptureCard** | Capture card plugged in via USB. Uses OpenCV. | Win + Mac |
| **CaptureCardGStreamer** | Same hardware, GStreamer pipeline. Try if OpenCV fails. | Win + Mac |
| **MSS** | Screen capture, no extra hardware. Single-PC setup. | Win + Mac |
| **UDP** | OBS streaming from another PC over network. | Win + Mac |
| **NDI** | NDI protocol over LAN from OBS or NDI Tools. | Win only |

### Capture Card setup

1. Set **Capture Mode** to `CaptureCard` (or `CaptureCardGStreamer`)
2. Set **Device Index** to the correct device (usually 0 or 1, try both)
3. Set **Resolution** to match your game output (1920x1080 is common)
4. Set **FPS** (240 is default, lower if your card tops out at 60 or 120)
5. Click **CONNECT**

If the Detection window opens showing your game feed, it worked. If it is black or missing, try the other capture mode or a different device index.

**GStreamer install** (only needed for CaptureCardGStreamer mode):
- Windows: Download the MSVC x86_64 runtime from https://gstreamer.freedesktop.org/download/
- macOS: `brew install gstreamer`

### MSS setup (single-PC, no capture card)

1. Set **Capture Mode** to `MSS`
2. Set **Monitor Index** (1 = primary monitor)
3. Set **FOV X** and **FOV Y**: how many pixels from screen center to capture in each direction. 320x320 is a good start.
4. Click **CONNECT**

### UDP setup

1. On the game PC, configure OBS to output a UDP stream to your aim PC's IP
2. Set **Capture Mode** to `UDP`
3. Enter the **IP** (aim PC's LAN IP, or 127.0.0.1 if same machine) and **Port**
4. Click **CONNECT**

---

## Step 2: Connect Mouse Device

Still in the **General** tab, find the **Hardware API** section.

### MAKCU / Serial (most common for 2-PC)

1. Set **Mouse API** to `Serial`
2. **Port Mode**: `Auto` scans for known devices (MAKCU, CH343, CH340, CH347, CP2102). Use this first.
3. If Auto fails, switch to `Manual` and pick the port:
   - Windows: `COM3`, `COM4`, etc. (check Device Manager > Ports)
   - macOS: `/dev/tty.usbserial-XXXX` (run `ls /dev/tty.usb*` to find it)
4. Click **CONNECT**
5. Click **Test Move** to verify. Your game PC cursor should jump 100 pixels.

### Arduino

1. Upload the CVM-compatible Arduino sketch to your board
2. Set **Mouse API** to `Arduino`
3. Set port and baud rate (default 115200)
4. Click **CONNECT**

### SendInput / Quartz (single-PC, no hardware)

1. Set **Mouse API** to `SendInput`
2. Click **CONNECT**
3. On Windows this uses the Win32 SendInput API. On macOS it automatically uses Quartz (CoreGraphics).
4. macOS: make sure you granted Accessibility permissions (see install section).

### Other devices

| Device | API Setting | Config needed |
|--------|-------------|---------------|
| Net (KMNet) | `Net` | IP, Port, UUID. Windows only (needs DLL). |
| KmboxA | `KmboxA` | VID/PID. Windows only. |
| MakV2 | `MakV2` | Port, Baud (default 4Mbps). |
| MakV2Binary | `MakV2Binary` | Port, Baud. |
| DHZ | `DHZ` | IP, Port. |
| Ferrum | `Ferrum` | Device path. |

---

## Step 3: Set Target Color

This is the most important step. Bad color settings = nothing detected or everything detected.

### How detection works

Each frame is converted to HSV color space. Pixels matching your color range are kept, everything else is discarded. The remaining pixels are grouped into blobs, which become detected targets.

### Quick start

In the **General** tab, find the **Settings** section.

1. Set **Color** to one of the presets: `yellow`, `purple`, `red`. These cover common game outline colors.
2. Look at the **Detection** window. You should see colored bounding boxes around players.

If the preset works, you are done. Move to Step 4.

### Custom color tuning

If no preset matches your game's outline color:

1. Set **Color** to `custom`
2. Open the **Custom HSV** section
3. Open **HSV Preview** (button in that section). This shows the raw frame and the filtered mask side by side.
4. Adjust the six sliders:

| Slider | What it controls | Tips |
|--------|-----------------|------|
| **H Min / H Max** | Hue range (the actual color). | Yellow: 20-40. Purple: 120-160. Red: 0-10 and 170-179. |
| **S Min / S Max** | Saturation (color intensity). | Set S Min to 50-80 to ignore gray and white. |
| **V Min / V Max** | Value (brightness). | Set V Min to 50-100 to ignore dark areas. |

5. Watch the mask preview. White pixels = detected. Narrow the range until only player outlines show up.

### Detection parameters (fine tuning)

In **General > Detection Parameters**:

| Parameter | What it does | Default | Tip |
|-----------|-------------|---------|-----|
| Min BBox Area | Minimum blob size (pixels squared) to count as a target | 150 | Raise to 200-300 if you get noise blobs |
| Open Kernel | Morphological open (removes small noise) | 3 | Raise to 5 if lots of tiny dots |
| Close Kernel | Morphological close (fills small gaps) | 5 | Lower to 3 if outlines are too thick |
| Mask Blur | Gaussian blur on the mask | 3 | Leave at 3 unless edges are jagged |
| Min Contour Points | Minimum contour complexity | 5 | Raise to 8-10 to filter stray shapes |
| Merge Distance | How close blobs merge into one target | 12 | Raise if one player splits into multiple targets |

---

## Step 4: Configure Aimbot

Open the **Aimbot** tab.

### Enable it

Check **Enable Aimbot**.

### Pick an operation mode

| Mode | How it works | Best for |
|------|-------------|----------|
| **Normal** | Smooth continuous correction toward the target. | General use. Start here. |
| **Silent** | Flicks to target, clicks, returns to original position. | Single-shot weapons like snipers. |
| **NCAF** | Stronger pull near crosshair, weaker far away. Feels natural. | Players who want help near the target but not full lock. |
| **WindMouse** | Curved, human-like mouse paths. | Looking more natural in replays. |
| **Bezier** | Bezier curve interpolation. | Smooth movement similar to WindMouse. |

### Key settings explained

| Setting | What it does | Start value | Higher means |
|---------|-------------|-------------|-------------|
| **X Speed** | Horizontal aim correction speed | 2-3 | Faster snap left/right |
| **Y Speed** | Vertical aim correction speed | 2-3 | Faster snap up/down |
| **Smooth** | Smoothing factor (higher = more gradual) | 20-30 | Slower, more controlled movement |
| **Smooth FOV** | Inner zone where extra smoothing kicks in | 20-30 | Larger "slow down" zone near target |
| **FOV Size** | Max distance from crosshair to look for targets (pixels) | 100-150 | Wider search area |
| **ADS FOV** | Separate FOV when aiming down sights | 60-80 | Enable for tighter aim while scoped |
| **Max Speed** | Absolute cap on mouse movement per frame | 1000 | Safety limit, rarely needs changing |

### Aim type

| Type | Aims at |
|------|---------|
| **head** | Estimated head position (top ~22% of body bbox). Default. |
| **body** | Center of the full body bounding box. |
| **nearest** | Closest point from head to body bottom. Adaptive. |

### Activation

- **Activation Type**: `hold_enable` = hold a button to aim. `toggle` = press once to turn on, again to turn off.
- **Mouse Button**: Which button activates. 1 = left click, 2 = right click, 3 = side button.

### ADS FOV (aim down sights)

Enable **ADS FOV** and set a smaller radius than your main FOV. Set the **ADS Key** to your right mouse button (or whatever you use to scope). When you hold that key, the aimbot uses the tighter FOV.

### Secondary Aimbot (Sec Aimbot tab)

An independent second aimbot with its own settings. Use it for:
- Different sensitivity when hip-firing vs scoped
- A different button for a different behavior
- A different aim type (head on main, body on secondary)

---

## Step 5: Configure Triggerbot

Open the **Trigger** tab.

The triggerbot automatically clicks when a target-colored pixel appears under your crosshair.

### Enable it

Check **Enable Triggerbot**.

### Key settings

| Setting | What it does | Start value |
|---------|-------------|-------------|
| **Trigger FOV** | Radius around crosshair center to check (pixels) | 5-10 |
| **Delay Min / Max** | Random delay before clicking (seconds) | 0.08 / 0.15 |
| **Hold Min / Max** | How long the click is held (ms) | 40 / 60 |
| **Cooldown Min / Max** | Minimum wait between trigger fires (seconds) | 0.0 / 0.0 |
| **ROI Size** | Pixel region around crosshair to sample | 8 |
| **Min Pixels** | How many colored pixels needed in ROI to fire | 4 |
| **Min Ratio** | Percentage of ROI that must be colored | 0.03 |
| **Confirm Frames** | Consecutive frames that must confirm before firing | 2 |

### Burst fire

- **Burst Count Min/Max**: Clicks per trigger activation. Set both to 1 for single fire. Set 2-3 for burst.
- **Burst Interval Min/Max**: Delay between burst clicks (seconds).

### Trigger activation

Same as aimbot: `hold_enable` or `toggle`, with a configurable button.

### ADS Trigger FOV

Like the aimbot, you can set a separate trigger FOV when ADSing. Enable **Trigger ADS FOV**, set a smaller radius, and pick the ADS key.

---

## Step 6: Recoil Control (RCS)

Open the **RCS** tab.

RCS pulls the mouse down while firing to counteract weapon recoil.

| Setting | What it does | Start value |
|---------|-------------|-------------|
| **Enable RCS** | Master toggle | Off |
| **Pull Speed** | Pixels to pull down per tick | 10 |
| **Activation Delay** | Ms after clicking before RCS activates | 100 |
| **Rapid Click Threshold** | If clicks are faster than this (ms), treat as full-auto spray | 200 |

Start with Pull Speed at 10 and test in-game. Increase until recoil feels flat. Different weapons need different values, so save weapon-specific configs.

---

## Saving Configs

Open the **Config** tab.

- **Save**: Type a name and save the current settings as a profile in `configs/`
- **Load**: Pick a saved profile to restore
- **Default**: Reset everything to factory defaults

Settings also auto-save to `config.json` every time you change them. Named profiles let you keep separate configs for different games, weapons, or setups.

---

## Platform Compatibility Table

### Video capture

| Backend | Windows | macOS |
|---------|---------|-------|
| CaptureCard (OpenCV) | Yes | Yes |
| CaptureCardGStreamer | Yes (install runtime) | Yes (`brew install gstreamer`) |
| MSS (screen capture) | Yes | Yes |
| UDP | Yes | Yes |
| NDI | Yes | No (cyndilib build fails on Mac) |

### Mouse control

| Backend | Windows | macOS |
|---------|---------|-------|
| Serial (MAKCU, CH340, etc.) | Yes | Yes |
| Arduino | Yes | Yes |
| SendInput / Quartz | Yes (Win32 API) | Yes (CoreGraphics) |
| MakV2 / MakV2Binary | Yes | Yes (serial) |
| DHZ | Yes | Yes (network) |
| Ferrum | Yes | Yes (serial) |
| Net (KMNet) | Yes (needs DLL) | No |
| KmboxA | Yes (needs DLL) | No |

### Serial ports

- **Windows**: Devices show as `COM3`, `COM4`, etc. Check Device Manager > Ports.
- **macOS**: Devices show as `/dev/tty.usbserial-XXXX` or `/dev/tty.usbmodemXXXX`. Run `ls /dev/tty.usb*` to list them.

---

## Troubleshooting

### Nothing appears in the Detection window

- Is your capture source connected? Check the cable, check the device index.
- Try switching between `CaptureCard` and `CaptureCardGStreamer`.
- For MSS, verify the monitor index is correct (1 = primary).
- Check the console output for error messages.

### Detection picks up everything / too much noise

- Your HSV range is too wide. Narrow it using the HSV Preview.
- Raise **Min BBox Area** to 200-400.
- Raise **Min Contour Points** to 8-10.
- Raise **S Min** (saturation minimum) to 80-100 to reject grays.

### Detection misses players

- Your HSV range is too narrow. Widen it.
- Lower **Min BBox Area**.
- Check if the game's outline color changes with distance or lighting. You may need a wider V range.

### Mouse not moving on game PC

- Check serial connection: right port, right baud.
- Click **Test Move** in the Hardware API section.
- MAKCU: try Auto mode first, then Manual with the specific port.
- macOS SendInput/Quartz: check **System Settings > Privacy & Security > Accessibility**.

### Aim overshoots or jitters

- Increase **Smooth** (try 40-60).
- Decrease **X Speed** and **Y Speed** (try 1-2).
- Increase **Smooth FOV** (try 40-50).
- Enable **Target Temporal Smoothing** in General settings.
- Raise **move_queue_merge_batch** to 6-8 (reduces queue jitter).

### Aim is too slow / barely moves

- Decrease **Smooth** (try 10-15).
- Increase **X Speed** and **Y Speed** (try 4-6).
- Decrease **Smooth FOV**.
- Check **Max Speed** is not set too low.

### Triggerbot fires at nothing

- Decrease **Trigger FOV** (try 3-5).
- Increase **Min Pixels** (try 6-8).
- Increase **Confirm Frames** (try 3-4).
- Check that your HSV range is clean (no noise in the center of screen area).

### Triggerbot does not fire

- Make sure it is enabled and the activation button is held.
- Increase **Trigger FOV**.
- Decrease **Min Pixels** and **Min Ratio**.
- Check that target-colored pixels are present at the crosshair position (use Detection window).

### GStreamer not found

- **Windows**: Install the MSVC x86_64 runtime from https://gstreamer.freedesktop.org/download/
- **macOS**: `brew install gstreamer`

### macOS: "Operation not permitted" or mouse does not move

Grant Accessibility permissions:
1. System Settings > Privacy & Security > Accessibility
2. Add your terminal app
3. Toggle on
4. Restart the terminal and CVM

---

## What This Fork Changed

This is a fork of [asenyeroao-ct/CVM-colorBot](https://github.com/asenyeroao-ct/CVM-colorBot). All original code and commit history is preserved.

**Added files**:
- `setup.sh` / `run.sh` - macOS launch scripts
- `requirements_macos.txt` - macOS dependencies (pyobjc-framework-Quartz instead of cyndilib)
- `src/utils/mouse/QuartzInputAPI.py` - macOS mouse/keyboard via CoreGraphics

**Modified files**:
- `src/utils/mouse/SendInputAPI.py` - delegates to QuartzInputAPI on macOS
- `main.py` - skips Windows-only ctypes.windll on macOS
- `src/capture/capture_service.py` - GStreamer detection handles macOS dylib paths
- `README.md` - this rewritten guide

---

## License

Copyright (c) 2025 **asenyeroao-ct**. All rights reserved.

- Personal, non-commercial use is permitted
- Modification and redistribution allowed with attribution to **asenyeroao-ct**
- Commercial use prohibited without written permission

See [LICENSE](LICENSE) for full terms.

## Support

- [Original Discord](https://discord.gg/pJ8JkSBnMB) for community help
- [Original GitHub Issues](https://github.com/asenyeroao-ct/CVM-colorBot/issues) for bugs and features
