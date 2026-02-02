"""Configuration management for Faker."""

import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "faker"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_CONFIG = {
    "method": "keyboard",
    "interval_seconds": 60,
    "enabled": False,
    "keyboard": {
        "key": "F15",
    },
    "mouse": {
        "mode": "fixed",
        "pixels": 1,
    },
    "ui": {
        "dark_mode": False,
    },
}


def _deep_merge(base: dict, overlay: dict) -> None:
    """Recursively merge overlay into base dict."""
    for key, value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def load_config() -> dict:
    """Load configuration from disk, merging with defaults for any missing keys."""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        merged = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
        _deep_merge(merged, config)
        return merged
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """Save configuration to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
