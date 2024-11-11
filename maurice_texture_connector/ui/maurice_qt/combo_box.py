"""
========================================================================================================================
Name: combo_box.py
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

from maurice_texture_connector.ui.maurice_qt.maurice_widgets_styles import MauriceWidgetsStyle


class QComboBox(QtWidgets.QComboBox):
    """QComboBox."""

    def __init__(self) -> None:
        """Initializes class attributes."""
        super(QComboBox, self).__init__()

        maurice_widgets_style = MauriceWidgetsStyle()

        # QComboBox class variables.
        self.last_text = ''
        self.wheel_event = True

        # QComboBox settings.
        self.setFixedHeight(maurice_widgets_style.HEIGHT)
        self.setStyleSheet(maurice_widgets_style.combo_box())

        # QStandardItemModel.
        self.standard_item_model = QtGui.QStandardItemModel()
        self.setModel(self.standard_item_model)
        self.setItemDelegate(QSeparatorStyledItemDelegate())

    def add_separator(self) -> None:
        """Adds a separator."""
        separator_standard_item = QtGui.QStandardItem()
        separator_standard_item.setData('mauriceSeparator', QtCore.Qt.UserRole)
        separator_standard_item.setEnabled(False)
        separator_standard_item.setSizeHint(QtCore.QSize(0, 10))
        self.standard_item_model.appendRow(separator_standard_item)

    def items_text(self) -> list:
        """Gets the items text."""
        return [self.itemText(i) for i in range(self.count())]

    @property
    def last_text_selected(self) -> str:
        """Gets the last text selected."""
        return self.last_text

    def set_wheel_event(self, wheel_event: bool) -> None:
        """Sets the wheel event."""
        self.wheel_event = wheel_event

    def keyPressEvent(self, event: any) -> None:
        """Key press event."""
        pass

    def mousePressEvent(self, event: any) -> None:
        """Mouse press event."""
        super(QComboBox, self).mousePressEvent(event)

        self.last_text = self.currentText()

    def wheelEvent(self, event: any) -> None:
        """Wheel event."""
        if self.wheel_event:
            super(QComboBox, self).wheelEvent(event)


class QSeparatorStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    """QSeparatorStyledItemDelegate."""

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        """Paint."""
        if index.data(QtCore.Qt.UserRole) == 'mauriceSeparator':
            pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
            pen.setWidth(1)
            painter.setPen(pen)

            separator_rect = option.rect
            y_center = separator_rect.center().y()
            start = separator_rect.bottomLeft()
            end = separator_rect.bottomRight()
            start.setY(y_center)
            end.setY(y_center)
            start.setX(start.x())
            end.setX(end.x())

            painter.drawLine(start, end)
        else:
            super(QSeparatorStyledItemDelegate, self).paint(painter, option, index)
