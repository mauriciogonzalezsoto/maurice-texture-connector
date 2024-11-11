"""
========================================================================================================================
Name: collapsable_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

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

import logging
import inspect

from maurice_texture_connector.ui.maurice_qt.maurice_widgets_styles import MauriceWidgetsStyle
import maurice_texture_connector.utils as maurice_utils


logger = logging.getLogger(__name__)


class Header(QtWidgets.QWidget):
    """Header widget."""
    clicked = QtCore.Signal()
    toggled = QtCore.Signal()

    def __init__(self, title: str) -> None:
        """Initializes class attributes."""
        super(Header, self).__init__()

        self.maurice_widgets_style = MauriceWidgetsStyle()

        # Files path class variables.
        self.icons = maurice_utils.get_icons()

        # Header class variables.
        self.background_label = None
        self.title_label = None
        self.caret_right_pixmap = None
        self.caret_down_pixmap = None
        self.icon_label = None
        self.collapsable = None
        self.is_expanded = False

        # Creates the widgets.
        self.create_widgets()
        self.create_layouts()

        self.set_title(title)

    def create_widgets(self) -> None:
        """Creates the widgets."""
        # Background QLabel.
        self.background_label = QtWidgets.QLabel()
        self.background_label.setFixedHeight(self.maurice_widgets_style.HEIGHT)
        self.background_label.setStyleSheet(f'''
            QLabel {{
                background-color: rgb(45, 45, 45); 
                border-radius: {maurice_utils.get_value_by_ppi(5, 7.5)}
            }}
            ''')

        # Title QLabel.
        self.title_label = QtWidgets.QLabel()
        self.title_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.title_label.setAlignment(QtCore.Qt.AlignLeft)
        self.title_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.title_label.setMargin(maurice_utils.get_value_by_ppi(3, 5))
        self.title_label.setStyleSheet(self.maurice_widgets_style.label())

        # Caret right QImage.
        caret_right_image = QtGui.QImage(self.icons['caret-right.png'])
        caret_right_image = caret_right_image.scaled(
            self.maurice_widgets_style.HEIGHT,
            self.maurice_widgets_style.HEIGHT,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation)

        # Caret right QPixmap.
        self.caret_right_pixmap = QtGui.QPixmap(caret_right_image)
        self.caret_right_pixmap.convertFromImage(caret_right_image)

        # Caret down QImage.
        caret_down_image = QtGui.QImage(self.icons['caret-down.png'])
        caret_down_image = caret_down_image.scaled(
            self.maurice_widgets_style.HEIGHT,
            self.maurice_widgets_style.HEIGHT,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation)

        # Caret down QPixmap.
        self.caret_down_pixmap = QtGui.QPixmap(caret_down_image)
        self.caret_down_pixmap.convertFromImage(caret_down_image)

        # Icon QLabel.
        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.icon_label.setAlignment(QtCore.Qt.AlignRight)
        self.icon_label.setPixmap(self.caret_right_pixmap)

    def create_layouts(self) -> None:
        """Creates the layouts."""
        # Header QStackedLayout.
        header_stacked_layout = QtWidgets.QStackedLayout(self)
        header_stacked_layout.setStackingMode(QtWidgets.QStackedLayout.StackAll)

        # Header QHBoxLayout.
        header_widget = QtWidgets.QWidget()
        header_widget.setFixedHeight(self.maurice_widgets_style.HEIGHT)

        # Header QHBoxLayout.
        header_h_box_layout = QtWidgets.QHBoxLayout(header_widget)
        header_h_box_layout.setContentsMargins(0, 0, 0, 0)
        header_h_box_layout.addWidget(self.title_label)
        header_h_box_layout.addWidget(self.icon_label)
        header_stacked_layout.addWidget(header_widget)
        header_stacked_layout.addWidget(self.background_label)

    def collapse(self) -> None:
        """Collapses the QCollapsableWidget."""
        if self.collapsable:
            self.icon_label.setPixmap(self.caret_right_pixmap)
            self.is_expanded = False

    def expand(self) -> None:
        """Expands the QCollapsableWidget."""
        if self.collapsable:
            self.icon_label.setPixmap(self.caret_down_pixmap)
            self.is_expanded = True

    def set_collapsable(self, collapsable: bool) -> None:
        """Sets the QCollapsableWidget as collapsable."""
        if not collapsable:
            self.expand()
            self.icon_label.setPixmap(QtGui.QPixmap(''))
        else:
            if self.is_expanded:
                self.icon_label.setPixmap(self.caret_down_pixmap)

        self.collapsable = collapsable

    def set_title(self, title: str) -> None:
        """Sets the QCollapsableWidget title."""
        self.title_label.setText(f'<b>{title}</b>')

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Mouse release event."""
        self.clicked.emit()
        self.toggled.emit()


