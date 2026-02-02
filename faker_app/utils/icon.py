"""Icon generation for Faker system tray."""

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor, QIcon, QPen


def generate_tray_icon(
    active: bool = False,
    dark_mode: bool = False,
    size: int = 64,
) -> QIcon:
    """Generate the system tray icon programmatically.

    The icon is a square with "F" centered as large as feasible.
    Background is colored green when active, transparent when paused.
    Border and text color are chosen to be readable on the taskbar.

    Args:
        active: Whether activity simulation is currently running.
        dark_mode: Whether the OS is in dark mode.
        size: Icon size in pixels.

    Returns:
        QIcon ready for use as a system tray icon.
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    margin = max(1, size // 16)
    rect = QRect(margin, margin, size - 2 * margin, size - 2 * margin)

    if active:
        bg_color = QColor("#4caf50")  # Material green
        fg_color = QColor("#ffffff")
    else:
        bg_color = QColor(Qt.GlobalColor.transparent)
        fg_color = QColor("#ffffff") if dark_mode else QColor("#000000")

    # Draw background if active
    if active:
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, size // 8, size // 8)

    # Draw border
    pen_width = max(1, size // 16)
    pen = QPen(fg_color, pen_width)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRoundedRect(rect, size // 8, size // 8)

    # Draw "F" text centered, as large as feasible
    font_size = max(1, size * 3 // 8)
    font = QFont("Arial", font_size, QFont.Weight.Bold)
    painter.setFont(font)
    painter.setPen(fg_color)
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "F")

    painter.end()

    return QIcon(pixmap)
