"""
========================================================================================================================
Name: double_spin_box.py
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


class QDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    """QDoubleSpinBox."""

    def __init__(self, *args) -> None:
        """Initializes class attributes."""
        super(QDoubleSpinBox, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QDoubleSpinBox settings.
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setFixedSize(maurice_widgets_style.WIDTH, maurice_widgets_style.HEIGHT)
        self.setStyleSheet(maurice_widgets_style.double_spin_box())

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        """Context menu event."""
        event.ignore()
