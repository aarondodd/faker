"""Centralized theme management for Faker.

Adapted from AWS SSO Watcher's theme system, using the same color palette.
"""

from PyQt6.QtWidgets import QApplication


class ThemeManager:
    """Single source of truth for all application theming."""

    _dark_mode: bool = False

    # Dark palette
    _D_BG = "#1e1e1e"
    _D_BG_ALT = "#252526"
    _D_BG_RAISED = "#2d2d2d"
    _D_BG_INPUT = "#3c3c3c"
    _D_BG_HOVER = "#4c4c4c"
    _D_BORDER = "#3d3d3d"
    _D_FG = "#d4d4d4"
    _D_FG_DIM = "#888888"
    _D_SELECTION = "#264f78"
    _D_ACCENT = "#0078d4"

    # Light palette
    _L_BG = "#ffffff"
    _L_BG_ALT = "#f9f9f9"
    _L_BG_RAISED = "#f3f3f3"
    _L_BG_HOVER = "#e5e5e5"
    _L_BORDER = "#d4d4d4"
    _L_FG = "#1e1e1e"
    _L_FG_DIM = "#666666"
    _L_SELECTION = "#cce8ff"
    _L_ACCENT = "#0078d4"

    DARK_STYLESHEET = f"""
        QWidget {{
            background-color: {_D_BG};
            color: {_D_FG};
        }}
        QWidget:focus {{
            outline: none;
        }}
        QMenu {{
            background-color: {_D_BG_RAISED};
            color: {_D_FG};
            border: 1px solid {_D_BORDER};
        }}
        QMenu::item:selected {{
            background-color: {_D_ACCENT};
        }}
        QPushButton {{
            background-color: {_D_BG_INPUT};
            color: {_D_FG};
            border: 1px solid {_D_BORDER};
            padding: 6px 16px;
            border-radius: 3px;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {_D_BG_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {_D_BG_RAISED};
        }}
        QPushButton:disabled {{
            background-color: {_D_BG_RAISED};
            color: {_D_FG_DIM};
        }}
        QLabel {{
            color: {_D_FG};
            background: transparent;
        }}
        QGroupBox {{
            color: {_D_FG};
            border: 1px solid {_D_BORDER};
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
        }}
        QRadioButton {{
            color: {_D_FG};
            background: transparent;
            spacing: 6px;
        }}
        QRadioButton::indicator {{
            width: 14px;
            height: 14px;
        }}
        QSpinBox {{
            background-color: {_D_BG_INPUT};
            color: {_D_FG};
            border: 1px solid {_D_BORDER};
            padding: 4px 8px;
            border-radius: 3px;
        }}
        QComboBox {{
            background-color: {_D_BG_INPUT};
            color: {_D_FG};
            border: 1px solid {_D_BORDER};
            padding: 4px 8px;
            border-radius: 3px;
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {_D_BG_RAISED};
            color: {_D_FG};
            border: 1px solid {_D_BORDER};
            selection-background-color: {_D_ACCENT};
        }}
        QDialog {{
            background-color: {_D_BG};
            color: {_D_FG};
        }}
        QMessageBox {{
            background-color: {_D_BG_RAISED};
            color: {_D_FG};
        }}
        QCheckBox {{
            color: {_D_FG};
            background: transparent;
            spacing: 6px;
        }}
    """

    LIGHT_STYLESHEET = f"""
        QWidget {{
            background-color: {_L_BG};
            color: {_L_FG};
        }}
        QWidget:focus {{
            outline: none;
        }}
        QMenu {{
            background-color: {_L_BG};
            color: {_L_FG};
            border: 1px solid {_L_BORDER};
        }}
        QMenu::item:selected {{
            background-color: {_L_ACCENT};
            color: white;
        }}
        QPushButton {{
            background-color: {_L_BG_RAISED};
            color: {_L_FG};
            border: 1px solid {_L_BORDER};
            padding: 6px 16px;
            border-radius: 3px;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {_L_BG_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {_L_BORDER};
        }}
        QPushButton:disabled {{
            background-color: {_L_BG_RAISED};
            color: {_L_FG_DIM};
        }}
        QLabel {{
            color: {_L_FG};
            background: transparent;
        }}
        QGroupBox {{
            color: {_L_FG};
            border: 1px solid {_L_BORDER};
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 4px;
        }}
        QRadioButton {{
            color: {_L_FG};
            background: transparent;
            spacing: 6px;
        }}
        QRadioButton::indicator {{
            width: 14px;
            height: 14px;
        }}
        QSpinBox {{
            background-color: {_L_BG};
            color: {_L_FG};
            border: 1px solid {_L_BORDER};
            padding: 4px 8px;
            border-radius: 3px;
        }}
        QComboBox {{
            background-color: {_L_BG};
            color: {_L_FG};
            border: 1px solid {_L_BORDER};
            padding: 4px 8px;
            border-radius: 3px;
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {_L_BG};
            color: {_L_FG};
            border: 1px solid {_L_BORDER};
            selection-background-color: {_L_ACCENT};
            selection-color: #ffffff;
        }}
        QDialog {{
            background-color: {_L_BG};
            color: {_L_FG};
        }}
        QMessageBox {{
            background-color: {_L_BG};
            color: {_L_FG};
        }}
        QCheckBox {{
            color: {_L_FG};
            background: transparent;
            spacing: 6px;
        }}
    """

    @classmethod
    def apply(cls, dark: bool) -> None:
        """Apply the theme globally and store the current mode."""
        cls._dark_mode = dark
        app = QApplication.instance()
        if app:
            app.setStyleSheet(cls.DARK_STYLESHEET if dark else cls.LIGHT_STYLESHEET)

    @classmethod
    def is_dark_mode(cls) -> bool:
        return cls._dark_mode

    @classmethod
    def accent_button_style(cls) -> str:
        """Return QSS for accent-colored buttons (Save, etc.)."""
        accent = cls._D_ACCENT if cls._dark_mode else cls._L_ACCENT
        return (
            f"background-color: {accent}; "
            f"color: white; "
            f"border: none; "
            f"padding: 8px 24px; "
            f"border-radius: 4px; "
            f"font-size: 13px; "
            f"font-weight: bold;"
        )
