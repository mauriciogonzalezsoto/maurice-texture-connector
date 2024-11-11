"""
========================================================================================================================
Name: h_box_layout.py
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


class QHBoxLayout(QtWidgets.QHBoxLayout):
    """QHBoxLayout."""

    def __init__(self, *args) -> None:
        """Initializes class attributes."""
        super(QHBoxLayout, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QHBoxLayout settings.
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(maurice_widgets_style.SPACING)
