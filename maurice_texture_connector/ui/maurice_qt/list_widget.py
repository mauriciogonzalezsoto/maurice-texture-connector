"""
========================================================================================================================
Name: list_widget.py
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


class QListWidget(QtWidgets.QListWidget):
    """QListWidget."""

    def __init__(self, *args) -> None:
        """Initializes class attributes."""
        super(QListWidget, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QListWidget settings.
        self.setStyleSheet(maurice_widgets_style.list_widget())
        self.setFocusPolicy(QtCore.Qt.NoFocus)
