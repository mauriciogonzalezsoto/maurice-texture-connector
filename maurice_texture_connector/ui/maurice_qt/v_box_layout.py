"""
========================================================================================================================
Name: v_box_layout.py
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


class QVBoxLayout(QtWidgets.QVBoxLayout):
    """QVBoxLayout."""

    def __init__(self, *args):
        """Initializes class attributes."""
        super(QVBoxLayout, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QVBoxLayout settings.
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(maurice_widgets_style.SPACING)
