"""
========================================================================================================================
Name: check_box.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-05-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

import maurice_texture_connector.ui.maurice_qt.widgets_styles as widgets_styles


class QCheckBox(QtWidgets.QCheckBox):
    """QCheckBox."""

    def __init__(self, *args):
        """Initializes class attributes."""
        super(QCheckBox, self).__init__(*args)

        # QCheckBox settings.
        self.setStyleSheet(widgets_styles.check_box_style())
