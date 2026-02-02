# Faker

A cross-platform system tray application that simulates user activity to prevent idle detection, screen locking, and display sleep. Built with Python and Qt6.

Faker lives entirely in the system tray — there is no main application window. All interaction happens through the tray icon's right-click context menu.

## Features

- **System tray only** — no window to manage, runs quietly in the background
- **Cross-platform** — works on both Linux (X11) and Windows
- **Multiple activity methods:**
  - **Keyboard Key Press** — sends a configurable key (default: F15, which has no visible effect on most systems)
  - **Mouse Jiggle** — moves the mouse pointer by a small amount (fixed offset that returns to position, or random movement)
  - **Scroll Lock Toggle** — toggles Scroll Lock on then off (invisible to most applications but registers as input)
  - **Idle Timer Reset** — resets the OS idle/sleep timer without simulating any input events (`SetThreadExecutionState` on Windows, `xdg-screensaver reset` on Linux)
- **Configurable interval** — set the time between triggers (1–3600 seconds, default: 60)
- **Dark/light theme** — uses the same color palette as [aws-sso-watcher](https://github.com/anthropics/aws-sso-watcher)
- **Persistent settings** — configuration saved to `~/.config/faker/settings.json`
- **Auto-resume** — remembers whether it was running and resumes on next launch

## Tray Icon

The tray icon is a bordered square containing the letter **F**.

| State | Appearance |
|-------|------------|
| Paused | Transparent background, themed border and text |
| Active | Green background (#4caf50), white text |

## Installation

### Prerequisites

- Python 3.10+
- **Linux only:** `xdotool` (for keyboard, mouse, and scroll lock methods)

  ```bash
  sudo apt install xdotool
  ```

### Setup

```bash
cd ~/repos/faker
python3 -m venv .venv
source .venv/bin/activate      # Linux
# .venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

### Run

```bash
source .venv/bin/activate
python main.py
```

### Build Standalone Executable

Build scripts create a single-file executable using PyInstaller and install it to `~/bin/`.

**Linux / macOS:**

```bash
./build.sh
```

**Windows (PowerShell):**

```powershell
.\build.ps1
```

After building, run the executable directly:

```bash
~/bin/faker          # Linux
%USERPROFILE%\bin\faker.exe   # Windows
```

## Usage

1. Launch the application — an **F** icon appears in the system tray.
2. **Right-click** the tray icon to open the context menu:
   - **Start / Pause** — toggle activity simulation on or off
   - **Options...** — open the configuration dialog
   - **Dark Mode / Light Mode** — toggle the UI theme
   - **Exit** — quit the application
3. In the **Options** dialog, choose an activity method and configure its parameters:
   - **Keyboard Key Press** — select the key from a dropdown (F13–F20) or type any X11 key name / Windows VK key name
   - **Mouse Jiggle** — choose between fixed offset (configurable pixel count, default 1) or random movement
   - **Scroll Lock Toggle** and **Idle Timer Reset** have no additional options beyond the interval

## Configuration

Settings are stored in `~/.config/faker/settings.json`:

```json
{
  "method": "keyboard",
  "interval_seconds": 60,
  "enabled": false,
  "keyboard": {
    "key": "F15"
  },
  "mouse": {
    "mode": "fixed",
    "pixels": 1
  },
  "ui": {
    "dark_mode": false
  }
}
```

## Platform Details

### Windows

All methods use the Win32 API via Python's `ctypes` — no external tools are required.

| Method | Implementation |
|--------|---------------|
| Keyboard | `SendInput` with virtual key codes |
| Mouse | `SendInput` with `MOUSEEVENTF_MOVE` |
| Scroll Lock | `SendInput` with `VK_SCROLL` (x2) |
| Idle Reset | `SetThreadExecutionState(ES_DISPLAY_REQUIRED \| ES_SYSTEM_REQUIRED)` |

### Linux

Input simulation methods require `xdotool` (X11). The idle reset method uses `xdg-screensaver` which is typically pre-installed.

| Method | Implementation |
|--------|---------------|
| Keyboard | `xdotool key <keyname>` |
| Mouse | `xdotool mousemove_relative` |
| Scroll Lock | `xdotool key Scroll_Lock` (x2) |
| Idle Reset | `xdg-screensaver reset` |

## Project Structure

```
faker/
├── main.py                      # Entry point
├── requirements.txt             # PyQt6
├── build.sh                     # Linux/macOS PyInstaller build
├── build.ps1                    # Windows PyInstaller build
├── faker.spec                   # PyInstaller spec file
└── faker_app/
    ├── __init__.py
    ├── version.py               # Version string
    ├── app.py                   # FakerApp — tray icon, timer, start/stop
    ├── methods.py               # Cross-platform activity simulation
    ├── options.py               # Options dialog
    └── utils/
        ├── __init__.py
        ├── config.py            # JSON config persistence
        ├── icon.py              # Tray icon generation (QPainter)
        └── theme.py             # Dark/light theme manager
```

## Dependencies

- [PyQt6](https://pypi.org/project/PyQt6/) >= 6.5.0
- **Linux only:** [xdotool](https://github.com/jordansissel/xdotool) (system package)
