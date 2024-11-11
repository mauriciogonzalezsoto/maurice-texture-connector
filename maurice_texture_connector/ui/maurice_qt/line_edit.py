"""
========================================================================================================================
Name: line_edit.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtWidgets
    from PySide6 import QtGui
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtGui

from maurice_texture_connector.ui.maurice_qt.maurice_widgets_styles import MauriceWidgetsStyle


class QLineEdit(QtWidgets.QLineEdit):
    """QLineEdit."""

    def __init__(self, *args) -> None:
        """Initializes class attributes."""
        super(QLineEdit, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QLineEdit settings.
        self.setFixedHeight(maurice_widgets_style.HEIGHT)
        self.setStyleSheet(maurice_widgets_style.line_edit())

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        """Context menu event."""
        event.ignore()
