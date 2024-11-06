"""
========================================================================================================================
Name: texture_settings_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-05-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtWidgets
    from PySide6 import QtCore
    from PySide6 import QtGui
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui

import maya.cmds as cmds

import os

import maurice_texture_connector.ui.maurice_qt as maurice_qt
import maurice_texture_connector.utils as maurice_utils


class TextureSettingsWidget(QtWidgets.QWidget):
    """Texture settings widget."""
    edit_texture_clicked = QtCore.Signal()

    def __init__(self):
        """Initializes class attributes."""
        super(TextureSettingsWidget, self).__init__()

        # Files path class variables.
        self.icons = maurice_utils.get_icons()

        # Widget class variables.
        self.is_expanded = False

        # Main layout.
        self.main_layout = maurice_qt.QVBoxLayout()
        self.setLayout(self.main_layout)

        # Header class variables.
        self.texture_type_label = None
        self.texture_path_label = None
        self.texture_path_push_button = None
        self.expand_collapse_options_push_button = None

        # Options class variables.
        self.options_group_box = None
        self.texture_suffix_line_edit = None
        self.texture_color_space_line_edit = None

        # Creates the widgets.
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self) -> None:
        """Creates the widgets."""
        # ==============================================================================================================
        # Header.
        # ==============================================================================================================
        # Texture type QFont.
        texture_type_font = QtGui.QFont()
        texture_type_font.setBold(True)

        # Texture type QLabel.
        self.texture_type_label = maurice_qt.QLabel()
        self.texture_type_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.texture_type_label.setContentsMargins(maurice_qt.widgets_attributes.spacing * 3, 0, 0, 0)
        self.texture_type_label.setFixedWidth(maurice_utils.get_value_by_ppi(77, 104))
        self.texture_type_label.setFont(texture_type_font)

        # Texture path QLabel.
        self.texture_path_label = maurice_qt.QLabel()
        self.texture_path_label.setContentsMargins(maurice_utils.get_value_by_ppi(5, 7), 0, 0, 0)

        # Texture path QPushButton.
        self.texture_path_push_button = maurice_qt.QPushButton()
        self.texture_path_push_button.setIcon(QtGui.QIcon(self.icons['folder.png']))
        self.texture_path_push_button.setVisible(False)
        self.texture_path_push_button.set_small_push_button_size()
        self.texture_path_push_button.set_transparent_background()

        # Expand-collapse options QPushButton.
        self.expand_collapse_options_push_button = maurice_qt.QPushButton()
        self.expand_collapse_options_push_button.setFixedSize(QtCore.QSize(
            maurice_qt.widgets_attributes.height,
            maurice_qt.widgets_attributes.height))
        self.expand_collapse_options_push_button.setIcon(QtGui.QIcon(self.icons['caret-right.png']))
        self.expand_collapse_options_push_button.setIconSize(QtCore.QSize(
            maurice_qt.widgets_attributes.height,
            maurice_qt.widgets_attributes.height))
        self.expand_collapse_options_push_button.set_transparent_background()

        # ==============================================================================================================
        # Options.
        # ==============================================================================================================
        # Texture suffix QLineEdit.
        self.texture_suffix_line_edit = maurice_qt.QLineEdit()

        # Texture color space QLineEdit.
        self.texture_color_space_line_edit = maurice_qt.QLineEdit('')
        self.texture_color_space_line_edit.setReadOnly(True)

    def create_layout(self) -> None:
        """Creates the layouts."""
        # ==============================================================================================================
        # Header.
        # ==============================================================================================================
        # Header QGroupBox.
        header_group_box = QtWidgets.QGroupBox()
        header_group_box.setStyleSheet('''
            QGroupBox {
                background-color: rgb(45, 45, 45); 
                border-radius: %dpx;
                padding: %dpx;}''' % (
            maurice_qt.widgets_attributes.border_radius,
            maurice_qt.widgets_attributes.spacing))
        self.main_layout.addWidget(header_group_box)

        # Header QHBoxLayout.
        header_h_box_layout = maurice_qt.QHBoxLayout()
        header_h_box_layout.addWidget(self.expand_collapse_options_push_button)
        header_h_box_layout.addWidget(self.texture_type_label)
        header_h_box_layout.addWidget(self.texture_path_label)
        header_h_box_layout.addWidget(self.texture_path_push_button)
        header_group_box.setLayout(header_h_box_layout)

        # ==============================================================================================================
        # Options.
        # ==============================================================================================================
        # Options QVBoxLayout.
        options_v_box_layout = maurice_qt.QVBoxLayout()
        options_v_box_layout.setContentsMargins(
            maurice_qt.widgets_attributes.spacing,
            0,
            maurice_qt.widgets_attributes.spacing,
            0)
        self.main_layout.addLayout(options_v_box_layout)

        # Options QGroupBox.
        self.options_group_box = maurice_qt.QGroupBox()
        self.options_group_box.setVisible(False)
        options_v_box_layout.addWidget(self.options_group_box)

        # Options QFormLayout.
        options_form_layout = maurice_qt.QFormLayout()
        options_form_layout.add_row('Texture Suffix: ', self.texture_suffix_line_edit)
        options_form_layout.add_row('Color Space: ', self.texture_color_space_line_edit)
        options_form_layout.setContentsMargins(maurice_utils.get_value_by_ppi(22, 40), 0, 0, 0)
        self.options_group_box.setLayout(options_form_layout)

    def create_connections(self) -> None:
        """Creates the connections."""
        # ==============================================================================================================
        # Header.
        # ==============================================================================================================
        self.expand_collapse_options_push_button.clicked.connect(self.expand_collapse_options_clicked_push_button)

        # ==============================================================================================================
        # Options.
        # ==============================================================================================================
        self.texture_path_push_button.clicked.connect(self.texture_path_clicked_push_button)

    def expand_collapse_options_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'expand-collapse options' push button."""
        self.collapse() if self.is_expanded else self.expand()

    def texture_path_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'texture path' push button."""
        self.edit_texture_clicked.emit()

    def expand(self) -> None:
        """Expands the options."""
        self.is_expanded = True
        self.expand_collapse_options_push_button.setIcon(QtGui.QIcon(self.icons['caret-down.png']))

        self.options_group_box.setVisible(True)

    def collapse(self) -> None:
        """Collapses the options."""
        self.is_expanded = False
        self.expand_collapse_options_push_button.setIcon(QtGui.QIcon(self.icons['caret-right.png']))

        self.options_group_box.setVisible(False)

    def clear_texture_info(self) -> None:
        """Clears the texture info."""
        self.texture_path_label.setText('')
        self.texture_path_label.setStyleSheet(maurice_qt.label_style() + 'QLabel {color: #ffffff}')

        self.texture_path_push_button.setVisible(False)

        self.texture_color_space_line_edit.setText('')

    def get_texture_suffix(self) -> str:
        """Gets the texture suffix."""
        return self.texture_suffix_line_edit.text()

    def set_texture_color_space(self, color_space: str) -> None:
        """Sets the texture color space."""
        self.texture_color_space_line_edit.setText(color_space)

    def set_texture_path(self, texture_path: str) -> None:
        """Sets the texture path."""
        if texture_path:
            current_maya_project = cmds.workspace(rootDirectory=True, query=True)

            if os.path.exists(texture_path):
                if texture_path.startswith(current_maya_project):
                    texture_path = texture_path.removeprefix(current_maya_project)
                    color = '#ffffff'
                else:
                    color = '#ffd600'
            else:
                color = '#fa0c08'

            self.texture_path_label.setStyleSheet(maurice_qt.line_edit_style() + 'QLabel {color: %s}' % color)
            self.texture_path_label.setText(texture_path)
            self.texture_path_push_button.setVisible(True)

    def set_texture_suffix(self, texture_suffix: str) -> None:
        """Sets the texture suffix."""
        self.texture_suffix_line_edit.setText(texture_suffix)

    def set_title(self, title: str) -> None:
        """Sets title."""
        self.texture_type_label.setText(title)
