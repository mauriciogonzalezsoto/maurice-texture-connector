"""
========================================================================================================================
Name: tree_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-10-2024

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


class QTreeWidget(QtWidgets.QTreeWidget):
    """QTreeWidget."""

    def __init__(self, *args):
        """Initializes class attributes."""
        super(QTreeWidget, self).__init__(*args)

        maurice_widgets_style = MauriceWidgetsStyle()

        # QTreeWidget settings.
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setHeaderHidden(True)
        self.setStyleSheet(maurice_widgets_style.tree_widget())
