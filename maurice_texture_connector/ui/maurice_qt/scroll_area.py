"""
========================================================================================================================
Name: scroll_area.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtWidgets
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore

from maurice_texture_connector.ui.maurice_qt.maurice_widgets_styles import MauriceWidgetsStyle


class QScrollArea(QtWidgets.QScrollArea):
    """QScrollArea."""

    def __init__(self, *args) -> None:
        """Initializes class attributes."""
        super(QScrollArea, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QScrollBar settings.
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setStyleSheet(maurice_widgets_style.scroll_area())
        self.setWidgetResizable(True)
