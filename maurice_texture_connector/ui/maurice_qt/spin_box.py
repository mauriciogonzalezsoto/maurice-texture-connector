"""
========================================================================================================================
Name: spin_box.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-10-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

from maurice_texture_connector.ui.maurice_qt.maurice_widgets_styles import MauriceWidgetsStyle


class QSpinBox(QtWidgets.QSpinBox):
    """QSpinBox."""

    def __init__(self, *args):
        """Initializes class attributes."""
        super(QSpinBox, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QSpinBox settings.
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setFixedSize(maurice_widgets_style.WIDTH, maurice_widgets_style.HEIGHT)
        self.setStyleSheet(maurice_widgets_style.spin_box())

    def contextMenuEvent(self, event):
        """Context menu event."""
        event.ignore()
