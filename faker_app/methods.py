"""Activity simulation methods.

Cross-platform support:
  - Linux: uses xdotool for input simulation, xdg-screensaver for idle reset.
    System requirement: xdotool (sudo apt install xdotool)
  - Windows: uses SendInput via ctypes for input, SetThreadExecutionState
    for idle reset. No external tools required.
"""

import random
import shutil
import subprocess
import sys

IS_WINDOWS = sys.platform == "win32"


# ── Windows backend (ctypes) ─────────────────────────────────

if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    # Input event type constants
    _INPUT_MOUSE = 0
    _INPUT_KEYBOARD = 1

    # Key event flags
    _KEYEVENTF_KEYUP = 0x0002

    # Mouse event flags
    _MOUSEEVENTF_MOVE = 0x0001

    # SetThreadExecutionState flags
    _ES_SYSTEM_REQUIRED = 0x00000001
    _ES_DISPLAY_REQUIRED = 0x00000002

    # Virtual key code mapping from config key names
    _VK_MAP = {
        "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73,
        "F5": 0x74, "F6": 0x75, "F7": 0x76, "F8": 0x77,
        "F9": 0x78, "F10": 0x79, "F11": 0x7A, "F12": 0x7B,
        "F13": 0x7C, "F14": 0x7D, "F15": 0x7E, "F16": 0x7F,
        "F17": 0x80, "F18": 0x81, "F19": 0x82, "F20": 0x83,
        "F21": 0x84, "F22": 0x85, "F23": 0x86, "F24": 0x87,
        "Scroll_Lock": 0x91,
        "Num_Lock": 0x90,
    }

    class _KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ("wVk", wintypes.WORD),
            ("wScan", wintypes.WORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ]

    class _MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ("dx", wintypes.LONG),
            ("dy", wintypes.LONG),
            ("mouseData", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        ]

    class _HARDWAREINPUT(ctypes.Structure):
        _fields_ = [
            ("uMsg", wintypes.DWORD),
            ("wParamL", wintypes.WORD),
            ("wParamH", wintypes.WORD),
        ]

    class _INPUT_UNION(ctypes.Union):
        _fields_ = [
            ("mi", _MOUSEINPUT),
            ("ki", _KEYBDINPUT),
            ("hi", _HARDWAREINPUT),
        ]

    class _INPUT(ctypes.Structure):
        _fields_ = [
            ("type", wintypes.DWORD),
            ("union", _INPUT_UNION),
        ]

    def _win_send_input(*inputs):
        n = len(inputs)
        arr = (_INPUT * n)(*inputs)
        return user32.SendInput(n, arr, ctypes.sizeof(_INPUT))

    def _win_key_press(vk: int) -> bool:
        """Send a key down + key up via SendInput."""
        down = _INPUT()
        down.type = _INPUT_KEYBOARD
        down.union.ki.wVk = vk

        up = _INPUT()
        up.type = _INPUT_KEYBOARD
        up.union.ki.wVk = vk
        up.union.ki.dwFlags = _KEYEVENTF_KEYUP

        return _win_send_input(down, up) == 2

    def _win_mouse_move(dx: int, dy: int) -> bool:
        """Send a relative mouse move via SendInput."""
        move = _INPUT()
        move.type = _INPUT_MOUSE
        move.union.mi.dx = dx
        move.union.mi.dy = dy
        move.union.mi.dwFlags = _MOUSEEVENTF_MOVE

        return _win_send_input(move) == 1


# ── Linux backend (xdotool / xdg-screensaver) ────────────────

