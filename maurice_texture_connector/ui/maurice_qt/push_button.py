"""
========================================================================================================================
Name: push_button.py
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
import maurice_texture_connector.utils as maurice_utils


class QPushButton(QtWidgets.QPushButton):
    """QPushButton."""
    ICON_SIZE = maurice_utils.get_value_by_ppi(16, 24)
    ICON_SMALL_SIZE = maurice_utils.get_value_by_ppi(12, 24)

    clicked_and_alt = QtCore.Signal()
    clicked_and_ctrl = QtCore.Signal()

    def __init__(self, *args):
        """Initializes class attributes."""
        super(QPushButton, self).__init__(*args)

        self.maurice_widgets_style = MauriceWidgetsStyle()

        # QPushButton settings.
        self.setFixedHeight(maurice_utils.get_value_by_ppi(26, 40))
        self.setIconSize(QtCore.QSize(QPushButton.ICON_SIZE, QPushButton.ICON_SIZE))
        self.setStyleSheet(self.maurice_widgets_style.push_button())

    def set_small_push_button_size(self) -> None:
        """Sets small push button size."""
        self.setFixedSize(
            self.maurice_widgets_style.HEIGHT,
            self.maurice_widgets_style.HEIGHT)
        self.setIconSize(QtCore.QSize(QPushButton.ICON_SMALL_SIZE, QPushButton.ICON_SMALL_SIZE))

    def set_transparent_background(self) -> None:
        """Sets transparent background."""
        style = f'''
            QPushButton {{
                background-color: transparent;
                border: 0px;}}

            QPushButton:hover {{
                border: 0px;}}

            QToolTip {{
            background-color: rgb(45, 45, 45);
            color: white; 
            border: 1px solid {self.maurice_widgets_style.COLOR_GOLD_YELLOW};}}
        '''

        self.setStyleSheet(style)

    def set_yellow_background(self) -> None:
        """Sets yellow background."""
        style = f'QPushButton {{background-color: {self.maurice_widgets_style.COLOR_GOLD_YELLOW};}}'

        self.setStyleSheet(self.maurice_widgets_style.push_button() + style)

    def setToolTip(self, lmb: str, alt_lmb: str = '', ctrl_lmb: str = '', title: str = ''):
        """Sets tool tip."""
        alt_lmb = alt_lmb.capitalize()
        ctrl_lmb = ctrl_lmb.capitalize()
        lmb = lmb.capitalize()

        if alt_lmb:
            alt_lmb = f'<br><br><b>Alt + LMB:</b> {alt_lmb}'

        if ctrl_lmb:
            ctrl_lmb = f'<br><br><b>Ctrl + LMB:</b> {ctrl_lmb}'

        title = title.title() if title else lmb.title()

        super(QPushButton, self).setToolTip(f'<b>{title}</b><br><br><b>LMB:</b> {lmb}{alt_lmb}{ctrl_lmb}')
