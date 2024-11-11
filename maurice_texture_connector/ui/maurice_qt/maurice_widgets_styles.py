"""
========================================================================================================================
Name: maurice_widgets_styles.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
import maurice_texture_connector.utils as maurice_utils


class MauriceWidgetsStyle(object):
    """Maurice widgets style."""
    SCALING_FACTOR = maurice_utils.get_value_by_ppi(2, 3)

    SOFTWARE_COLOR = '#5285A6'
    WHITE_COLOR = '#FFFFFF'
    WARNING_C0LOR = '#FFD600'
    ERROR_COLOR = '#D50000'

    BORDER_RADIUS = SCALING_FACTOR * 2
    FONT_SIZE = maurice_utils.get_value_by_ppi(11, 15)
    SPACING = SCALING_FACTOR
    HEIGHT = SCALING_FACTOR * 10
    WIDTH = maurice_utils.get_value_by_ppi(100, 126)

    def __init__(self) -> None:
        """Initializes class attributes."""
        self.icons = maurice_utils.get_icons()

    def check_box(self) -> str:
        """QCheckBox."""
        style = f'''
            QCheckBox {{
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
                font-size: {MauriceWidgetsStyle.FONT_SIZE};
            }}
            
            QCheckBox:!enabled {{
                color: rgb(112, 112, 112);
            }}
            
            QCheckBox::indicator:checked {{
                image: url({self.icons['checkbox.png']});
            }}
            
            QCheckBox::indicator:checked:!enabled {{
                image: url({self.icons['checkbox-disabled.png']});
            }}
            
            QCheckBox::indicator:checked:hover {{
                image: url({self.icons['checkbox-checked-hover.png']});
            }}
            
            QCheckBox::indicator:unchecked {{
                image: url({self.icons['checkbox-unchecked.png']});
            }}
            
            QCheckBox::indicator:unchecked:hover {{
                image: url({self.icons['checkbox-unchecked-hover.png']});
            }}
            
            QCheckBox::indicator {{
                width: {MauriceWidgetsStyle.SCALING_FACTOR * 6}px; 
                height: {MauriceWidgetsStyle.SCALING_FACTOR * 6}px;
            }}
            '''

        return style

    def combo_box(self) -> str:
        """QComboBox."""
        style = f'''
            QComboBox {{
                background-color: rgb(45, 45, 45); 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px; 
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
                padding-left: {maurice_utils.get_value_by_ppi(4, 7)}px;
            }}
    
            QComboBox:!enabled {{
                color: rgb(112, 112, 112);
            }}
    
            QComboBox QAbstractItemView {{
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
                selection-background-color: {MauriceWidgetsStyle.SOFTWARE_COLOR};
            }}
    
            QComboBox::drop-down {{
                width: {MauriceWidgetsStyle.SCALING_FACTOR * 6}px; 
                border-left-width: {maurice_utils.get_value_by_ppi(3, 5)}px; 
                border-left-color: transparent;
                border-left-style: solid;
            }}
    
            QComboBox:on {{
                color: gray;
                padding-top: 0px; 
                padding-left: {maurice_utils.get_value_by_ppi(4, 7)}px;
            }}
    
            QComboBox::down-arrow {{
                image: url({self.icons['caret-down.png']});
            }}
    
            QComboBox::down-arrow {{
                width: {MauriceWidgetsStyle.SCALING_FACTOR * 6}px;
                height: {MauriceWidgetsStyle.SCALING_FACTOR * 6}px;
            }}
            
            QComboBox::separator {{
                background-color: rgb(205, 25, 25);
                margin: 1px 0px 1px 0px;
                padding-top:120px;
                height: 100px;
            }}
            '''

        return style

    @staticmethod
    def double_spin_box() -> str:
        """QDoubleSpinBox."""
        style = f'''
            QDoubleSpinBox {{
                background-color: rgb(45, 45, 45);
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px; 
                color: {MauriceWidgetsStyle.WHITE_COLOR};
                selection-background-color: {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
            }}
            
            QDoubleSpinBox:!enabled {{
                color: #808080;
            }}
            '''

        return style

    @staticmethod
    def group_box() -> str:
        """QGroupBox."""
        style = f'''
            QGroupBox {{
                background-color: rgb(65, 65, 65); 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px; 
                padding: {MauriceWidgetsStyle.SCALING_FACTOR}px;
            }}
            '''

        return style

    @staticmethod
    def label() -> str:
        """QLabel."""
        style = f'''
        QLabel {{
            color: {MauriceWidgetsStyle.WHITE_COLOR}; 
            font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
        }}
                       
        QLabel:!enabled {{
            color: #808080;
        }}
        '''

        return style

    @staticmethod
    def line_edit() -> str:
        """QLineEdit."""
        style = f'''
            QLineEdit {{
                background-color: rgb(45, 45, 45); 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px; 
                color: {MauriceWidgetsStyle.WHITE_COLOR};
                selection-background-color: {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px; 
                padding-left: 4px;
            }}
            
            QLineEdit:!enabled {{
                color: rgb(128, 128, 128);
            }}
            '''

        return style

    def list_widget(self) -> str:
        """QListWidget."""
        style = f'''
            QListWidget {{
                border: 2px solid rgb(43, 43, 43); 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px;
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
            }}
            
            QListWidget::item {{
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
            }}
            
            QListWidget::item:selected {{
                background: {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
                border: 2px solid {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px;
                color: black; 
                padding-left: -2px; 
                padding-top: 0px;
            }}
            
            {self.scroll_area()}
            '''

        return style

    def menu_bar(self) -> str:
        """QMenuBar."""
        style = f'''
            QMenuBar {{
                background-color: rgb(45, 45, 45); 
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
                padding: 1px 1px 1px {maurice_utils.get_value_by_ppi(-2, -4)}px;
                icon-size: {MauriceWidgetsStyle.SCALING_FACTOR * 8}px;
            }}
            
            QMenuBar::item {{
                border-radius: 5px; 
                padding: 3px 3px 3px 3px;
            }}
            
            QMenuBar::item:selected {{
                background-color: {MauriceWidgetsStyle.SOFTWARE_COLOR};
            }}
            
            QMenu {{
                background-color: rgb(40, 40, 40);
            }}
            
            QMenu::indicator {{
                background-color: rgb(40, 40, 40);
                height: 27px;
                width: 36px;
                padding: -1px -1px 2px 0px;
            }}
                        
            QMenu::item {{
                border-radius: 5px; 
                padding: 3px 50px 3px 15px;
                background-color: rgb(45, 45, 45);
                color: {MauriceWidgetsStyle.WHITE_COLOR};
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
                margin: 1px 0px 1px 0px;
                min-width: {MauriceWidgetsStyle.SCALING_FACTOR * 40}px;
                min-height: {MauriceWidgetsStyle.SCALING_FACTOR * 8}px;
            }}
            
            QMenu::item:selected {{
                background-color: {MauriceWidgetsStyle.SOFTWARE_COLOR};
            }}
            
            QMenu::icon {{
                subcontrol-origin: padding;
                subcontrol-position: left center;
                background-color: rgb(40, 40, 40);
                padding: 6px
            }}
            
            QMenu::right-arrow {{
                image: url({self.icons['caret-right.png']});
                width: 24px; 
                height: 24px;
            }}
            
            QMenu::separator {{
                height: 1px;
                background-color: {MauriceWidgetsStyle.WHITE_COLOR};
                margin: 1px 0px 1px 0px;
                margin-left: auto;
            }}
            '''

        return style

    @staticmethod
    def push_button() -> str:
        """QPushButton."""
        style = f'''
            QPushButton {{
                background-color: rgb(45, 45, 45); 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px; 
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
            }}
            
            QPushButton:!enabled {{
                color: rgb(128, 128, 128);
            }}
            
            QPushButton:pressed {{
                background-color: rgb(70, 70, 70);
                border: none;
            }}
            
            QPushButton:hover {{
                border: 2px solid {MauriceWidgetsStyle.SOFTWARE_COLOR};
            }}
            
            QToolTip {{
                background-color: rgb(45, 45, 45);
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
                border: 1px solid {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
            }}
            '''

        return style

    def radio_button(self) -> str:
        """QRadioButton."""
        style = f'''
            QRadioButton {{
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
            }}
                    
            QRadioButton:!enabled {{
                color: rgb(128, 128, 128);
            }}
            
            QRadioButton::indicator:checked {{
                image: url({self.icons['radio-button.png']});
            }}
            
            QRadioButton::indicator:checked:!enabled {{
                image: url({self.icons['radio-button-disabled.png']});
            }}
            
            QRadioButton::indicator:checked:hover {{
                image: url({self.icons['radio-button-checked-hover.png']});
            }}
            
            QRadioButton::indicator:unchecked {{
                image: url({self.icons['radio-button-unchecked.png']});
            }}
            
            QRadioButton::indicator:unchecked:!enabled {{
                image: url({self.icons['radio-button-unchecked-disabled.png']});
            }}
            
            QRadioButton::indicator:unchecked:hover {{
                image: url({self.icons['radio-button-unchecked-hover.png']});
            }}
            
            QRadioButton::indicator {{
                width: {MauriceWidgetsStyle.SCALING_FACTOR * 6}px; 
                height: {MauriceWidgetsStyle.SCALING_FACTOR * 6}px;
            }}
            '''

        return style

    @staticmethod
    def scroll_area() -> str:
        """QScrollArea."""
        scroll_area = f'''        
            QScrollArea {{
                background-color: rgb(55, 55, 55);
                border: none;
            }}
    
            QScrollBar:vertical {{
                border: none;
                background-color: transparent;
                width: 18px;
                margin: 0px 0px 0px 2px;
            }}
            
            QScrollBar::handle:vertical {{
                background: rgb(43, 43, 43);
                min-height: 20px;
                border-radius: 6px;
            }}
            
            QScrollBar::add-line:vertical {{
                background: none;
                height: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            
            QScrollBar::sub-line:vertical {{
                background: none;
                height: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            '''

        return scroll_area

    @staticmethod
    def spin_box() -> str:
        """QSpinBox."""
        style = f'''
            QSpinBox {{
                background-color: rgb(45, 45, 45);
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px;
                color: {MauriceWidgetsStyle.WHITE_COLOR};
                selection-background-color: {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
                font-size: {MauriceWidgetsStyle.FONT_SIZE}px;
            }}
            
            QSpinBox:!enabled {{
                color: rgb(128, 128, 128);
            }}
            '''

        return style

    @staticmethod
    def splitter() -> str:
        """QSplitter."""
        style = f'''
            QSplitter::handle {{
                background-color: transparent; 
                margin: {maurice_utils.get_value_by_ppi(-2, -4)}px;
            }}
            '''

        return style

    @staticmethod
    def tab_widget() -> str:
        """QTabWidget."""
        style = f'''
            QTabWidget::pane {{
                border: 0px;
                border-top: 2px solid #2b2b2b;
            }}
            
            QTabBar::tab {{
                background-color: #2b2b2b;
                color: rgb(43, 43, 43);
                border: none;
                border-radius: 4px;
                padding: 4px 6px 2px 6px;
                margin-right: 3px;
                margin-bottom: 1px;
            }}
            
            QTabBar::tab:only-one {{
                padding: 100px 10px 100px 10px;
            }}
            
            QTabBar::tab:selected {{
                background-color: rgb(45, 45, 45);
                color: {MauriceWidgetsStyle.WHITE_COLOR};
            }}
            
            QTabBar::tab:!selected {{
                background-color: rgb(70, 70, 70);
                color: {MauriceWidgetsStyle.WHITE_COLOR};
            }}
            
            QTabBar::tab:first {{
                margin-left: 0;
            }}
            
            QTabBar::tab:last {{
                margin-right: 0;
            }}
            '''

        return style

    def tree_widget(self) -> str:
        """QTreeWidget."""
        style = f'''
            QTreeWidget {{
                border: 2px solid rgb(43, 43, 43); 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px;
            }}
            
            QTreeWidget::item:selected {{
                background: {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
                border: 2px solid {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
                border-radius: {MauriceWidgetsStyle.BORDER_RADIUS}px;  
                color: black; 
                padding-left: -2px; 
                padding-top: 0px;
            }}
            
            QTreeView::branch {{
                background-color: rgb(43, 43, 43);
            }}
            
            QTreeView::branch:open {{
                image: url({self.icons['caret-down.png']});
            }}
            
            QTreeView::branch:closed:has-children {{
                image: url({self.icons['caret-right.png']});
            }}
            
            QToolTip {{
                background-color: rgb(45, 45, 45);
                color: {MauriceWidgetsStyle.WHITE_COLOR}; 
                border: 1px solid {MauriceWidgetsStyle.SOFTWARE_COLOR}; 
            }}
            
            {self.scroll_area()}
            ''' 
    
        return style

    @staticmethod
    def widget() -> str:
        """QWidget."""
        style = '''
            QWidget[localStyle="true"] {
                background-color: rgb(60, 60, 60);
            }
            '''
    
        return style