def _run(args: list[str]) -> bool:
    """Run a subprocess command, returning True on success."""
    try:
        subprocess.run(
            args,
            check=True,
            capture_output=True,
            timeout=5,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


# ── Tool availability checks ─────────────────────────────────

def check_requirements(method: str) -> str | None:
    """Check if the required tools are available for a method.

    Returns None if everything is available, or an error message string
    describing what is missing.
    """
    if IS_WINDOWS:
        return None  # ctypes always available

    if method in ("keyboard", "mouse", "scroll_lock"):
        if not shutil.which("xdotool"):
            return (
                "xdotool is required but not installed.\n"
                "Install it with: sudo apt install xdotool"
            )
    elif method == "idle_reset":
        if not shutil.which("xdg-screensaver"):
            return (
                "xdg-screensaver is required but not found.\n"
                "Install it with: sudo apt install xdg-utils"
            )
    return None


# ── Public API (cross-platform) ───────────────────────────────

def send_key(key: str = "F15") -> bool:
    """Simulate a key press and release.

    Args:
        key: Key name (e.g. F15, F13, Scroll_Lock).
             On Linux these are X11 key names passed to xdotool.
             On Windows they are mapped to virtual key codes.
    """
    if IS_WINDOWS:
        vk = _VK_MAP.get(key)
        if vk is None:
            return False
        return _win_key_press(vk)
    return _run(["xdotool", "key", key])


def move_mouse_fixed(pixels: int = 1) -> bool:
    """Move mouse by a fixed offset then back.

    Moves right by N pixels, then immediately back left by N pixels,
    so the cursor ends up in the same position.
    """
    if IS_WINDOWS:
        ok = _win_mouse_move(pixels, 0)
        if ok:
            ok = _win_mouse_move(-pixels, 0)
        return ok
    ok = _run(["xdotool", "mousemove_relative", "--", str(pixels), "0"])
    if ok:
        ok = _run(["xdotool", "mousemove_relative", "--", str(-pixels), "0"])
    return ok


def move_mouse_random() -> bool:
    """Move mouse by a small random offset.

    Moves the cursor by a random amount between -5 and +5 pixels
    in both X and Y directions.
    """
    x = random.randint(-5, 5)
    y = random.randint(-5, 5)
    if x == 0 and y == 0:
        x = 1
    if IS_WINDOWS:
        return _win_mouse_move(x, y)
    return _run(["xdotool", "mousemove_relative", "--", str(x), str(y)])


def toggle_scroll_lock() -> bool:
    """Toggle Scroll Lock on then off.

    Sends two Scroll_Lock key events so the state ends up unchanged.
    This is invisible to most applications but registers as user activity.
    """
    if IS_WINDOWS:
        ok = _win_key_press(_VK_MAP["Scroll_Lock"])
        if ok:
            ok = _win_key_press(_VK_MAP["Scroll_Lock"])
        return ok
    ok = _run(["xdotool", "key", "Scroll_Lock"])
    if ok:
        ok = _run(["xdotool", "key", "Scroll_Lock"])
    return ok


def reset_idle_timer() -> bool:
    """Reset the desktop idle timer.

    On Linux: calls 'xdg-screensaver reset' which resets the screensaver
    idle countdown on most desktop environments.

    On Windows: calls SetThreadExecutionState with ES_DISPLAY_REQUIRED
    and ES_SYSTEM_REQUIRED, which resets the idle timers for display
    sleep and system sleep.
    """
    if IS_WINDOWS:
        result = kernel32.SetThreadExecutionState(
            _ES_DISPLAY_REQUIRED | _ES_SYSTEM_REQUIRED
        )
        return result != 0
    return _run(["xdg-screensaver", "reset"])


# ── Method registry ───────────────────────────────────────────

METHODS = {
    "keyboard": {
        "label": "Keyboard Key Press",
        "description": "Sends a configurable key press (default: F15, "
                       "a key with no visible effect on most systems).",
        "has_options": True,
    },
    "mouse": {
        "label": "Mouse Jiggle",
        "description": "Moves the mouse pointer by a small amount to "
                       "simulate user activity.",
        "has_options": True,
    },
    "scroll_lock": {
        "label": "Scroll Lock Toggle",
        "description": "Toggles Scroll Lock on then off. Invisible to "
                       "most applications but counts as input activity.",
        "has_options": False,
    },
    "idle_reset": {
        "label": "Idle Timer Reset",
        "description": (
            "Resets the display and system sleep timers without "
            "simulating any actual input events. Uses "
            "SetThreadExecutionState on Windows, xdg-screensaver "
            "reset on Linux."
        ),
        "has_options": False,
    },
}
