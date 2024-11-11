"""
========================================================================================================================
Name: dialog_maya.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from shiboken6 import wrapInstance
    from PySide6 import QtWidgets
    from PySide6 import QtCore
    from PySide6 import QtGui
except ImportError:
    from shiboken2 import wrapInstance
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui

import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui

from maurice_texture_connector.ui.maurice_qt.dialog import QDialog


def maya_main_window() -> QtWidgets.QWidget:
    """Gets the Maya main window widget as a Python object."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

    return main_window


class QDialogMaya(QDialog):
    """QDialog Maya."""
    def __init__(self, parent: QtWidgets.QWidget = maya_main_window()) -> None:
        super(QDialogMaya, self).__init__(parent)

        # Script jobs class variables.
        self.script_jobs = []

        # Call backs class variables.
        self.call_backs = []

    def create_call_backs(self) -> None:
        """Creates the call-backs."""
        pass

    def delete_call_backs(self) -> None:
        """Deletes the call-backs."""
        for call_back in self.call_backs:
            om.MSceneMessage.removeCallback(call_back)

        self.call_backs.clear()

    def create_script_jobs(self) -> None:
        """Creates the script jobs."""
        pass

    def delete_script_jobs(self) -> None:
        """Deletes the script jobs."""
        for job_number in self.script_jobs:
            cmds.scriptJob(kill=job_number)

        self.script_jobs.clear()

    def closeEvent(self, event: any) -> None:
        """Close event."""
        super(QDialogMaya, self).closeEvent(event)

        self.delete_call_backs()
        self.delete_script_jobs()

    def showEvent(self, event: any) -> None:
        """Show event."""
        super(QDialogMaya, self).showEvent(event)

        self.create_call_backs()
        self.create_script_jobs()
