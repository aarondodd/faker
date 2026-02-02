"""Main application with system tray for Faker."""

from PyQt6.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QApplication,
    QMessageBox,
)
from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtGui import QAction

from .methods import (
    send_key,
    move_mouse_fixed,
    move_mouse_random,
    toggle_scroll_lock,
    reset_idle_timer,
    check_requirements,
    METHODS,
)
from .options import OptionsDialog
from .utils.config import load_config, save_config
from .utils.icon import generate_tray_icon
from .utils.theme import ThemeManager


class FakerApp(QObject):
    """System tray application for simulating user activity."""

    def __init__(self):
        super().__init__()

        self._config = load_config()
        self._active = False
        self._dark_mode = self._config.get("ui", {}).get("dark_mode", False)

        ThemeManager.apply(self._dark_mode)

        self._setup_tray()
        self._setup_timer()

        self._update_tooltip()

        # Auto-start if previously enabled
        if self._config.get("enabled", False):
            self._start()

    def _setup_tray(self):
        """Set up the system tray icon and context menu."""
        self.tray_icon = QSystemTrayIcon()
        self._update_tray_icon()

        tray_menu = QMenu()

        self._toggle_action = QAction("Start", self)
        self._toggle_action.triggered.connect(self._toggle)
        tray_menu.addAction(self._toggle_action)

        tray_menu.addSeparator()

        options_action = QAction("Options...", self)
        options_action.triggered.connect(self._show_options)
        tray_menu.addAction(options_action)

        dark_mode_text = "Light Mode" if self._dark_mode else "Dark Mode"
        self._dark_mode_action = QAction(dark_mode_text, self)
        self._dark_mode_action.triggered.connect(self._toggle_dark_mode)
        tray_menu.addAction(self._dark_mode_action)

        tray_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self._exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def _setup_timer(self):
        """Set up the activity trigger timer."""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._trigger_activity)

    def _toggle(self):
        """Toggle between active and paused states."""
        if self._active:
            self._stop()
        else:
            self._start()

    def _start(self):
        """Start simulating activity."""
        method = self._config.get("method", "keyboard")
        error = check_requirements(method)
        if error:
            self.tray_icon.showMessage(
                "Faker",
                error,
                QSystemTrayIcon.MessageIcon.Warning,
                5000,
            )
            return

        self._active = True
        interval_ms = self._config.get("interval_seconds", 60) * 1000
        self._timer.start(interval_ms)
        self._toggle_action.setText("Pause")
        self._update_tray_icon()
        self._update_tooltip()

        self._config["enabled"] = True
        save_config(self._config)

    def _stop(self):
        """Stop simulating activity."""
        self._active = False
        self._timer.stop()
        self._toggle_action.setText("Start")
        self._update_tray_icon()
        self._update_tooltip()

        self._config["enabled"] = False
        save_config(self._config)

    def _trigger_activity(self):
        """Execute the configured activity simulation method."""
        method = self._config.get("method", "keyboard")

        if method == "keyboard":
            key = self._config.get("keyboard", {}).get("key", "F15")
            send_key(key)
        elif method == "mouse":
            mode = self._config.get("mouse", {}).get("mode", "fixed")
            if mode == "random":
                move_mouse_random()
            else:
                pixels = self._config.get("mouse", {}).get("pixels", 1)
                move_mouse_fixed(pixels)
        elif method == "scroll_lock":
            toggle_scroll_lock()
        elif method == "idle_reset":
            reset_idle_timer()

    def _show_options(self):
        """Show the options dialog."""
        was_active = self._active
        if was_active:
            self._stop()

        dialog = OptionsDialog(self._config)
        if dialog.exec():
            self._config = dialog.get_config()
            # Preserve UI and enabled state
            self._config.setdefault("ui", {})["dark_mode"] = self._dark_mode
            save_config(self._config)
            self._update_tooltip()

        if was_active:
            self._start()

    def _toggle_dark_mode(self):
        """Toggle between dark and light mode."""
        self._dark_mode = not self._dark_mode
        ThemeManager.apply(self._dark_mode)
        self._update_tray_icon()

        self._dark_mode_action.setText(
            "Light Mode" if self._dark_mode else "Dark Mode"
        )

        self._config.setdefault("ui", {})["dark_mode"] = self._dark_mode
        save_config(self._config)

    def _update_tray_icon(self):
        """Update the tray icon to reflect the current state."""
        icon = generate_tray_icon(
            active=self._active,
            dark_mode=self._dark_mode,
        )
        self.tray_icon.setIcon(icon)

    def _update_tooltip(self):
        """Update the tray icon tooltip with current status."""
        if self._active:
            method = self._config.get("method", "keyboard")
            label = METHODS.get(method, {}).get("label", method)
            interval = self._config.get("interval_seconds", 60)
            self.tray_icon.setToolTip(
                f"Faker - Active\n{label} every {interval}s"
            )
        else:
            self.tray_icon.setToolTip("Faker - Paused")

    def _exit_app(self):
        """Exit the application."""
        self.tray_icon.hide()
        QApplication.instance().quit()