class QCollapsableWidget(QtWidgets.QWidget):
    """QCollapsableWidget."""

    def __init__(self, title: str, parent: QtWidgets.QWidget) -> None:
        """Initializes class attributes."""
        super(QCollapsableWidget, self).__init__()

        self.maurice_widgets_style = MauriceWidgetsStyle()

        # QCollapsableWidget class variables.
        self.header = None
        self.content_widget = None
        self.content_v_box_layout = None
        self.parent = parent
        self.title = title
        self.collapsable = None
        self.container_height = None

        # Creates the widgets.
        self.create_frame_layout()
        self.set_collapsable(True)

    def create_frame_layout(self) -> None:
        """Creates the QCollapsableWidget."""
        # Frame layout QVBoxLayout.
        frame_layout_v_box_layout = QtWidgets.QVBoxLayout(self)
        frame_layout_v_box_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout_v_box_layout.setSpacing(0)

        # Header.
        self.header = Header(title=self.title)

        # Frame layout QWidget.
        frame_layout_widget = QtWidgets.QWidget()
        frame_layout_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        frame_layout_v_box_layout.addWidget(self.header)
        frame_layout_v_box_layout.addWidget(frame_layout_widget)

        # Frame layout QGridLayout.
        frame_layout_grid_layout = QtWidgets.QGridLayout(frame_layout_widget)
        frame_layout_grid_layout.setContentsMargins(0, 0, 0, 0)

        # Content QWidget.
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setVisible(False)
        frame_layout_grid_layout.addWidget(self.content_widget)

        # Content QVBoxLayout.
        self.content_v_box_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_v_box_layout.setContentsMargins(
            self.maurice_widgets_style.SPACING,
            self.maurice_widgets_style.SPACING,
            self.maurice_widgets_style.SPACING,
            0)
        self.content_v_box_layout.setSpacing(self.maurice_widgets_style.SPACING)

    def on_header_clicked(self) -> None:
        """On header clicked."""
        if self.header.is_expanded:
            self.collapse()
        else:
            self.expand()

    def add_layout(self, layout: any) -> None:
        """Adds a layout."""
        self.content_v_box_layout.addLayout(layout)

    def add_widget(self, widget) -> None:
        """Adds a widget."""
        self.content_v_box_layout.addWidget(widget)

    def collapse(self) -> None:
        """Collapses the QCollapsableWidget."""
        if not self.container_height:
            logger.error(f'[{inspect.currentframe().f_code.co_name}] Height has not been set.')
            return

        if self.collapsable:
            if self.header.is_expanded:
                self.header.collapse()
                self.parent.setFixedHeight(self.parent.height() - self.container_height)
                self.content_widget.setVisible(False)
        else:
            logger.error(f'[{inspect.currentframe().f_code.co_name}] The QCollapsableWidget is not collapsable.')

    def expand(self) -> None:
        """Expands the QCollapsableWidget."""
        if not self.container_height:
            logger.error(f'[{inspect.currentframe().f_code.co_name}] Height has not been set.')
            return

        if self.collapsable:
            if not self.header.is_expanded:
                self.header.expand()
                self.parent.setFixedHeight(self.parent.height() + self.container_height)
                self.content_widget.setVisible(True)
        else:
            logger.error(f'[{inspect.currentframe().f_code.co_name}] The QCollapsableWidget is not collapsable.')

    @property
    def is_expanded(self) -> bool:
        """Gets whether the QCollapsableWidget is expanded."""
        return self.header.is_expanded

    @property
    def main_widget(self) -> any:
        """Gets the main widget."""
        return self.content_widget

    def set_collapsable(self, collapsable: bool):
        """Sets the QCollapsableWidget as collapsable."""
        self.header.set_collapsable(collapsable)
        self.collapsable = collapsable

        if not collapsable:
            self.header.clicked.disconnect(self.on_header_clicked)
            self.content_widget.setVisible(True)
        else:
            self.header.clicked.connect(self.on_header_clicked)

    def set_title(self, title: str):
        """Sets the QCollapsableWidget title."""
        self.header.set_title(title=title)

    def set_height(self, height: int):
        """Sets the QCollapsableWidget height."""
        self.container_height = height
