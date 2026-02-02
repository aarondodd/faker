"""Options dialog for Faker configuration."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QRadioButton,
    QPushButton,
    QSpinBox,
    QComboBox,
    QButtonGroup,
)
from PyQt6.QtCore import Qt

from .methods import METHODS
from .utils.theme import ThemeManager


class OptionsDialog(QDialog):
    """Dialog for configuring Faker activity simulation options."""

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Faker Options")
        self.setMinimumWidth(400)
        self.setModal(True)

        self._config = config

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)

        # -- General section --
        general_group = QGroupBox("General")
        general_layout = QHBoxLayout()
        general_layout.addWidget(QLabel("Interval:"))
        self._interval_spin = QSpinBox()
        self._interval_spin.setRange(1, 3600)
        self._interval_spin.setSuffix(" seconds")
        self._interval_spin.setValue(config.get("interval_seconds", 60))
        general_layout.addWidget(self._interval_spin)
        general_layout.addStretch()
        general_group.setLayout(general_layout)
        main_layout.addWidget(general_group)

        # -- Activity Method section --
        method_group = QGroupBox("Activity Method")
        method_layout = QVBoxLayout()
        self._method_button_group = QButtonGroup(self)

        current_method = config.get("method", "keyboard")
        for i, (method_id, info) in enumerate(METHODS.items()):
            radio = QRadioButton(info["label"])
            radio.setToolTip(info["description"])
            radio.setProperty("method_id", method_id)
            self._method_button_group.addButton(radio, i)
            method_layout.addWidget(radio)

            # Description label (smaller, dimmed)
            desc = QLabel(info["description"])
            desc.setWordWrap(True)
            desc.setStyleSheet("font-size: 11px; color: #888888; margin-left: 22px;")
            method_layout.addWidget(desc)

            if method_id == current_method:
                radio.setChecked(True)

        method_group.setLayout(method_layout)
        main_layout.addWidget(method_group)

        # -- Keyboard Options section --
        self._keyboard_group = QGroupBox("Keyboard Options")
        kb_layout = QHBoxLayout()
        kb_layout.addWidget(QLabel("Key:"))
        self._key_combo = QComboBox()
        self._key_combo.setEditable(True)
        self._key_combo.addItems([
            "F13", "F14", "F15", "F16", "F17", "F18", "F19", "F20",
        ])
        current_key = config.get("keyboard", {}).get("key", "F15")
        self._key_combo.setCurrentText(current_key)
        kb_layout.addWidget(self._key_combo)
        kb_layout.addStretch()
        self._keyboard_group.setLayout(kb_layout)
        main_layout.addWidget(self._keyboard_group)

        # -- Mouse Options section --
        self._mouse_group = QGroupBox("Mouse Options")
        mouse_layout = QVBoxLayout()

        self._mouse_mode_group = QButtonGroup(self)
        mouse_mode = config.get("mouse", {}).get("mode", "fixed")

        # Fixed offset option with pixels spinner
        fixed_row = QHBoxLayout()
        self._mouse_fixed_radio = QRadioButton("Fixed offset")
        self._mouse_mode_group.addButton(self._mouse_fixed_radio, 0)
        fixed_row.addWidget(self._mouse_fixed_radio)
        fixed_row.addWidget(QLabel("Pixels:"))
        self._pixels_spin = QSpinBox()
        self._pixels_spin.setRange(1, 100)
        self._pixels_spin.setValue(config.get("mouse", {}).get("pixels", 1))
        fixed_row.addWidget(self._pixels_spin)
        fixed_row.addStretch()
        mouse_layout.addLayout(fixed_row)

        # Random option
        self._mouse_random_radio = QRadioButton("Random movement")
        self._mouse_mode_group.addButton(self._mouse_random_radio, 1)
        mouse_layout.addWidget(self._mouse_random_radio)

        if mouse_mode == "random":
            self._mouse_random_radio.setChecked(True)
        else:
            self._mouse_fixed_radio.setChecked(True)

        self._mouse_group.setLayout(mouse_layout)
        main_layout.addWidget(self._mouse_group)

        main_layout.addStretch()

        # -- Buttons --
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(ThemeManager.accent_button_style())
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)

        main_layout.addLayout(button_layout)

        # Connect method change to show/hide options
        self._method_button_group.buttonClicked.connect(self._on_method_changed)
        self._on_method_changed()

        # Connect mouse mode to enable/disable pixels spinner
        self._mouse_fixed_radio.toggled.connect(self._on_mouse_mode_changed)
        self._on_mouse_mode_changed()

    def _on_method_changed(self, _btn=None):
        """Show/hide method-specific option groups."""
        method = self._get_selected_method()
        self._keyboard_group.setVisible(method == "keyboard")
        self._mouse_group.setVisible(method == "mouse")

    def _on_mouse_mode_changed(self):
        """Enable/disable pixels spinner based on mouse mode."""
        self._pixels_spin.setEnabled(self._mouse_fixed_radio.isChecked())

    def _get_selected_method(self) -> str:
        """Return the ID of the currently selected method."""
        btn = self._method_button_group.checkedButton()
        if btn:
            return btn.property("method_id")
        return "keyboard"

    def get_config(self) -> dict:
        """Build and return the updated configuration dict."""
        config = dict(self._config)
        config["method"] = self._get_selected_method()
        config["interval_seconds"] = self._interval_spin.value()
        config["keyboard"] = {
            "key": self._key_combo.currentText().strip() or "F15",
        }
        config["mouse"] = {
            "mode": "random" if self._mouse_random_radio.isChecked() else "fixed",
            "pixels": self._pixels_spin.value(),
        }
        return config
