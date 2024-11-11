"""
========================================================================================================================
Name: texture_connector_ui.py
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

import maya.api.OpenMaya as om
import maya.cmds as cmds

from functools import partial
import os

from maurice_texture_connector.core.create_material_network_redshift import CreateMaterialNetworkRedshift
from maurice_texture_connector.core.edit_material_network_redshift import EditMaterialNetworkRedshift
from maurice_texture_connector.core.create_material_network_arnold import CreateMaterialNetworkArnold
from maurice_texture_connector.core.edit_material_network_arnold import EditMaterialNetworkArnold
from maurice_texture_connector.core.create_network_network_v_ray import CreateMaterialNetworkVRay
from maurice_texture_connector.core.edit_material_network_v_ray import EditMaterialNetworkVRay
from maurice_texture_connector.ui.texture_settings_widget import TextureSettingsWidget
import maurice_texture_connector.ui.maurice_qt as maurice_qt
import maurice_texture_connector.utils as maurice_utils
import maurice_texture_connector as maurice


class TextureConnectorUI(maurice_qt.QDialogMaya):
    """Texture connector UI."""
    WINDOW_HEIGHT = maurice_utils.get_value_by_ppi(400, 600)
    WINDOW_NAME = maurice.TEXTURE_CONNECTOR_WINDOW_NAME
    WINDOW_TITLE = maurice.TEXTURE_CONNECTOR
    WINDOW_WIDTH = maurice_utils.get_value_by_ppi(600, 900)

    CONFIG_PATH = os.path.join(maurice_utils.get_data_folder_path(), f'{WINDOW_NAME}.ini')

    ARNOLD = 'Arnold'
    REDSHIFT = 'Redshift'
    V_RAY = 'V-Ray'

    IMAGE_EXTENSIONS_SUPPORTED = ['exr', 'gif', 'hdr', 'jpg', 'jpeg', 'png', 'tif', 'tiff']

    PUSH_BUTTON_SCALING_FACTOR = 1.5

    @classmethod
    def show_window(cls) -> None:
        """Shows the window."""
        if not cls.window_instance:
            cls.window_instance = TextureConnectorUI()

        super(TextureConnectorUI, cls).show_window()

    def __init__(self):
        """Initializes class attributes."""
        self.maurice_widgets_style = maurice_qt.MauriceWidgetsStyle()

        self.main_widget = None

        # Actions class variables.
        self.show_all_images_action = None
        self.show_base_color_images_action = None
        self.show_roughness_images_action = None
        self.show_metalness_images_action = None
        self.show_normal_images_action = None
        self.show_height_images_action = None
        self.show_emissive_images_action = None
        self.show_opacity_images_action = None
        self.create_material_network_action = None
        self.repath_files_action = None
        self.reveal_in_explorer = None

        # Activity class variables.
        self.show_settings_push_button = None
        self.show_explorer_push_button = None
        self.show_files_push_button = None
        self.show_hypershade_push_button = None

        # Settings class variables.
        self.settings_main_widget = None
        self.render_engine_combo_box = None
        self.create_material_network_push_button = None
        self.texture_connector_scroll_area = None
        self.settings_widget = None
        self.material_collapsable_widget = None
        self.base_color_check_box = None
        self.roughness_check_box = None
        self.metalness_check_box = None
        self.normal_check_box = None
        self.height_check_box = None
        self.emissive_check_box = None
        self.opacity_check_box = None
        self.triplanar_collapsable_widget = None
        self.use_triplanar_check_box = None
        self.settings_collapsable_widget = None
        self.use_texture_name_check_box = None
        self.case_sensitivity_check_box = None
        
        # Explorer class variables.
        self.explorer_widget = None
        self.materials_filter_line_edit = None
        self.materials_list_widget = None
        self.file_explorer_filter_line_edit = None
        self.file_explorer_tree_widget = None
        self.show_base_color_items = False
        self.show_roughness_items = False
        self.show_metalness_items = False
        self.show_normal_items = False
        self.show_height_items = False
        self.show_emissive_items = False
        self.show_opacity_items = False
        self.base_color_suffix = None
        self.roughness_suffix = None
        self.metalness_suffix = None
        self.normal_suffix = None
        self.height_suffix = None
        self.emissive_suffix = None
        self.opacity_suffix = None

        # Files class variables.
        self.files_widget = None
        self.files_filter_line_edit = None
        self.files_tree_widget = None

        # Texture connector class variables.
        self.presets_combo_box = None
        self.texture_connector_widget = None
        self.base_color_widget = None
        self.roughness_widget = None
        self.metalness_widget = None
        self.normal_widget = None
        self.height_widget = None
        self.emissive_widget = None
        self.opacity_widget = None
        self.base_color_file_texture_name = ''
        self.base_color_color_space = ''
        self.roughness_file_texture_name = ''
        self.roughness_color_space = ''
        self.metalness_file_texture_name = ''
        self.metalness_color_space = ''
        self.normal_file_texture_name = ''
        self.normal_color_space = ''
        self.height_file_texture_name = ''
        self.height_color_space = ''
        self.emissive_file_texture_name = ''
        self.emissive_color_space = ''
        self.opacity_file_texture_name = ''
        self.opacity_color_space = ''

        # Status bar class variables.
        self.maya_project_check_status_pixmap = None
        self.maya_project_warning_status_pixmap = None
        self.maya_project_status_label = None
        self.maya_project_path_label = None
        self.update_ui_push_button = None

        # Texture connector.
        self.edit_material_network_arnold = None
        self.edit_material_network_redshift = None
        self.edit_material_network_v_ray = None

        self.file_system_watcher = QtCore.QFileSystemWatcher()

        super(TextureConnectorUI, self).__init__()

        # QDialog settings.
        self.setMinimumHeight(self.WINDOW_HEIGHT)
        self.setMinimumWidth(self.WINDOW_WIDTH)
        self.set_window_title()

        # Main layout.
        self.main_layout.setAlignment(QtCore.Qt.AlignBottom)
        self.main_layout.setSpacing(0)

    def create_actions(self) -> None:
        """Creates the actions."""
        # ==============================================================================================================
        # File explorer.
        # ==============================================================================================================
        # Show all images QAction.
        self.show_all_images_action = maurice_qt.QAction('All')
        self.show_all_images_action.setIcon(QtGui.QIcon(self.icons['square-a-color.png']))

        # Show base color images QAction.
        self.show_base_color_images_action = maurice_qt.QAction('Base Color')
        self.show_base_color_images_action.setIcon(QtGui.QIcon(self.icons['square-d.png']))

        # Show roughness images QAction.
        self.show_roughness_images_action = maurice_qt.QAction('Roughness')
        self.show_roughness_images_action.setIcon(QtGui.QIcon(self.icons['square-r.png']))

        # Show metalness images QAction.
        self.show_metalness_images_action = maurice_qt.QAction('Metalness')
        self.show_metalness_images_action.setIcon(QtGui.QIcon(self.icons['square-m.png']))

        # Show normal images QAction.
        self.show_normal_images_action = maurice_qt.QAction('Normal')
        self.show_normal_images_action.setIcon(QtGui.QIcon(self.icons['square-n.png']))

        # Show height images QAction.
        self.show_height_images_action = maurice_qt.QAction('Height')
        self.show_height_images_action.setIcon(QtGui.QIcon(self.icons['square-h.png']))

        # Show emissive images QAction.
        self.show_emissive_images_action = maurice_qt.QAction('Emissive')
        self.show_emissive_images_action.setIcon(QtGui.QIcon(self.icons['square-e.png']))

        # Show opacity images QAction.
        self.show_opacity_images_action = maurice_qt.QAction('Opacity')
        self.show_opacity_images_action.setIcon(QtGui.QIcon(self.icons['square-o.png']))

        # Create material network QAction.
        self.create_material_network_action = maurice_qt.QAction('Create Material Network')
        self.create_material_network_action.setIcon(QtGui.QIcon(self.icons['chart-tree.png']))

        # ==============================================================================================================
        # Files.
        # ==============================================================================================================
        # Repath files QAction.
        self.repath_files_action = maurice_qt.QAction('Repath Files')
        self.repath_files_action.setIcon(QtGui.QIcon(self.icons['code-compare.png']))

        # Reveal in explorer QAction.
        self.reveal_in_explorer = maurice_qt.QAction('Reveal in Explorer')
        self.reveal_in_explorer.setIcon(QtGui.QIcon(self.icons['overview.png']))

    def create_widgets(self) -> None:
        """Creates the widgets."""
        # ==============================================================================================================
        # Activity.
        # ==============================================================================================================
        # Show settings QPushButton.
        self.show_settings_push_button = maurice_qt.QPushButton()
        self.show_settings_push_button.setFixedSize(
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR)
        self.show_settings_push_button.setIcon(QtGui.QIcon(self.icons['settings.png']))
        self.show_settings_push_button.setIconSize(QtCore.QSize(
            self.show_settings_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.show_settings_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR))
        self.show_settings_push_button.setToolTip(lmb='Settings')
        self.show_settings_push_button.set_transparent_background()

        # Show explorer QPushButton.
        self.show_explorer_push_button = maurice_qt.QPushButton()
        self.show_explorer_push_button.setFixedSize(
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR)
        self.show_explorer_push_button.setIcon(QtGui.QIcon(self.icons['ballot-disabled.png']))
        self.show_explorer_push_button.setIconSize(QtCore.QSize(
            self.show_explorer_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.show_explorer_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR))
        self.show_explorer_push_button.setToolTip(lmb='Explorer')
        self.show_explorer_push_button.set_transparent_background()

        # Show files QPushButton.
        self.show_files_push_button = maurice_qt.QPushButton()
        self.show_files_push_button.setFixedSize(
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR)
        self.show_files_push_button.setIcon(QtGui.QIcon(self.icons['folder-tree-disabled.png']))
        self.show_files_push_button.setIconSize(QtCore.QSize(
            self.show_files_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.show_files_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR))
        self.show_files_push_button.setToolTip(lmb='Files')
        self.show_files_push_button.set_transparent_background()

        # Show hypershade QPushButton.
        self.show_hypershade_push_button = maurice_qt.QPushButton()
        self.show_hypershade_push_button.setFixedSize(
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.maurice_widgets_style.HEIGHT * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR)
        self.show_hypershade_push_button.setIcon(QtGui.QIcon(self.icons['browser.png']))
        self.show_hypershade_push_button.setIconSize(QtCore.QSize(
            self.show_hypershade_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR,
            self.show_hypershade_push_button.ICON_SIZE * TextureConnectorUI.PUSH_BUTTON_SCALING_FACTOR))
        self.show_hypershade_push_button.setToolTip(lmb='Hypershade')
        self.show_hypershade_push_button.set_transparent_background()

        # ==============================================================================================================
        # Settings.
        # ==============================================================================================================
        # Render engine QComboBox.
        self.render_engine_combo_box = maurice_qt.QComboBox(fixed_size=False)

        # Base color QCheckBox.
        self.base_color_check_box = maurice_qt.QCheckBox('Base Color')

        # Roughness QCheckBox.
        self.roughness_check_box = maurice_qt.QCheckBox('Roughness')

        # Metalness QCheckBox.
        self.metalness_check_box = maurice_qt.QCheckBox('Metalness')

        # Normal QCheckBox.
        self.normal_check_box = maurice_qt.QCheckBox('Normal')

        # Height QCheckBox.
        self.height_check_box = maurice_qt.QCheckBox('Height')

        # Emissive QCheckBox.
        self.emissive_check_box = maurice_qt.QCheckBox('Emissive')

        # Opacity QCheckBox.
        self.opacity_check_box = maurice_qt.QCheckBox('Opacity')

        # Use triplanar QCheckBox.
        self.use_triplanar_check_box = maurice_qt.QCheckBox('Use Triplanar')

        # Use texture base QCheckBox.
        self.use_texture_name_check_box = maurice_qt.QCheckBox('Use Texture Name')

        # Case sensitivity QCheckBox.
        self.case_sensitivity_check_box = maurice_qt.QCheckBox('Case Sensitivity')

        # Create material network QPushButton.
        self.create_material_network_push_button = maurice_qt.QPushButton('Create Material Network')
        self.create_material_network_push_button.setIcon(QtGui.QIcon(self.icons['chart-tree.png']))
        self.create_material_network_push_button.setToolTip(lmb='Create Material Network')
        self.create_material_network_push_button.set_color_background()

        # ==============================================================================================================
        # Texture connector.
        # ==============================================================================================================
        # Presets QComboBox.
        self.presets_combo_box = maurice_qt.QComboBox(fixed_size=False)
        self.presets_combo_box.add_separator()
        self.presets_combo_box.set_wheel_event(False)
        self.presets_combo_box.addItems(['Add New Preset', 'Delete Current Preset'])

        # Base color widget.
        self.base_color_widget = TextureSettingsWidget()
        self.base_color_widget.set_title('Base Color')
        self.base_color_widget.setVisible(False)

        # Roughness widget.
        self.roughness_widget = TextureSettingsWidget()
        self.roughness_widget.set_title('Roughness')
        self.roughness_widget.setVisible(False)

        # Metalness widget.
        self.metalness_widget = TextureSettingsWidget()
        self.metalness_widget.set_title('Metalness')
        self.metalness_widget.setVisible(False)

        # Normal widget.
        self.normal_widget = TextureSettingsWidget()
        self.normal_widget.set_title('Normal')
        self.normal_widget.setVisible(False)

        # Height widget.
        self.height_widget = TextureSettingsWidget()
        self.height_widget.set_title('Height')
        self.height_widget.setVisible(False)

        # Emissive widget.
        self.emissive_widget = TextureSettingsWidget()
        self.emissive_widget.set_title('Emissive')
        self.emissive_widget.setVisible(False)

        # Opacity widget.
        self.opacity_widget = TextureSettingsWidget()
        self.opacity_widget.set_title('Opacity')
        self.opacity_widget.setVisible(False)

        # ==============================================================================================================
        # Explorer.
        # ==============================================================================================================
        # Materials filter QLineEdit.
        self.materials_filter_line_edit = maurice_qt.QLineEdit()
        self.materials_filter_line_edit.setPlaceholderText('Search...')

        # Materials QListWidget.
        self.materials_list_widget = maurice_qt.QListWidget()
        self.materials_list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.materials_list_widget.setMinimumHeight(maurice_utils.get_value_by_ppi(100, 150))
        self.materials_list_widget.setSelectionMode(QtWidgets.QListWidget.SingleSelection)

        # File explorer filter QLineEdit.
        self.file_explorer_filter_line_edit = maurice_qt.QLineEdit()
        self.file_explorer_filter_line_edit.setPlaceholderText('Search...')

        # File explorer QTreeWidget.
        self.file_explorer_tree_widget = maurice_qt.QTreeWidget()
        self.file_explorer_tree_widget.setMinimumHeight(maurice_utils.get_value_by_ppi(100, 150))

        # ==============================================================================================================
        # Files.
        # ==============================================================================================================
        self.files_filter_line_edit = maurice_qt.QLineEdit()
        self.files_filter_line_edit.setPlaceholderText('Search...')

        # Files QTreeWidget.
        self.files_tree_widget = maurice_qt.QTreeWidget()
        self.files_tree_widget.setMinimumHeight(maurice_utils.get_value_by_ppi(100, 150))

        # ==============================================================================================================
        # Status bar.
        # ==============================================================================================================
        # Maya project check status QImage.
        maya_project_check_status_image = QtGui.QImage(self.icons['check.png'])
        maya_project_check_status_image = maya_project_check_status_image.scaled(
            maurice_utils.get_value_by_ppi(14, 21),
            maurice_utils.get_value_by_ppi(14, 21),
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation)

        # Maya project check status QPixmap.
        self.maya_project_check_status_pixmap = QtGui.QPixmap()
        self.maya_project_check_status_pixmap.convertFromImage(maya_project_check_status_image)

        # Maya project warning status QImage.
        maya_project_warning_status_image = QtGui.QImage(self.icons['warning.png'])
        maya_project_warning_status_image = maya_project_warning_status_image.scaled(
            maurice_utils.get_value_by_ppi(14, 21),
            maurice_utils.get_value_by_ppi(14, 21),
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation)

        # Maya project warning status QPixmap.
        self.maya_project_warning_status_pixmap = QtGui.QPixmap()
        self.maya_project_warning_status_pixmap.convertFromImage(maya_project_warning_status_image)

        # Maya project status QLabel.
        self.maya_project_status_label = QtWidgets.QLabel()
        self.maya_project_status_label.setMaximumSize(
            maurice_utils.get_value_by_ppi(14, 21),
            maurice_utils.get_value_by_ppi(14, 21))

        # Maya project path QLabel.
        self.maya_project_path_label = maurice_qt.QLabel()

        # Update UI QPushButton.
        self.update_ui_push_button = maurice_qt.QPushButton()
        self.update_ui_push_button.setIcon(QtGui.QIcon(self.icons['refresh.png']))
        self.update_ui_push_button.setIconSize(QtCore.QSize(
            self.update_ui_push_button.ICON_SIZE * 0.75,
            self.update_ui_push_button.ICON_SIZE * 0.75))
        self.update_ui_push_button.setFixedSize(QtCore.QSize(
            self.maurice_widgets_style.HEIGHT * 0.75,
            self.maurice_widgets_style.HEIGHT * 0.75))
        self.update_ui_push_button.setToolTip(lmb='Update Interface.')
        self.update_ui_push_button.set_transparent_background()

    def create_layouts(self) -> None:
        """Creates the layouts."""
        # Main QWidget.
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setVisible(False)
        self.main_layout.addWidget(self.main_widget)

        # Main QHBoxLayout.
        main_h_box_layout = maurice_qt.QHBoxLayout()
        self.main_widget.setLayout(main_h_box_layout)

        # ==============================================================================================================
        # Activity.
        # ==============================================================================================================
        # Activity main QVBoxLayout.
        activity_main_v_box_layout = maurice_qt.QVBoxLayout()
        activity_main_v_box_layout.addWidget(self.show_settings_push_button)
        activity_main_v_box_layout.addWidget(self.show_explorer_push_button)
        activity_main_v_box_layout.addWidget(self.show_files_push_button)
        activity_main_v_box_layout.addStretch()
        activity_main_v_box_layout.addWidget(self.show_hypershade_push_button)
        activity_main_v_box_layout.setAlignment(QtCore.Qt.AlignTop)
        main_h_box_layout.addLayout(activity_main_v_box_layout)

        # Main QSplitter.
        main_splitter = maurice_qt.QSplitter()
        main_h_box_layout.addWidget(main_splitter)

        # Activity QWidget.
        activity_widget = QtWidgets.QWidget()
        main_splitter.addWidget(activity_widget)

        # Activity QVBoxLayout.
        activity_v_box_layout = maurice_qt.QVBoxLayout()
        activity_widget.setLayout(activity_v_box_layout)

        # ==============================================================================================================
        # Settings.
        # ==============================================================================================================
        # Settings main QWidget.
        self.settings_main_widget = QtWidgets.QWidget()
        self.settings_main_widget.setMinimumWidth(maurice_utils.get_value_by_ppi(236, 314))
        activity_v_box_layout.addWidget(self.settings_main_widget)

        # Settings main QVBoxLayout.
        settings_main_v_box_layout = maurice_qt.QVBoxLayout()
        settings_main_v_box_layout.addWidget(self.render_engine_combo_box)
        self.settings_main_widget.setLayout(settings_main_v_box_layout)

        # Settings QWidget.
        self.settings_widget = QtWidgets.QWidget()
        self.settings_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        settings_main_v_box_layout.addWidget(self.settings_widget)

        # Settings QVBoxLayout.
        settings_v_box_layout = maurice_qt.QVBoxLayout()
        self.settings_widget.setLayout(settings_v_box_layout)

        # Material QCollapsableWidget.
        self.material_collapsable_widget = maurice_qt.QCollapsableWidget(title='Material', parent=self.settings_widget)
        self.material_collapsable_widget.set_height(maurice_utils.get_value_by_ppi(109, 167))
        settings_v_box_layout.addWidget(self.material_collapsable_widget)

        # Material QGroupBox.
        material_group_box = maurice_qt.QGroupBox()
        self.material_collapsable_widget.add_widget(material_group_box)

        # Material QFormLayout.
        material_form_layout = maurice_qt.QFormLayout()
        material_form_layout.addWidget(self.base_color_check_box)
        material_form_layout.addWidget(self.roughness_check_box)
        material_form_layout.addWidget(self.metalness_check_box)
        material_form_layout.addWidget(self.normal_check_box)
        material_form_layout.addWidget(self.height_check_box)
        material_form_layout.addWidget(self.emissive_check_box)
        material_form_layout.addWidget(self.opacity_check_box)
        material_form_layout.setContentsMargins(maurice_utils.get_value_by_ppi(88, 112), 0, 0, 0)
        material_group_box.setLayout(material_form_layout)

        # Triplanar QCollapsableWidget.
        self.triplanar_collapsable_widget = maurice_qt.QCollapsableWidget(
            title='Triplanar',
            parent=self.settings_widget)
        self.triplanar_collapsable_widget.set_height(maurice_utils.get_value_by_ppi(19, 30))
        settings_v_box_layout.addWidget(self.triplanar_collapsable_widget)

        # Triplanar QGroupBox.
        triplanar_group_box = maurice_qt.QGroupBox()
        triplanar_group_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.triplanar_collapsable_widget.add_widget(triplanar_group_box)

        # Triplanar QFormLayout.
        triplanar_form_layout = maurice_qt.QFormLayout()
        triplanar_form_layout.addWidget(self.use_triplanar_check_box)
        triplanar_form_layout.setContentsMargins(maurice_utils.get_value_by_ppi(88, 112), 0, 0, 0)
        triplanar_group_box.setLayout(triplanar_form_layout)

        # Settings QCollapsableWidget.
        self.settings_collapsable_widget = maurice_qt.QCollapsableWidget(title='Settings', parent=self.settings_widget)
        self.settings_collapsable_widget.set_height(maurice_utils.get_value_by_ppi(19, 30))
        settings_v_box_layout.addWidget(self.settings_collapsable_widget)

        # Settings QGroupBox.
        settings_group_box = maurice_qt.QGroupBox()
        settings_group_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.settings_collapsable_widget.add_widget(settings_group_box)

        # Settings QFormLayout.
        settings_form_layout = maurice_qt.QFormLayout()
        settings_form_layout.addWidget(self.use_texture_name_check_box)
        settings_form_layout.setContentsMargins(maurice_utils.get_value_by_ppi(88, 112), 0, 0, 0)
        settings_group_box.setLayout(settings_form_layout)

        settings_main_v_box_layout.addStretch()
        settings_main_v_box_layout.addWidget(self.create_material_network_push_button)

        # ==============================================================================================================
        # Explorer.
        # ==============================================================================================================
        # Explorer QWidget.
        self.explorer_widget = QtWidgets.QWidget()
        self.explorer_widget.setMinimumWidth(maurice_utils.get_value_by_ppi(236, 314))
        self.explorer_widget.setVisible(False)
        activity_v_box_layout.addWidget(self.explorer_widget)

        # Explorer QVBoxLayout.
        explorer_v_box_layout = maurice_qt.QVBoxLayout(self.explorer_widget)

        # Explorer QSplitter.
        explorer_splitter = maurice_qt.QSplitter(QtCore.Qt.Vertical)
        explorer_v_box_layout.addWidget(explorer_splitter)

        # Materials QWidget.
        materials_widget = QtWidgets.QWidget()
        explorer_splitter.addWidget(materials_widget)

        # Materials QVBoxLayout.
        materials_v_box_layout = maurice_qt.QVBoxLayout()
        materials_v_box_layout.addWidget(self.materials_filter_line_edit)
        materials_v_box_layout.addWidget(self.materials_list_widget)
        materials_widget.setLayout(materials_v_box_layout)

        # File explorer QWidget.
        file_explorer_widget = QtWidgets.QWidget()
        explorer_splitter.addWidget(file_explorer_widget)

        # File explorer QVBoxLayout.
        file_explorer_v_box_layout = maurice_qt.QVBoxLayout()
        file_explorer_v_box_layout.addWidget(self.file_explorer_filter_line_edit)
        file_explorer_v_box_layout.addWidget(self.file_explorer_tree_widget)
        file_explorer_widget.setLayout(file_explorer_v_box_layout)

        # ==============================================================================================================
        # Files.
        # ==============================================================================================================
        # Files QWidget.
        self.files_widget = QtWidgets.QWidget()
        self.files_widget.setMinimumWidth(maurice_utils.get_value_by_ppi(236, 314))
        self.files_widget.setVisible(False)
        activity_v_box_layout.addWidget(self.files_widget)

        # Files QVBoxLayout.
        files_v_box_layout = maurice_qt.QVBoxLayout()
        files_v_box_layout.addWidget(self.files_filter_line_edit)
        files_v_box_layout.addWidget(self.files_tree_widget)
        self.files_widget.setLayout(files_v_box_layout)

        # ==============================================================================================================
        # Texture connector.
        # ==============================================================================================================
        # Texture connector QWidget.
        texture_connector_widget = QtWidgets.QWidget()
        texture_connector_widget.setMinimumWidth(maurice_utils.get_value_by_ppi(236, 314))
        main_splitter.addWidget(texture_connector_widget)

        # Texture connector main QVBoxLayout.
        texture_connector_main_v_box_layout = maurice_qt.QVBoxLayout(texture_connector_widget)
        texture_connector_main_v_box_layout.addWidget(self.presets_combo_box)

        # Texture connector QGroupBox.
        texture_connector_group_box = QtWidgets.QGroupBox()
        texture_connector_group_box.setStyleSheet(f'''
            QGroupBox {{
                background-color: rgb(35, 35, 35); 
                border-radius: {self.maurice_widgets_style.BORDER_RADIUS}px;
                padding: {maurice_utils.get_value_by_ppi(4, 6)}px;}}
            ''')
        texture_connector_main_v_box_layout.addWidget(texture_connector_group_box)

        # Texture connector QVBoxLayout.
        texture_connector_v_box_layout = maurice_qt.QVBoxLayout()
        texture_connector_group_box.setLayout(texture_connector_v_box_layout)

        # Texture connector QScrollArea.
        self.texture_connector_scroll_area = maurice_qt.QScrollArea()
        texture_connector_v_box_layout.addWidget(self.texture_connector_scroll_area)

        # Texture connector QWidget.
        self.texture_connector_widget = QtWidgets.QWidget()
        self.texture_connector_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.texture_connector_widget.setProperty('localStyle', True)
        self.texture_connector_widget.setStyleSheet('QWidget[localStyle="true"] {background-color: rgb(35, 35, 35);}')
        self.texture_connector_scroll_area.setWidget(self.texture_connector_widget)

        # Texture connector items QVBoxKLayout.
        texture_connector_items_v_box_layout = maurice_qt.QVBoxLayout()
        texture_connector_items_v_box_layout.addWidget(self.base_color_widget)
        texture_connector_items_v_box_layout.addWidget(self.roughness_widget)
        texture_connector_items_v_box_layout.addWidget(self.metalness_widget)
        texture_connector_items_v_box_layout.addWidget(self.normal_widget)
        texture_connector_items_v_box_layout.addWidget(self.height_widget)
        texture_connector_items_v_box_layout.addWidget(self.emissive_widget)
        texture_connector_items_v_box_layout.addWidget(self.opacity_widget)
        texture_connector_items_v_box_layout.setAlignment(QtCore.Qt.AlignTop)
        self.texture_connector_widget.setLayout(texture_connector_items_v_box_layout)

        main_splitter.setCollapsible(0, False)
        main_splitter.setCollapsible(1, False)
        main_splitter.setStretchFactor(1, 1)

        # ==============================================================================================================
        # Status bar.
        # ==============================================================================================================
        # Status bar QWidget.
        status_bar_widget = QtWidgets.QWidget()
        status_bar_widget.setFixedHeight(maurice_utils.get_value_by_ppi(20, 30))
        self.main_layout.addWidget(status_bar_widget)

        # Status bar QHBoxLayout.
        status_bar_h_box_layout = maurice_qt.QHBoxLayout()
        status_bar_h_box_layout.addWidget(self.maya_project_status_label)
        status_bar_h_box_layout.addWidget(self.maya_project_path_label)
        status_bar_h_box_layout.addStretch()
        status_bar_h_box_layout.addWidget(self.update_ui_push_button)
        status_bar_h_box_layout.setContentsMargins(maurice_utils.get_value_by_ppi(4, 6), 0, 0, 0)
        status_bar_widget.setLayout(status_bar_h_box_layout)

    def create_connections(self) -> None:
        """Creates the connections."""
        self.file_system_watcher.directoryChanged.connect(self.file_system_watcher_directory_changed)

        # ==============================================================================================================
        # Actions.
        # ==============================================================================================================
        self.show_all_images_action.triggered.connect(self.show_all_images_triggered_action)
        self.show_base_color_images_action.triggered.connect(self.show_base_color_images_triggered_action)
        self.show_roughness_images_action.triggered.connect(self.show_roughness_images_triggered_action)
        self.show_metalness_images_action.triggered.connect(self.show_metalness_images_triggered_action)
        self.show_normal_images_action.triggered.connect(self.show_normal_images_triggered_action)
        self.show_height_images_action.triggered.connect(self.show_height_images_triggered_action)
        self.show_emissive_images_action.triggered.connect(self.show_emissive_images_triggered_action)
        self.show_opacity_images_action.triggered.connect(self.show_opacity_images_triggered_action)
        self.create_material_network_action.triggered.connect(self.create_material_network_triggered_action)
        self.repath_files_action.triggered.connect(self.repath_files_clicked_push_button)
        self.reveal_in_explorer.triggered.connect(self.reveal_in_explorer_triggered_action)

        # ==============================================================================================================
        # Activity.
        # ==============================================================================================================
        self.show_settings_push_button.clicked.connect(self.show_settings_clicked_push_button)
        self.show_explorer_push_button.clicked.connect(self.show_explorer_clicked_push_button)
        self.show_files_push_button.clicked.connect(self.show_files_clicked_push_button)
        self.show_hypershade_push_button.clicked.connect(self.show_hypershade_clicked_push_button)

        # ==============================================================================================================
        # Settings.
        # ==============================================================================================================
        self.render_engine_combo_box.currentTextChanged.connect(self.render_engine_current_text_changed_combo_box)
        self.base_color_check_box.toggled.connect(self.base_color_toggled_check_box)
        self.roughness_check_box.toggled.connect(self.roughness_toggled_check_box)
        self.metalness_check_box.toggled.connect(self.metalness_toggled_check_box)
        self.normal_check_box.toggled.connect(self.normal_toggled_check_box)
        self.height_check_box.toggled.connect(self.height_toggled_check_box)
        self.emissive_check_box.toggled.connect(self.emissive_toggled_check_box)
        self.opacity_check_box.toggled.connect(self.opacity_toggled_check_box)
        self.create_material_network_push_button.clicked.connect(self.create_material_network_clicked_push_button)

        # ==============================================================================================================
        # Explorer.
        # ==============================================================================================================
        self.materials_filter_line_edit.textChanged.connect(self.materials_filter_text_changed_line_edit)
        self.materials_list_widget.itemClicked.connect(self.materials_item_clicked_list_widget)
        self.file_explorer_filter_line_edit.textChanged.connect(self.file_explorer_filter_text_changed_line_edit)
        self.file_explorer_tree_widget.customContextMenuRequested.connect(
            self.file_explore_custom_context_menu_requested_tree_widget)
        self.file_explorer_tree_widget.itemCollapsed.connect(self.file_explorer_item_collapsed_tree_widget)
        self.file_explorer_tree_widget.itemExpanded.connect(self.file_explorer_item_expanded_tree_widget)

        # ==============================================================================================================
        # Files.
        # ==============================================================================================================
        self.files_filter_line_edit.textChanged.connect(self.files_filter_text_changed_line_edit)
        self.files_tree_widget.customContextMenuRequested.connect(self.files_custom_context_menu_request_tree_widget)
        self.files_tree_widget.itemClicked.connect(self.files_item_clicked_tree_widget)

        # ==============================================================================================================
        # Texture connector.
        # ==============================================================================================================
        self.presets_combo_box.currentTextChanged.connect(self.presets_current_text_changed_combo_box)
        self.base_color_widget.edit_texture_clicked.connect(self.base_color_edit_texture_clicked_widget)
        self.roughness_widget.edit_texture_clicked.connect(self.roughness_edit_texture_clicked_widget)
        self.metalness_widget.edit_texture_clicked.connect(self.metalness_edit_texture_clicked_widget)
        self.normal_widget.edit_texture_clicked.connect(self.normal_edit_texture_clicked_widget)
        self.height_widget.edit_texture_clicked.connect(self.height_edit_texture_clicked_widget)
        self.emissive_widget.edit_texture_clicked.connect(self.emissive_edit_texture_clicked_widget)
        self.opacity_widget.edit_texture_clicked.connect(self.opacity_edit_texture_clicked_widget)

        # ==============================================================================================================
        # Status bar.
        # ==============================================================================================================
        self.update_ui_push_button.clicked.connect(self.update_ui_clicked_push_button)

    def save_settings(self) -> None:
        """Saves the settings."""
        current_preset = self.presets_combo_box.currentText()
        s = QtCore.QSettings(self.CONFIG_PATH, QtCore.QSettings.IniFormat)

        # ==============================================================================================================
        # Settings.
        # ==============================================================================================================
        s.beginGroup(f'settings')
        s.setValue('baseColor', self.base_color_check_box.isChecked())
        s.setValue('roughness', self.roughness_check_box.isChecked())
        s.setValue('metalness', self.metalness_check_box.isChecked())
        s.setValue('normal', self.normal_check_box.isChecked())
        s.setValue('height', self.height_check_box.isChecked())
        s.setValue('emissive', self.emissive_check_box.isChecked())
        s.setValue('opacity', self.opacity_check_box.isChecked())
        s.setValue('useTriplanar', self.use_triplanar_check_box.isChecked())
        s.setValue('useTextureName', self.use_texture_name_check_box.isChecked())
        s.endGroup()

        # ==============================================================================================================
        # Texture connector.
        # ==============================================================================================================
        s.beginGroup('texture_connector')
        s.setValue('presets', ','.join(self.presets_combo_box.items_text()[:-3]))
        s.setValue('currentPreset', current_preset)
        s.endGroup()

        s.beginGroup(current_preset)
        s.setValue('baseColorSuffix', self.base_color_widget.get_texture_suffix())
        s.setValue('roughnessSuffix', self.roughness_widget.get_texture_suffix())
        s.setValue('metalnessSuffix', self.metalness_widget.get_texture_suffix())
        s.setValue('normalSuffix', self.normal_widget.get_texture_suffix())
        s.setValue('heightSuffix', self.height_widget.get_texture_suffix())
        s.setValue('emissiveSuffix', self.emissive_widget.get_texture_suffix())
        s.setValue('opacitySuffix', self.opacity_widget.get_texture_suffix())
        s.endGroup()

    def reset_settings(self) -> None:
        """Resets the settings."""
        # ==============================================================================================================
        # Settings.
        # ==============================================================================================================
        self.base_color_check_box.setChecked(True)
        self.roughness_check_box.setChecked(True)
        self.metalness_check_box.setChecked(True)
        self.normal_check_box.setChecked(True)
        self.height_check_box.setChecked(True)
        self.emissive_check_box.setChecked(True)
        self.opacity_check_box.setChecked(True)
        self.use_triplanar_check_box.setChecked(False)
        self.use_texture_name_check_box.setChecked(True)

        # ==============================================================================================================
        # Texture connector.
        # ==============================================================================================================
        self.base_color_widget.set_texture_suffix('BaseColor')
        self.roughness_widget.set_texture_suffix('Roughness')
        self.metalness_widget.set_texture_suffix('Metallic')
        self.normal_widget.set_texture_suffix('Normal')
        self.height_widget.set_texture_suffix('Height')
        self.emissive_widget.set_texture_suffix('Emissive')
        self.opacity_widget.set_texture_suffix('Opacity')

    def show_about(self) -> None:
        """Shows the QAbout."""
        about_ui = maurice_qt.QAbout(
            parent=self,
            image_path=self.images['texture-connector.png'],
            tool_name=self.WINDOW_TITLE,
            tool_version=maurice.VERSION)
        about_ui.exec_()

    def collapse_collapsable_widgets(self) -> None:
        """Collapses collapsable widgets."""
        self.material_collapsable_widget.collapse()
        self.triplanar_collapsable_widget.collapse()
        self.settings_collapsable_widget.collapse()

        self.base_color_widget.collapse()
        self.roughness_widget.collapse()
        self.metalness_widget.collapse()
        self.normal_widget.collapse()
        self.height_widget.collapse()
        self.emissive_widget.collapse()
        self.opacity_widget.collapse()

    def expand_collapsable_widgets(self) -> None:
        """Expands collapsable widgets."""
        self.material_collapsable_widget.expand()
        self.triplanar_collapsable_widget.expand()
        self.settings_collapsable_widget.expand()

        self.base_color_widget.expand()
        self.roughness_widget.expand()
        self.metalness_widget.expand()
        self.normal_widget.expand()
        self.height_widget.expand()
        self.emissive_widget.expand()
        self.opacity_widget.expand()

    def load_settings(self) -> None:
        """Loads the settings."""
        s = QtCore.QSettings(self.CONFIG_PATH, QtCore.QSettings.IniFormat)

        # ==============================================================================================================
        # Settings.
        # ==============================================================================================================
        s.beginGroup('settings')
        self.base_color_check_box.setChecked(s.value('baseColor', 'True', str).lower() == 'true')
        self.roughness_check_box.setChecked(s.value('roughness', 'True', str).lower() == 'true')
        self.metalness_check_box.setChecked(s.value('metalness', 'True', str).lower() == 'true')
        self.normal_check_box.setChecked(s.value('normal', 'True', str).lower() == 'true')
        self.height_check_box.setChecked(s.value('height', 'True', str).lower() == 'true')
        self.emissive_check_box.setChecked(s.value('emissive', 'True', str).lower() == 'true')
        self.opacity_check_box.setChecked(s.value('opacity', 'True', str).lower() == 'true')
        self.use_triplanar_check_box.setChecked(s.value('useTriplanar', 'False', str).lower() == 'true')
        self.use_texture_name_check_box.setChecked(s.value('useTextureName', 'True', str).lower() == 'true')
        s.endGroup()

        # ==============================================================================================================
        # Texture connector.
        # ==============================================================================================================
        self.block_all_signals()

        s.beginGroup('texture_connector')
        self.presets_combo_box.insertItems(0, s.value('presets', 'Maurice', str).split(','))
        self.presets_combo_box.setCurrentText(s.value('currentPreset', 'Maurice', str))
        s.endGroup()

        self.unblock_all_signals()

        s.beginGroup(self.presets_combo_box.currentText())
        self.base_color_widget.set_texture_suffix(s.value('baseColorSuffix', 'BaseColor', str))
        self.roughness_widget.set_texture_suffix(s.value('roughnessSuffix', 'Roughness', str))
        self.metalness_widget.set_texture_suffix(s.value('metalnessSuffix', 'Metallic', str))
        self.normal_widget.set_texture_suffix(s.value('normalSuffix', 'Normal', str))
        self.height_widget.set_texture_suffix(s.value('heightSuffix', 'Height', str))
        self.emissive_widget.set_texture_suffix(s.value('emissiveSuffix', 'Emissive', str))
        self.opacity_widget.set_texture_suffix(s.value('opacitySuffix', 'Opacity', str))
        s.endGroup()

    def create_call_backs(self) -> None:
        """Creates the call-backs."""
        om.MSceneMessage.addCallback(om.MSceneMessage.kAfterNew, self.new_scene)
        om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, self.new_scene)

        om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave, self.after_save_scene)

        om.MSceneMessage.addStringArrayCallback(om.MSceneMessage.kAfterPluginLoad, self.set_render_engines)
        om.MSceneMessage.addStringArrayCallback(om.MSceneMessage.kAfterPluginUnload, self.set_render_engines)

    def create_script_jobs(self) -> None:
        """Creates the script jobs."""
        self.script_jobs.append(cmds.scriptJob(event=['SelectionChanged', partial(self.selection_changed)]))
        self.script_jobs.append(cmds.scriptJob(event=['workspaceChanged', partial(self.workspace_changed)]))

    def new_scene(self, *args) -> None:
        """New scene."""
        self.clear_textures_info()
        self.set_maya_project_status_image()
        self.update_materials_items()
        self.update_images_items()
        self.update_files_items()

    def after_save_scene(self, *args) -> None:
        """After save scene."""
        self.set_maya_project_status_image()

    def selection_changed(self) -> None:
        """Selection changed."""
        default_materials = ['lambert1', 'standardSurface1', 'particleCloud1']
        material_selected = cmds.ls(selection=True, materials=True)

        if material_selected:
            material = material_selected[-1]

            if material not in default_materials:
                self.display_material_properties(material)
                self.select_material_item(material)

    def workspace_changed(self) -> None:
        """Workspace changed."""
        self.set_maya_project_status_image()
        self.set_current_maya_project_path_label()
        self.update_images_items()
        self.update_watched_paths()
        self.update_files_items()

    def file_system_watcher_directory_changed(self) -> None:
        """Executes the signal 'directory changed' of the file system watcher."""
        self.update_images_items()

    def show_all_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show all images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()
        self.update_images_items()

        self.show_all_images_action.setIcon(QtGui.QIcon(self.icons['square-a-color.png']))

    def show_base_color_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show base color images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()

        self.show_base_color_images_action.setIcon(QtGui.QIcon(self.icons['square-d-color.png']))
        self.base_color_suffix = self.base_color_widget.get_texture_suffix()
        self.show_base_color_items = True

        self.update_images_items()

    def show_roughness_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show roughness images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()

        self.show_roughness_images_action.setIcon(QtGui.QIcon(self.icons['square-r-color.png']))
        self.show_roughness_items = True
        self.roughness_suffix = self.roughness_widget.get_texture_suffix()

        self.update_images_items()

    def show_metalness_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show metalness images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()

        self.show_metalness_images_action.setIcon(QtGui.QIcon(self.icons['square-m-color.png']))
        self.metalness_suffix = self.metalness_widget.get_texture_suffix()
        self.show_metalness_items = True

        self.update_images_items()

    def show_normal_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show normal images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()

        self.show_normal_images_action.setIcon(QtGui.QIcon(self.icons['square-n-color.png']))
        self.normal_suffix = self.normal_widget.get_texture_suffix()
        self.show_normal_items = True

        self.update_images_items()

    def show_height_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show height images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()

        self.show_height_images_action.setIcon(QtGui.QIcon(self.icons['square-h-color.png']))
        self.height_suffix = self.height_widget.get_texture_suffix()
        self.show_height_items = True

        self.update_images_items()

    def show_emissive_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show emissive images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()

        self.show_emissive_images_action.setIcon(QtGui.QIcon(self.icons['square-e-color.png']))
        self.emissive_suffix = self.emissive_widget.get_texture_suffix()
        self.show_emissive_items = True

        self.update_images_items()

    def show_opacity_images_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'show opacity images' action."""
        self.disable_filter_explorer_filters()
        self.reset_file_explorer_actions_icons()
        
        self.show_opacity_images_action.setIcon(QtGui.QIcon(self.icons['square-o-color.png']))
        self.opacity_suffix = self.opacity_widget.get_texture_suffix()
        self.show_opacity_items = True

        self.update_images_items()

    def create_material_network_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'create material network' action."""
        item = self.file_explorer_tree_widget.currentItem()
        item_data = item.data(0, QtCore.Qt.UserRole)
        render_engine = self.render_engine_combo_box.currentText()

        if render_engine == TextureConnectorUI.ARNOLD:
            self.create_material_network_arnold(image_path=item_data)
        elif render_engine == TextureConnectorUI.REDSHIFT:
            self.create_material_network_redshift(image_path=item_data)
        elif render_engine == TextureConnectorUI.V_RAY:
            self.create_material_network_v_ray(image_path=item_data)

    def reveal_in_explorer_triggered_action(self) -> None:
        """Executes the signal 'triggered' of the 'reveal in explorer' action."""
        file_path = self.files_tree_widget.currentItem().data(0, QtCore.Qt.UserRole)

        if isinstance(file_path, tuple):
            file_path = file_path[1]

        file_info = QtCore.QFileInfo(file_path)

        if file_info.isDir():
            QtGui.QDesktopServices.openUrl(file_path)
        else:
            if os.name == 'nt':
                if self.open_in_explorer(file_path):
                    return
            elif os.name == 'posix':
                if self.open_in_finder(file_path):
                    return

    def show_settings_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'show settings' push button."""
        self.hide_activity_widgets()

        self.show_settings_push_button.setIcon(QtGui.QIcon(self.icons['settings.png']))
        self.settings_main_widget.setVisible(True)

    def show_explorer_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'show explorer' push button."""
        self.hide_activity_widgets()

        self.show_explorer_push_button.setIcon(QtGui.QIcon(self.icons['ballot.png']))
        self.explorer_widget.setVisible(True)

    def show_files_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'show files' push button."""
        self.hide_activity_widgets()

        self.show_files_push_button.setIcon(QtGui.QIcon(self.icons['folder-tree.png']))
        self.files_widget.setVisible(True)

    @staticmethod
    def show_hypershade_clicked_push_button() -> None:
        """Executes the signal 'clicked' of the 'show hypershade' push button."""
        cmds.HypershadeWindow()

    def render_engine_current_text_changed_combo_box(self, text: str) -> None:
        """Executes the signal 'current text changed' of the 'render engine' combo box."""
        renderer_engines_names = {
            TextureConnectorUI.ARNOLD: 'arnold',
            TextureConnectorUI.REDSHIFT: 'redshift',
            TextureConnectorUI.V_RAY: 'vray'}

        maya_current_render_engine = cmds.getAttr('defaultRenderGlobals.currentRenderer')

        if maya_current_render_engine != renderer_engines_names.get(text) and text:
            om.MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] The current engine is not {text}.')

        self.clear_textures_info()
        self.set_window_title()
        self.update_materials_items()

    def base_color_toggled_check_box(self, checked: bool) -> None:
        """Executes the signal 'toggled' of the 'Base color' check box."""
        self.base_color_widget.setVisible(checked)

    def roughness_toggled_check_box(self, checked: bool) -> None:
        """Executes the signal 'toggled' of the 'roughness' check box."""
        self.roughness_widget.setVisible(checked)

    def metalness_toggled_check_box(self, checked: bool) -> None:
        """Executes the signal 'toggled' of the 'metalness' check box."""
        self.metalness_widget.setVisible(checked)

    def normal_toggled_check_box(self, checked: bool) -> None:
        """Executes the signal 'toggled' of the 'normal' check box."""
        self.normal_widget.setVisible(checked)

    def height_toggled_check_box(self, checked: bool) -> None:
        """Executes the signal 'toggled' of the 'height' check box."""
        self.height_widget.setVisible(checked)

    def emissive_toggled_check_box(self, checked: bool) -> None:
        """Executes the signal 'toggled' of the 'emissive' check box."""
        self.emissive_widget.setVisible(checked)

    def opacity_toggled_check_box(self, checked: bool) -> None:
        """Executes the signal 'toggled' of the 'opacity' check box."""
        self.opacity_widget.setVisible(checked)

    def create_material_network_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'create material network' push button."""
        render_engine = self.render_engine_combo_box.currentText()

        if render_engine == TextureConnectorUI.ARNOLD:
            self.create_material_network_arnold()
        elif render_engine == TextureConnectorUI.REDSHIFT:
            self.create_material_network_redshift()
        elif render_engine == TextureConnectorUI.V_RAY:
            self.create_material_network_v_ray()

    def materials_filter_text_changed_line_edit(self) -> None:
        """Executes the signal 'text changed' of the 'materials filter' line edit."""
        self.update_materials_items()

    def materials_item_clicked_list_widget(self, item: any) -> None:
        """Executes the signal 'item clicked' of the 'materials' list widget."""
        self.clear_textures_info()

        material = item.text()

        if cmds.ls(material, materials=True):
            cmds.select(material, replace=True)
        else:
            self.update_materials_items()
            
    def file_explorer_filter_text_changed_line_edit(self) -> None:
        """Executes the signal 'text changed' of the 'file explorer filter' line edit."""
        self.update_images_items()

    def file_explore_custom_context_menu_requested_tree_widget(self, pos: any) -> None:
        """Executes the signal 'custom context menu requested' of the 'file explorer' tree widget."""
        item = self.file_explorer_tree_widget.currentItem()

        if item:
            item_data = item.data(0, QtCore.Qt.UserRole)
            file_info = QtCore.QFileInfo(item_data)

            context_menu = QtWidgets.QMenu()
            context_menu.setStyleSheet(self.maurice_widgets_style.menu_bar())

            if self.file_explorer_tree_widget.itemAt(pos):
                context_menu.addAction(self.show_all_images_action)
                context_menu.addAction(self.show_base_color_images_action)
                context_menu.addAction(self.show_roughness_images_action)
                context_menu.addAction(self.show_metalness_images_action)
                context_menu.addAction(self.show_normal_images_action)
                context_menu.addAction(self.show_height_images_action)
                context_menu.addAction(self.show_emissive_images_action)
                context_menu.addAction(self.show_opacity_images_action)

                if file_info.isFile():
                    context_menu.addSeparator()
                    context_menu.addAction(self.create_material_network_action)

            context_menu.exec_(self.file_explorer_tree_widget.mapToGlobal(pos))

    def file_explorer_item_collapsed_tree_widget(self, item: any) -> None:
        """Executes the signal 'item collapsed' of the 'file explorer' tree widget."""
        item.setIcon(0, QtGui.QIcon(self.icons['folder.png']))

    def file_explorer_item_expanded_tree_widget(self, item: any) -> None:
        """Executes the signal 'item expanded' of the 'file explorer' tree widget."""
        item.setIcon(0, QtGui.QIcon(self.icons['folder-open.png']))

    def files_filter_text_changed_line_edit(self) -> None:
        """Executes the signal 'text changed' of the 'files filter' line edit."""
        self.update_files_items()

    def files_custom_context_menu_request_tree_widget(self, pos: any) -> None:
        """Executes the signal 'custom context menu requested' of the 'files' tree widget."""
        item = self.files_tree_widget.currentItem()

        if item:
            context_menu = QtWidgets.QMenu()
            context_menu.setStyleSheet(self.maurice_widgets_style.menu_bar())

            context_menu.addAction(self.repath_files_action)
            context_menu.addSeparator()
            context_menu.addAction(self.reveal_in_explorer)

            context_menu.exec_(self.files_tree_widget.mapToGlobal(pos))

    @staticmethod
    def files_item_clicked_tree_widget(item: any) -> None:
        """Executes the signal 'item clicked' of the 'files' tree widget."""
        item_data = item.data(0, QtCore.Qt.UserRole)

        if item.parent():
            file_node = item_data[0]

            if cmds.objExists(file_node):
                cmds.select(file_node, replace=True)
            else:
                om.MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] \'{file_node}\' does not exists.')

    def repath_files_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'repath files' push button."""
        selected_item = self.files_tree_widget.currentItem()

        if selected_item:
            current_maya_project = cmds.workspace(rootDirectory=True, query=True)
            new_directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Find Directory', current_maya_project)

            if new_directory:
                item_parent = selected_item.parent()
                item = item_parent if item_parent else selected_item
                base_name = item.data(0, QtCore.Qt.UserRole)

                for i in range(item.childCount()):
                    child_item = item.child(i)
                    file_node, file_texture_name = child_item.data(0, QtCore.Qt.UserRole)

                    if cmds.objExists(file_node):
                        ignore_color_space_file_rules = cmds.getAttr(f'{file_node}.ignoreColorSpaceFileRules')

                        cmds.setAttr(
                            f'{file_node}.ignoreColorSpaceFileRules',
                            True)
                        cmds.setAttr(
                            f'{file_node}.fileTextureName',
                            file_texture_name.replace(base_name, new_directory),
                            type='string')
                        cmds.setAttr(
                            f'{file_node}.ignoreColorSpaceFileRules',
                            ignore_color_space_file_rules)

        self.update_files_items()

        material_item = self.materials_list_widget.currentItem()

        if material_item:
            self.display_material_properties(material=material_item.text())

    def presets_current_text_changed_combo_box(self, text: str) -> None:
        """Executes the signal 'current text changed' of the 'presets' combo box."""
        last_text_selected = self.presets_combo_box.last_text_selected

        if text == 'Add New Preset':
            self.presets_combo_box.setCurrentText(last_text_selected)
            self.add_new_preset()
        elif text == 'Delete Current Preset':
            self.presets_combo_box.setCurrentText(last_text_selected)
            self.delete_current_preset()
        else:
            s = QtCore.QSettings(self.CONFIG_PATH, QtCore.QSettings.IniFormat)
            s.beginGroup('texture_connector')
            s.setValue('currentPreset', self.presets_combo_box.currentText())
            s.endGroup()

    def base_color_edit_texture_clicked_widget(self) -> None:
        """Executes the signal 'edit texture clicked' of the 'base color' widget."""
        render_engine = self.render_engine_combo_box.currentText()
        image_path = self.get_open_file_name()

        if image_path:
            if render_engine == TextureConnectorUI.ARNOLD:
                self.edit_material_network_arnold.edit_base_color_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.REDSHIFT:
                self.edit_material_network_redshift.edit_base_color_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.V_RAY:
                self.edit_material_network_v_ray.edit_base_color_file_texture_node(image_path)

            self.base_color_widget.set_texture_path(image_path)

    def roughness_edit_texture_clicked_widget(self) -> None:
        """Executes the signal 'edit texture clicked' of the 'roughness' widget."""
        render_engine = self.render_engine_combo_box.currentText()
        image_path = self.get_open_file_name()

        if image_path:
            if render_engine == TextureConnectorUI.ARNOLD:
                self.edit_material_network_arnold.edit_roughness_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.REDSHIFT:
                self.edit_material_network_redshift.edit_roughness_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.V_RAY:
                self.edit_material_network_v_ray.edit_roughness_file_texture_node(image_path)

            self.roughness_widget.set_texture_path(image_path)

    def metalness_edit_texture_clicked_widget(self) -> None:
        """Executes the signal 'edit texture clicked' of the 'metalness' widget."""
        render_engine = self.render_engine_combo_box.currentText()
        image_path = self.get_open_file_name()

        if image_path:
            if render_engine == TextureConnectorUI.ARNOLD:
                self.edit_material_network_arnold.edit_metalness_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.REDSHIFT:
                self.edit_material_network_redshift.edit_metalness_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.V_RAY:
                self.edit_material_network_v_ray.edit_metalness_file_texture_node(image_path)

            self.metalness_widget.set_texture_path(image_path)

    def normal_edit_texture_clicked_widget(self) -> None:
        """Executes the signal 'edit texture clicked' of the 'normal' widget."""
        render_engine = self.render_engine_combo_box.currentText()
        image_path = self.get_open_file_name()

        if image_path:
            if render_engine == TextureConnectorUI.ARNOLD:
                self.edit_material_network_arnold.edit_normal_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.REDSHIFT:
                self.edit_material_network_redshift.edit_normal_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.V_RAY:
                self.edit_material_network_v_ray.edit_normal_file_texture_node(image_path)

            self.normal_widget.set_texture_path(image_path)

    def height_edit_texture_clicked_widget(self) -> None:
        """Executes the signal 'edit texture clicked' of the 'height' widget."""
        render_engine = self.render_engine_combo_box.currentText()
        image_path = self.get_open_file_name()

        if image_path:
            if render_engine == TextureConnectorUI.ARNOLD:
                self.edit_material_network_arnold.edit_height_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.REDSHIFT:
                self.edit_material_network_redshift.edit_height_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.V_RAY:
                self.edit_material_network_v_ray.edit_height_file_texture_node(image_path)

            self.height_widget.set_texture_path(image_path)

    def emissive_edit_texture_clicked_widget(self) -> None:
        """Executes the signal 'edit texture clicked' of the 'emissive' widget."""
        render_engine = self.render_engine_combo_box.currentText()
        image_path = self.get_open_file_name()

        if image_path:
            if render_engine == TextureConnectorUI.ARNOLD:
                self.edit_material_network_arnold.edit_emissive_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.REDSHIFT:
                self.edit_material_network_redshift.edit_emissive_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.V_RAY:
                self.edit_material_network_v_ray.edit_emissive_file_texture_node(image_path)

            self.emissive_widget.set_texture_path(image_path)

    def opacity_edit_texture_clicked_widget(self) -> None:
        """Executes the signal 'edit texture clicked' of the 'opacity' widget."""
        render_engine = self.render_engine_combo_box.currentText()
        image_path = self.get_open_file_name()

        if image_path:
            if render_engine == TextureConnectorUI.ARNOLD:
                self.edit_material_network_arnold.edit_opacity_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.REDSHIFT:
                self.edit_material_network_redshift.edit_opacity_file_texture_node(image_path)
            elif render_engine == TextureConnectorUI.V_RAY:
                self.edit_material_network_v_ray.edit_opacity_file_texture_node(image_path)

            self.opacity_widget.set_texture_path(image_path)

    def update_ui_clicked_push_button(self) -> None:
        """Executes the signal 'clicked' of the 'update UI' QPushButton."""
        self.update_files_items()
        self.update_images_items()
        self.update_materials_items()
        self.update_watched_paths()

        om.MGlobal.displayInfo(f'[{maurice.TEXTURE_CONNECTOR}] Interface updated.')

    def add_image_file_child_item(self, dir_path: str, file_name: str, parent_item: any) -> None:
        """Adds image file children item."""
        file_explorer_filter = self.file_explorer_filter_line_edit.text()

        file_path = os.path.join(dir_path, file_name)
        file_info = QtCore.QFileInfo(file_path)

        file_info_suffix = file_info.suffix().lower()
        file_info_name = file_info.fileName()

        if file_info_suffix in TextureConnectorUI.IMAGE_EXTENSIONS_SUPPORTED or file_info.isDir():
            if file_explorer_filter.lower() not in file_info_name.lower():
                return

            if file_info.isFile():
                if self.show_base_color_items:
                    if not self.base_color_suffix or self.base_color_suffix not in file_info_name:
                        return
                elif self.show_roughness_items:
                    if not self.roughness_suffix or self.roughness_suffix not in file_info_name:
                        return
                elif self.show_metalness_items:
                    if not self.metalness_suffix or self.metalness_suffix not in file_info_name:
                        return
                elif self.show_normal_items:
                    if not self.normal_suffix or self.normal_suffix not in file_info_name:
                        return
                elif self.show_height_items:
                    if not self.height_suffix or self.height_suffix not in file_info_name:
                        return
                elif self.show_emissive_items:
                    if not self.emissive_suffix or self.emissive_suffix not in file_info_name:
                        return
                elif self.show_opacity_items:
                    if not self.opacity_suffix or self.opacity_suffix not in file_info_name:
                        return

            item = QtWidgets.QTreeWidgetItem(parent_item, [file_name])
            item.setData(0, QtCore.Qt.UserRole, file_path)

            if file_info.isDir():
                item.setIcon(0, QtGui.QIcon(self.icons['folder.png']))
                self.add_image_file_children_item(dir_path=file_info.absoluteFilePath(), parent_item=item)
            else:
                item.setIcon(0, QtGui.QIcon(self.icons['picture.png']))

            if not parent_item:
                self.file_explorer_tree_widget.addTopLevelItem(item)

    def add_image_file_children_item(self, dir_path: str, parent_item: any) -> None:
        """Adds image file children item."""
        folders_ignored = ['.mayaSwatches', '.vrayThumbs']

        directory = QtCore.QDir(dir_path)
        directory.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)

        for file_name in directory.entryList():
            if file_name not in folders_ignored:
                self.add_image_file_child_item(dir_path=dir_path, file_name=file_name, parent_item=parent_item)

    def add_new_preset(self) -> None:
        """Add a new preset."""
        protected_names = ['Add New Preset', 'Delete Current Preset']

        input_dialog = maurice_qt.QInputDialog('New Preset Name')

        if input_dialog.exec_():
            new_preset_name = input_dialog.get_text()

            if new_preset_name in protected_names:
                om.MGlobal.displayError(f'[{maurice.TEXTURE_CONNECTOR}] Preset name is not allowed.')
            elif new_preset_name in self.presets_combo_box.items_text():
                om.MGlobal.displayError(
                    f'[{maurice.TEXTURE_CONNECTOR}] Preset name \'{new_preset_name}\' already exists.')
            else:
                self.presets_combo_box.insertItem(self.presets_combo_box.count() - 3, new_preset_name)
                self.presets_combo_box.setCurrentText(new_preset_name)

        s = QtCore.QSettings(self.CONFIG_PATH, QtCore.QSettings.IniFormat)
        s.beginGroup('texture_connector')
        s.setValue('presets', ','.join(self.presets_combo_box.items_text()[:-3]))
        s.endGroup()

    def delete_current_preset(self) -> None:
        """Deletes the current preset and its preference."""
        current_index = self.presets_combo_box.currentIndex()

        if self.presets_combo_box.currentText() != 'Maurice':
            if not maurice_qt.QMessageBoxQuestion(
                    question='Do you want to delete the current preset?',
                    title='Delete current preset').exec_():
                return

            s = QtCore.QSettings(self.CONFIG_PATH, QtCore.QSettings.IniFormat)
            s.remove(self.presets_combo_box.currentText())

            self.presets_combo_box.removeItem(current_index)
            self.presets_combo_box.setCurrentIndex(current_index - 1)

            s.beginGroup('texture_connector')
            s.setValue('presets', ','.join(self.presets_combo_box.items_text()[:-3]))
            s.endGroup()
        else:
            om.MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] The preset \'Maurice\' cannot be deleted.')

    def clear_textures_info(self) -> None:
        """Clears the textures info."""
        self.base_color_widget.clear_texture_info()
        self.roughness_widget.clear_texture_info()
        self.metalness_widget.clear_texture_info()
        self.normal_widget.clear_texture_info()
        self.height_widget.clear_texture_info()
        self.emissive_widget.clear_texture_info()
        self.opacity_widget.clear_texture_info()

    def create_material_network(self, image_path: str, material_network: any, use_triplanar: bool) -> None:
        """Creates the material network."""
        name = ''

        if not self.use_texture_name_check_box.isChecked():
            input_dialog = maurice_qt.QInputDialog('Material Name')

            if input_dialog.exec_():
                name = input_dialog.get_text()
            else:
                return

        if not image_path:
            image_path = self.get_open_file_name()

        if image_path:
            material_network.set_base_color_settings(
                enabled=self.use_texture_name_check_box.isChecked(),
                suffix=self.base_color_widget.get_texture_suffix())
            material_network.set_roughness_settings(
                enabled=self.roughness_check_box.isChecked(),
                suffix=self.roughness_widget.get_texture_suffix())
            material_network.set_metalness_settings(
                enabled=self.metalness_check_box.isChecked(),
                suffix=self.metalness_widget.get_texture_suffix())
            material_network.set_normal_settings(
                enabled=self.normal_check_box.isChecked(),
                suffix=self.normal_widget.get_texture_suffix())
            material_network.set_height_settings(
                enabled=self.height_check_box.isChecked(),
                suffix=self.height_widget.get_texture_suffix())
            material_network.set_emissive_settings(
                enabled=self.emissive_check_box.isChecked(),
                suffix=self.emissive_widget.get_texture_suffix())
            material_network.set_opacity_settings(
                enabled=self.opacity_check_box.isChecked(),
                suffix=self.opacity_widget.get_texture_suffix())

            material_network.create(
                name=name,
                image_path=image_path,
                use_texture_base_name=self.use_texture_name_check_box.isChecked(),
                use_triplanar=use_triplanar)

            self.update_materials_items()
            self.update_files_items()
            self.select_material_item(material_network.get_material())

    def load_look_dev_kit_plugin(self) -> None:
        """Loads the look dev kit plugin."""
        plugins_loaded = cmds.pluginInfo(listPlugins=True, query=True)
        use_triplanar = self.use_triplanar_check_box.isChecked()

        if 'lookdevKit' not in plugins_loaded and use_triplanar:
            if not maurice_qt.QMessageBoxQuestion(
                    question='Do you want to load the lookdevKit.mll plugin?',
                    title='Load Plugin').exec_():
                return

            cmds.loadPlugin('lookdevKit')

    def create_material_network_arnold(self, image_path: str = '') -> None:
        """Creates the material network Arnold."""
        self.load_look_dev_kit_plugin()
        self.clear_textures_info()

        material_network_arnold = CreateMaterialNetworkArnold()
        use_triplanar = self.use_triplanar_check_box.isChecked()

        if not material_network_arnold.are_plugins_loaded(
                render_engine_plugin_name='mtoa',
                use_triplanar=use_triplanar):
            return

        self.create_material_network(
            image_path=image_path,
            material_network=material_network_arnold,
            use_triplanar=use_triplanar)

    def create_material_network_redshift(self, image_path: str = '') -> None:
        """Creates the material network Redshift."""
        self.load_look_dev_kit_plugin()
        self.clear_textures_info()

        material_network_redshift = CreateMaterialNetworkRedshift()
        use_triplanar = self.use_triplanar_check_box.isChecked()

        if not material_network_redshift.are_plugins_loaded(
                render_engine_plugin_name='redshift4maya', 
                use_triplanar=use_triplanar):
            return

        self.create_material_network(
            image_path=image_path,
            material_network=material_network_redshift,
            use_triplanar=use_triplanar)

    def create_material_network_v_ray(self, image_path: str = '') -> None:
        """Creates the material network V-Ray."""
        self.load_look_dev_kit_plugin()
        self.clear_textures_info()

        material_network_v_ray = CreateMaterialNetworkVRay()
        use_triplanar = self.use_triplanar_check_box.isChecked()

        if not material_network_v_ray.are_plugins_loaded(
                render_engine_plugin_name='vrayformaya',
                use_triplanar=use_triplanar):
            return

        self.create_material_network(
            image_path=image_path,
            material_network=material_network_v_ray,
            use_triplanar=use_triplanar)

    def disable_filter_explorer_filters(self) -> None:
        """Disables the file explorer filters."""
        self.show_base_color_items = False
        self.show_roughness_items = False
        self.show_metalness_items = False
        self.show_normal_items = False
        self.show_height_items = False
        self.show_emissive_items = False
        self.show_opacity_items = False

    def display_material_properties(self, material: str) -> None:
        """Displays the material's properties."""
        render_engine = self.render_engine_combo_box.currentText()

        if render_engine == TextureConnectorUI.ARNOLD:
            if cmds.objectType(material, isType='aiStandardSurface'):
                self.edit_material_network_arnold = EditMaterialNetworkArnold(material)

                self.get_textures_properties(material_network=self.edit_material_network_arnold)
                self.display_textures_properties()
            else:
                self.clear_textures_info()

        elif render_engine == TextureConnectorUI.REDSHIFT:
            if cmds.objectType(material, isType='RedshiftStandardMaterial'):
                self.edit_material_network_redshift = EditMaterialNetworkRedshift(material)

                self.get_textures_properties(material_network=self.edit_material_network_redshift)
                self.display_textures_properties()
            else:
                self.clear_textures_info()

        elif render_engine == TextureConnectorUI.V_RAY:
            if cmds.objectType(material, isType='VRayMtl'):
                self.edit_material_network_v_ray = EditMaterialNetworkVRay(material)

                self.get_textures_properties(material_network=self.edit_material_network_v_ray)
                self.display_textures_properties()
            else:
                self.clear_textures_info()

    def display_textures_properties(self) -> None:
        """Displays the textures properties."""
        self.base_color_widget.set_texture_path(self.base_color_file_texture_name)
        self.base_color_widget.set_texture_color_space(self.base_color_color_space)
        self.roughness_widget.set_texture_path(self.roughness_file_texture_name)
        self.roughness_widget.set_texture_color_space(self.roughness_color_space)
        self.metalness_widget.set_texture_path(self.metalness_file_texture_name)
        self.metalness_widget.set_texture_color_space(self.metalness_color_space)
        self.normal_widget.set_texture_path(self.normal_file_texture_name)
        self.normal_widget.set_texture_color_space(self.normal_color_space)
        self.height_widget.set_texture_path(self.height_file_texture_name)
        self.height_widget.set_texture_color_space(self.height_color_space)
        self.emissive_widget.set_texture_path(self.emissive_file_texture_name)
        self.emissive_widget.set_texture_color_space(self.emissive_color_space)
        self.opacity_widget.set_texture_path(self.opacity_file_texture_name)
        self.opacity_widget.set_texture_color_space(self.opacity_color_space)

    def get_open_file_name(self) -> str:
        """Gets and opens the file name."""
        current_maya_project = cmds.workspace(rootDirectory=True, query=True)
        source_images_path = os.path.join(current_maya_project, 'sourceimages')
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Image', source_images_path)[0]

        return image_path

    def get_textures_properties(self, material_network: any) -> None:
        """Gets textures properties."""
        self.base_color_file_texture_name = material_network.get_base_color_file_texture_name()
        self.base_color_color_space = material_network.get_base_color_color_space()
        self.roughness_file_texture_name = material_network.get_roughness_file_texture_name()
        self.roughness_color_space = material_network.get_roughness_color_space()
        self.metalness_file_texture_name = material_network.get_metalness_file_texture_name()
        self.metalness_color_space = material_network.get_metalness_color_space()
        self.normal_file_texture_name = material_network.get_normal_file_texture_name()
        self.normal_color_space = material_network.get_normal_color_space()
        self.height_file_texture_name = material_network.get_height_file_texture_name()
        self.height_color_space = material_network.get_height_color_space()
        self.emissive_file_texture_name = material_network.get_emissive_file_texture_name()
        self.emissive_color_space = material_network.get_emissive_color_space()
        self.opacity_file_texture_name = material_network.get_opacity_file_texture_name()
        self.opacity_color_space = material_network.get_opacity_color_space()

    def hide_activity_widgets(self) -> None:
        """Hides the activity widgets."""
        self.show_settings_push_button.setIcon(QtGui.QIcon(self.icons['settings-disabled.png']))
        self.show_explorer_push_button.setIcon(QtGui.QIcon(self.icons['ballot-disabled.png']))
        self.show_files_push_button.setIcon(QtGui.QIcon(self.icons['folder-tree-disabled.png']))

        self.settings_main_widget.setVisible(False)
        self.explorer_widget.setVisible(False)
        self.files_widget.setVisible(False)

    @staticmethod
    def open_in_explorer(file_path: str) -> bool:
        file_info = QtCore.QFileInfo(file_path)
        args = []

        if not file_info.isDir():
            args.append('/Select,')

        args.append(QtCore.QDir.toNativeSeparators(file_path))

        if QtCore.QProcess.startDetached('explorer', args):
            return True

        return False

    @staticmethod
    def open_in_finder(file_path: str) -> bool:
        args = ['-e', 'tell application "Finder"', '-e', 'activate', '-e', 'select POSIX file "{0}"'.format(file_path),
                '-e', 'end tell', '-e', 'return']

        if QtCore.QProcess.startDetached('/usr/bin/osascript', args):
            return True

        return False

    def reset_file_explorer_actions_icons(self) -> None:
        """Resets the file explorer actions icons."""
        self.show_all_images_action.setIcon(QtGui.QIcon(self.icons['square-a.png']))
        self.show_base_color_images_action.setIcon(QtGui.QIcon(self.icons['square-d.png']))
        self.show_roughness_images_action.setIcon(QtGui.QIcon(self.icons['square-r.png']))
        self.show_metalness_images_action.setIcon(QtGui.QIcon(self.icons['square-m.png']))
        self.show_normal_images_action.setIcon(QtGui.QIcon(self.icons['square-n.png']))
        self.show_height_images_action.setIcon(QtGui.QIcon(self.icons['square-h.png']))
        self.show_emissive_images_action.setIcon(QtGui.QIcon(self.icons['square-e.png']))
        self.show_opacity_images_action.setIcon(QtGui.QIcon(self.icons['square-o.png']))

    def select_material_item(self, material_name: str) -> None:
        """Selects the material item."""
        items = self.materials_list_widget.findItems(material_name, QtCore.Qt.MatchExactly)

        if items:
            self.materials_list_widget.setCurrentItem(items[0])

    def set_current_maya_project_path_label(self) -> None:
        """Sets the current Maya project path label."""
        current_maya_project = cmds.workspace(rootDirectory=True, query=True)
        self.maya_project_path_label.setText(current_maya_project)

    def set_maya_project_status_image(self) -> None:
        """Sets Maya project status image."""
        current_maya_project = cmds.workspace(query=True, rootDirectory=True)
        current_maya_scene = cmds.file(query=True, sceneName=True)

        if current_maya_scene:
            self.maya_project_status_label.setVisible(True)

            if current_maya_scene.startswith(current_maya_project):
                self.maya_project_status_label.setPixmap(self.maya_project_check_status_pixmap)
            else:
                self.maya_project_status_label.setPixmap(self.maya_project_warning_status_pixmap)
        else:
            self.maya_project_status_label.setVisible(False)

    def set_render_engines(self, *args) -> None:
        """Sets render engines."""
        plugins_loaded = cmds.pluginInfo(listPlugins=True, query=True)
        render_engines = ('mtoa', 'redshift4maya', 'vrayformaya')

        # Add render engine.
        current_render_engine = self.render_engine_combo_box.currentText()

        self.render_engine_combo_box.clear()

        if render_engines[0] in plugins_loaded:
            self.render_engine_combo_box.addItem(TextureConnectorUI.ARNOLD)

        if render_engines[1] in plugins_loaded:
            self.render_engine_combo_box.addItem(TextureConnectorUI.REDSHIFT)

        if render_engines[2] in plugins_loaded:
            self.render_engine_combo_box.addItem(TextureConnectorUI.V_RAY)

        if current_render_engine:
            self.render_engine_combo_box.setCurrentText(current_render_engine)

        # Display texture connector.
        render_engine_loaded = any(render_engine in plugins_loaded for render_engine in render_engines)

        self.main_widget.setVisible(render_engine_loaded)

    def set_window_title(self) -> None:
        """Sets the window title."""
        render_engine = self.render_engine_combo_box.currentText()

        if render_engine:
            self.setWindowTitle(f'{maurice.TEXTURE_CONNECTOR} - {render_engine}')
        else:
            self.setWindowTitle(maurice.TEXTURE_CONNECTOR)

    def update_files_items(self) -> None:
        """Updated files items."""
        self.files_tree_widget.clear()

        current_maya_project = cmds.workspace(rootDirectory=True, query=True)
        files_filter = self.files_filter_line_edit.text()
        root_paths = {}

        for file_node in cmds.ls(type='file'):
            file_texture_name = cmds.getAttr(f'{file_node}.fileTextureName')

            if file_texture_name:
                file_texture_dirname = os.path.dirname(file_texture_name)

                if file_texture_dirname not in root_paths.keys():
                    root_paths[file_texture_dirname] = [(file_node, file_texture_name)]
                else:
                    files = root_paths[file_texture_dirname]
                    files.append((file_node, file_texture_name))

                    root_paths[file_texture_dirname] = files

        for key in root_paths.keys():
            top_level_item = QtWidgets.QTreeWidgetItem(None)
            top_level_item.setData(0, QtCore.Qt.UserRole, key)

            if os.path.exists(key):
                if key.startswith(current_maya_project):
                    top_level_item.setText(0, f'../{os.path.basename(os.path.split(os.path.normpath(key))[-1])}')
                else:
                    top_level_item.setText(0, key)
            else:
                top_level_item.setText(0, key)

            file_status = []

            for value in root_paths[key]:
                file_node, file_texture_name = value

                if files_filter.lower() in file_texture_name.lower():
                    item = QtWidgets.QTreeWidgetItem(top_level_item, [os.path.basename(file_texture_name)])
                    item.setData(0, QtCore.Qt.UserRole, (file_node, file_texture_name))

                    if os.path.exists(file_texture_name):
                        if file_texture_name.startswith(current_maya_project):
                            icon = QtGui.QIcon(self.icons['check-1.png'])
                            file_status.append('check')
                        else:
                            icon = QtGui.QIcon(self.icons['warning.png'])
                            file_status.append('warning')
                    else:
                        icon = QtGui.QIcon(self.icons['cross.png'])
                        file_status.append('cross')

                    item.setIcon(0, icon)

            file_status_cross_count = file_status.count('cross')
            file_status_warning_count = file_status.count('warning')

            if file_status_cross_count:
                icon = QtGui.QIcon(self.icons['cross.png'])
            elif file_status_warning_count:
                icon = QtGui.QIcon(self.icons['warning.png'])
            else:
                icon = QtGui.QIcon(self.icons['check-1.png'])

            top_level_item_count = top_level_item.childCount()

            if top_level_item_count:
                self.files_tree_widget.addTopLevelItem(top_level_item)
                top_level_item.setIcon(0, icon)
                top_level_item.setExpanded(True)
                top_level_item.setToolTip(0, f'<b>Files:</b> {top_level_item_count}')

    def update_images_items(self) -> None:
        """Updates images items."""
        current_maya_project = cmds.workspace(rootDirectory=True, query=True)
        source_images_project_path = os.path.join(current_maya_project, 'sourceimages')

        self.file_explorer_tree_widget.clear()

        if os.path.exists(source_images_project_path):
            self.add_image_file_children_item(dir_path=source_images_project_path, parent_item=None)

    def update_materials_items(self) -> None:
        """Updates the materials items."""
        render_engine = self.render_engine_combo_box.currentText()

        if render_engine == TextureConnectorUI.ARNOLD:
            material_type = 'aiStandardSurface'
        elif render_engine == TextureConnectorUI.REDSHIFT:
            material_type = 'RedshiftStandardMaterial'
        elif render_engine == TextureConnectorUI.V_RAY:
            material_type = 'VRayMtl'
        else:
            material_type = ''

        materials_filter = self.materials_filter_line_edit.text()
        materials = cmds.ls(materials=True)
        materials.sort()

        self.materials_list_widget.clear()

        for material in materials:
            if cmds.objectType(material, isType=material_type) and materials_filter.lower() in material.lower():
                item = QtWidgets.QListWidgetItem(material)
                item.setIcon(QtGui.QIcon(self.icons['bowling-ball.png']))
                self.materials_list_widget.addItem(item)

    def update_watched_paths(self) -> None:
        """Updates the watched paths."""
        current_maya_project = cmds.workspace(rootDirectory=True, query=True)
        source_images_path = os.path.join(current_maya_project, 'sourceimages')

        self.file_system_watcher.addPath(source_images_path)

    def showEvent(self, event):
        """Show event."""
        super(TextureConnectorUI, self).showEvent(event)

        renderer_engines_names = {
            'arnold': TextureConnectorUI.ARNOLD,
            'redshift': TextureConnectorUI.REDSHIFT,
            'vray': TextureConnectorUI.V_RAY}

        maya_current_render = cmds.getAttr('defaultRenderGlobals.currentRenderer')
        self.render_engine_combo_box.setCurrentText(renderer_engines_names.get(maya_current_render))

        self.set_current_maya_project_path_label()
        self.set_maya_project_status_image()
        self.set_render_engines()
        self.update_materials_items()
        self.update_images_items()
        self.update_watched_paths()
        self.update_files_items()


if __name__ == '__main__':
    texture_connector = TextureConnectorUI()
    texture_connector.show_window()
