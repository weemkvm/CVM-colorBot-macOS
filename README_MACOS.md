<div align="center">
  <img src="cvm.jpg" alt="CVM-colorBot Logo" width="200"/>

  # CVM-colorBot macOS Port

  **Computer-vision color aimbot running on macOS, controlling a Windows game PC**

  [![Original Repo](https://img.shields.io/badge/Original-asenyeroao--ct%2FCVM--colorBot-blue?style=for-the-badge&logo=github)](https://github.com/asenyeroao-ct/CVM-colorBot)
  [![Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/pJ8JkSBnMB)
</div>

---

## What Is This

CVM-colorBot detects player outlines by their color (HSV filtering) in a video feed, then moves your mouse toward the detected target. It is designed for **2-PC setups**: one PC runs the game, the other runs this tool and controls the mouse via a hardware device (MAKCU, Arduino, serial adapter, etc.).

This fork adds **macOS support** so you can run the detection/aiming side on a Mac instead of a second Windows machine.

**Original author**: [asenyeroao-ct](https://github.com/asenyeroao-ct). All core detection, aiming, and UI code is theirs. See the [LICENSE](LICENSE) for terms.

---

## Table of Contents

1. [How the 2-PC Setup Works](#how-the-2-pc-setup-works)
2. [What You Need](#what-you-need)
3. [Install (macOS)](#install-macos)
4. [Install (Windows)](#install-windows)
5. [First Run Walkthrough](#first-run-walkthrough)
6. [Connecting Your Video Source](#connecting-your-video-source)
7. [Connecting Your Mouse Device](#connecting-your-mouse-device)
8. [Tuning Color Detection](#tuning-color-detection)
9. [Configuring the Aimbot](#configuring-the-aimbot)
10. [Configuring the Triggerbot](#configuring-the-triggerbot)
11. [RCS (Recoil Control)](#rcs-recoil-control)
12. [Saving and Loading Configs](#saving-and-loading-configs)
13. [Troubleshooting](#troubleshooting)
14. [macOS-Specific Notes](#macos-specific-notes)
15. [What Changed From the Original](#what-changed-from-the-original)

---

## How the 2-PC Setup Works

```
 GAME PC (Windows)                    AIM PC (macOS or Windows)
+---------------------+              +---------------------------+
|                     |   HDMI out   |                           |
|  Game running       |──────────────>  Capture card receives    |
|  (e.g. Valorant)    |              |  the game video feed      |
|                     |              |                           |
|  MAKCU/Arduino      |<─── USB ────|  CVM-colorBot detects     |
|  receives mouse     |              |  targets and sends mouse  |
|  commands           |              |  movements via serial     |
+---------------------+              +---------------------------+
```

**Game PC**: Runs the game. Has a MAKCU or Arduino plugged into USB. The game sees mouse input from that device.

**Aim PC**: Has a capture card receiving the game's video via HDMI. Runs CVM-colorBot. Analyzes frames, finds colored outlines, calculates aim corrections, sends mouse move commands to the MAKCU/Arduino over USB serial.

For **single-PC setups**: Use MSS (screen capture) instead of a capture card, and SendInput (Windows) or Quartz (macOS) instead of a hardware mouse device.

---

## What You Need

### Hardware (2-PC setup)
- A capture card (any USB capture card that works with OpenCV or GStreamer)
- A mouse controller: MAKCU (recommended), Arduino, or any supported serial device
- HDMI cable from game PC to capture card
- USB cable from mouse controller to both PCs

### Hardware (single-PC setup)
- Nothing extra. Uses screen capture and software mouse input.

### Software
- **Python 3.11, 3.12, or 3.13** (3.14 is not supported)
- macOS 10.15+ or Windows 10/11

---

## Install (macOS)

### Step 1: Install Python

If you do not have Python 3.11+:
```bash
brew install python@3.12
```

Verify:
```bash
python3 --version
```

### Step 2: Clone and set up

```bash
git clone https://github.com/weemkvm/CVM-colorBot-macOS.git
cd CVM-colorBot-macOS
chmod +x setup.sh run.sh
./setup.sh
```

The setup script creates a virtual environment and installs all dependencies.

### Step 3: Grant Accessibility permissions

macOS blocks apps from moving the mouse unless you allow it.

1. Open **System Settings > Privacy & Security > Accessibility**
2. Click the **+** button
3. Add your terminal app (Terminal, iTerm2, Warp, etc.)
4. Make sure the toggle is **on**

Without this, the Quartz mouse backend will not move the cursor.

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

## Install (Windows)

```bash
git clone https://github.com/weemkvm/CVM-colorBot-macOS.git
cd CVM-colorBot-macOS
setup.bat
```

Then run:
```bash
run.bat
```

---

## First Run Walkthrough

When you launch the app, you get a window with tabs across the top. Here is what to do in order.

### 1. Connect your video source (General tab)

At the top of the General tab, you see the capture controls.

- **Capture Mode dropdown**: Pick your video source type
  - `CaptureCard` or `CaptureCardGStreamer` for a capture card
  - `NDI` for network video (NDI protocol)
  - `UDP` for OBS UDP streaming
  - `MSS` for screen capture (single-PC)
- Click **CONNECT**

If it works, the Detection window opens showing the video feed with overlays.

### 2. Connect your mouse device (General tab > Hardware API)

- **Mouse API dropdown**: Pick your device type
  - `Serial` for MAKCU and compatible adapters
  - `Arduino` for Arduino boards
  - `SendInput` for software mouse (no hardware needed)
  - `Net`, `KmboxA`, `MakV2`, `DHZ`, `Ferrum` for their respective devices
- For Serial: set port mode to Auto (it scans for MAKCU) or Manual (pick a COM port)
- Click **CONNECT**

### 3. Set your target color (General tab > Settings)

- **Color dropdown**: Pick the outline color your game uses
  - `yellow`, `purple`, `red`, or `custom`
- For custom: use the HSV sliders to dial in the exact color range
- Open the **HSV Preview** to see what the color filter is picking up in real time

### 4. Enable the aimbot (Aimbot tab)

- Check **Enable Aimbot**
- The default mode is **Normal** which works for most cases
- Set your activation button (which mouse button triggers aiming)

### 5. Test it

- Start a game with colored player outlines
- Hold your activation button
- The crosshair should pull toward detected targets

---

## Connecting Your Video Source

### Capture Card (recommended for 2-PC)

1. Plug your capture card into the aim PC via USB
2. Connect HDMI from the game PC's GPU output to the capture card
3. In CVM, set Capture Mode to `CaptureCard` or `CaptureCardGStreamer`
4. Set resolution to match your game output (e.g. 1920x1080)
5. Click CONNECT

If `CaptureCard` does not detect your device, try `CaptureCardGStreamer` (requires GStreamer installed).

**Installing GStreamer on macOS:**
```bash
brew install gstreamer
```

**Installing GStreamer on Windows:**
Download from https://gstreamer.freedesktop.org/download/ (MSVC 64-bit runtime)

### MSS (screen capture, single-PC)

1. Set Capture Mode to `MSS`
2. Pick your monitor index (1 = primary)
3. Set FOV X and FOV Y (how many pixels from center to capture, e.g. 320x320)
4. Click CONNECT

### NDI (network video)

1. On the game PC, use OBS with NDI output or NDI Tools
2. On the aim PC, set Capture Mode to `NDI`
3. Select the NDI source from the dropdown
4. Click CONNECT

Note: NDI (cyndilib) may not build on macOS. Use UDP or a capture card instead.

### UDP (OBS streaming)

1. In OBS on the game PC, set up a custom output to UDP
2. On the aim PC, set Capture Mode to `UDP`
3. Enter the IP and port
4. Click CONNECT

---

## Connecting Your Mouse Device

### MAKCU / Serial (most common)

MAKCU is a USB device that presents as a mouse/keyboard to the game PC. CVM sends serial commands to it.

1. Plug MAKCU into both PCs (USB to aim PC for serial, USB to game PC for HID output)
2. Set Mouse API to `Serial`
3. Port Mode: `Auto` scans for known VID/PIDs (MAKCU 1A86:55D3, CH343, CH340, etc.)
4. Port Mode: `Manual` lets you pick a specific COM port (Windows) or /dev/tty device (macOS)
5. Click CONNECT
6. Click **Test Move** to verify. Your game PC cursor should jump.

### Arduino

1. Upload the appropriate Arduino sketch to your board (handles serial mouse commands)
2. Set Mouse API to `Arduino`
3. Set the port and baud rate (default 115200)
4. Click CONNECT

### SendInput / Quartz (no hardware, single-PC)

- Windows: Set Mouse API to `SendInput`. No setup needed.
- macOS: Same setting. It automatically uses Quartz (CoreGraphics) instead. Needs Accessibility permissions.

### Other devices

- **Net**: Network mouse device. Enter IP, port, and UUID.
- **KmboxA**: Set VID/PID. Windows only (uses a DLL).
- **MakV2 / MakV2Binary**: Serial devices. Set port and baud (default 4Mbps).
- **DHZ**: Network device. Set IP and port.
- **Ferrum**: Serial device. Set device path.

---

## Tuning Color Detection

This is the most important step. Bad color settings = bad detection.

### How it works

CVM converts each frame to HSV color space, then filters for pixels matching your target color range. The remaining pixels are grouped into contours, which become detected "bodies."

### Using the HSV Preview

1. In the General tab, find the Custom HSV section
2. Set color to `custom`
3. Click **HSV Preview** to open the live preview window
4. You will see the raw frame and the filtered mask side by side

### Dialing in the color

- **H (Hue)**: The color itself. Yellow is around 20-40, purple around 120-160, red wraps around 0-10 and 170-179
- **S (Saturation)**: Color intensity. Set min to at least 50-80 to avoid picking up gray/white
- **V (Value)**: Brightness. Set min to 50-100 to avoid dark noise

Start wide, then narrow down:
1. Set a wide range that catches the target color
2. Look at the mask. White pixels = detected.
3. Narrow the range until only player outlines remain
4. Reduce noise with the detection parameters (min area, morph kernel sizes)

### Detection Parameters (General tab > Detection Parameters)

- **Min BBox Area**: Minimum bounding box area in pixels. Raise this to ignore tiny noise blobs. Default 150.
- **Open Kernel / Close Kernel**: Morphological operations. Open removes noise, Close fills gaps. Default 3/5.
- **Mask Blur**: Gaussian blur on the mask. Smooths edges. Default 3.
- **Min Contour Points**: Minimum points in a contour to be valid. Default 5.
- **Merge Distance**: How close detections must be to merge into one. Default 12.

---

## Configuring the Aimbot

### Aimbot Tab

- **Enable Aimbot**: Master toggle
- **Operation Mode**:
  - `Normal`: Standard aim correction. Good default.
  - `Silent`: Flicks to target, clicks, returns. For single shots.
  - `NCAF`: Near-center adaptive field. Stronger correction near crosshair, weaker far away.
  - `WindMouse`: Human-like curved mouse movement. Looks more natural.
  - `Bezier`: Bezier curve interpolation for smooth paths.

### Key settings

- **X Speed / Y Speed**: How fast the aim corrects horizontally/vertically. Higher = faster snap. Start at 2-3.
- **Smooth**: Smoothing factor. Higher = slower, more gradual correction. Start at 20-30.
- **Smooth FOV**: Inner radius where smoothing kicks in harder. Prevents overshooting near the target.
- **FOV Size**: How far from center (in pixels) to look for targets. 100-200 is typical.
- **ADS FOV**: Separate FOV when aiming down sights. Enable and set smaller than main FOV for tighter aim while scoped.
- **Aim Type**: `head` (aim at estimated head position), `body` (center mass), `nearest` (closest point on body)

### Activation

- **Activation Type**: `hold_enable` means hold a button to activate. `toggle` means press once on, press again off.
- **Mouse Button**: Which button activates aiming (1=left, 2=right, 3=side buttons)

### Secondary Aimbot (Sec Aimbot tab)

A second aimbot with independent settings. Useful for having different configs for hip-fire vs ADS, or different buttons for different behaviors.

---

## Configuring the Triggerbot

The Triggerbot tab controls automatic firing when a target is under your crosshair.

- **Enable Triggerbot**: Master toggle
- **Trigger FOV**: Radius around crosshair center. Only fires when a target is within this. Keep small (5-15).
- **Delay Min/Max**: Random delay before firing (seconds). Adds human-like reaction time. 0.08-0.15 is typical.
- **Hold Min/Max**: How long to hold the click (milliseconds). 40-60 is typical.
- **Cooldown Min/Max**: Minimum time between trigger activations. Prevents spam.
- **Burst Count**: How many clicks per activation. 1 for single fire, 2-3 for burst.
- **Burst Interval**: Delay between burst clicks.
- **ROI Size**: Size of the region checked for target pixels. Default 8.
- **Min Pixels / Min Ratio**: How many target-colored pixels must be in the ROI to trigger. Prevents false fires.
- **Confirm Frames**: How many consecutive frames must confirm before firing. 2 is default. Raise to reduce false triggers.

### Trigger Activation

- **Activation Type**: `hold_enable` = hold a button to allow triggering. The trigger fires automatically within that hold.
- **Button**: Which button enables the triggerbot.

---

## RCS (Recoil Control)

The RCS tab handles automatic recoil compensation. When firing, it pulls the mouse down to counteract weapon recoil.

- **Enable RCS**: Master toggle
- **Pull Speed**: How fast to pull down (pixels per tick). Start at 10.
- **Activation Delay**: Milliseconds after clicking before RCS kicks in. 100ms default.
- **Rapid Click Threshold**: If clicks happen faster than this (ms), treat as full-auto spray. 200ms default.

---

## Saving and Loading Configs

### Config Tab

- **Save**: Saves current settings to a named profile in the `configs/` folder
- **Load**: Loads a saved profile
- **Default**: Resets to default settings

Settings auto-save to `config.json` as you change them. Named profiles let you keep separate configs for different games or setups.

---

## Troubleshooting

### "No frame" or black Detection window
- Check your capture card is plugged in and the game PC is outputting video
- Try a different Capture Mode (switch between CaptureCard and CaptureCardGStreamer)
- For MSS, make sure the correct monitor index is selected

### Mouse not moving on game PC
- Check the serial connection (correct COM port, MAKCU plugged in)
- Click Test Move in the Hardware API section
- For MAKCU: try Auto port mode first
- On macOS with SendInput/Quartz: check Accessibility permissions

### Detection picking up wrong things
- Narrow your HSV range using the HSV Preview
- Raise Min BBox Area to filter noise
- Raise Min Contour Points
- Enable Anti-Smoke Detection if smoke grenades cause false targets

### Aim is jerky or overshoots
- Increase Smooth value (try 30-50)
- Decrease X/Y Speed (try 1-2)
- Increase Smooth FOV
- Enable Target Temporal Smoothing in General settings

### Aim is too slow
- Decrease Smooth value
- Increase X/Y Speed
- Decrease Smooth FOV

### GStreamer not found (macOS)
```bash
brew install gstreamer
```

### GStreamer not found (Windows)
Download and install the MSVC x86_64 runtime from https://gstreamer.freedesktop.org/download/

---

## macOS-Specific Notes

### What works on macOS
- MSS screen capture
- Capture card via OpenCV
- Capture card via GStreamer (with brew install)
- UDP video input
- Serial mouse devices (MAKCU, Arduino, MakV2, etc.)
- Quartz mouse/keyboard input (replaces Windows SendInput)
- The full UI (CustomTkinter is cross-platform)

### What does not work on macOS
- KmboxA (requires a Windows DLL)
- NDI via cyndilib (may fail to build; use NDI Tools + UDP as a workaround)
- Net mouse backend DLL (the .pyd files are Windows-only)

### Serial ports on macOS
On macOS, serial devices appear as `/dev/tty.usbserial-XXXX` or `/dev/tty.usbmodemXXXX`. Set Serial Port Mode to Manual and enter the path, or use Auto and it will scan for known VID/PIDs.

To find your device:
```bash
ls /dev/tty.usb*
```

---

## What Changed From the Original

This fork adds macOS compatibility on top of the original Windows codebase by [asenyeroao-ct](https://github.com/asenyeroao-ct).

| File | Change |
|------|--------|
| `setup.sh` / `run.sh` | Shell equivalents of the .bat scripts |
| `requirements_macos.txt` | Drops cyndilib, adds pyobjc-framework-Quartz |
| `src/utils/mouse/QuartzInputAPI.py` | macOS mouse/keyboard backend via CoreGraphics |
| `src/utils/mouse/SendInputAPI.py` | Auto-delegates to Quartz on macOS |
| `main.py` | Skips Windows-only ctypes.windll calls on macOS |
| `src/capture/capture_service.py` | GStreamer detection supports macOS dylib paths |
| `README_MACOS.md` | This file |

The original Windows functionality is completely preserved. All original files and commit history are intact.
