"""
========================================================================================================================
Name: action.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtGui


    class QAction(QtGui.QAction):
        """QAction"""

        def __init__(self, *args) -> None:
            super(QAction, self).__init__(*args)
except ImportError:
    from PySide2 import QtWidgets


    class QAction(QtWidgets.QAction):
        """QAction"""

        def __init__(self, *args) -> None:
            super(QAction, self).__init__(*args)
