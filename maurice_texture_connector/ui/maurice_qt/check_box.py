"""
========================================================================================================================
Name: check_box.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

from maurice_texture_connector.ui.maurice_qt.maurice_widgets_styles import MauriceWidgetsStyle


class QCheckBox(QtWidgets.QCheckBox):
    """QCheckBox."""

    def __init__(self, *args) -> None:
        """Initializes class attributes."""
        super(QCheckBox, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QCheckBox settings.
        self.setStyleSheet(maurice_widgets_style.check_box())
