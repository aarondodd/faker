#!/usr/bin/env python3
"""Faker - System tray application to simulate user activity."""

import sys
from PyQt6.QtWidgets import QApplication
from faker_app.app import FakerApp


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Faker")
    app.setOrganizationName("Faker")
    app.setQuitOnLastWindowClosed(False)

    faker = FakerApp()  # noqa: F841 - must keep reference alive

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
