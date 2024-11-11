"""
========================================================================================================================
Name: edit_material_network.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-10-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
from maya.api.OpenMaya import MGlobal
import maya.cmds as cmds

import maurice_texture_connector as maurice


class EditMaterialNetwork(object):
    """Edit material network."""
    MATERIAL_NODE = None

    BASE_COLOR_MATERIAL_INPUT_NAME = None
    EMISSIVE_MATERIAL_INPUT_NAME = None
    METALNESS_MATERIAL_INPUT_NAME = None
    NORMAL_MATERIAL_INPUT_NAME = None
    OPACITY_MATERIAL_INPUT_NAME = None
    ROUGHNESS_MATERIAL_INPUT_NAME = None

    def __init__(self, material: str) -> None:
        """Initializes class attributes."""
        self.material = material

        self.base_color_file_node = ''
        self.emissive_file_node = ''
        self.roughness_file_node = ''
        self.metalness_file_node = ''
        self.normal_file_node = ''
        self.height_file_node = ''
        self.opacity_file_node = ''

        self.get_material_file_nodes()

    def edit_base_color_file_texture_node(self, texture_path: str) -> None:
        """Edits the base color file texture node."""
        self.set_file_texture_name(file_node=self.base_color_file_node, texture_path=texture_path)

    def edit_emissive_file_texture_node(self, texture_path: str) -> None:
        """Edits the emissive file texture node."""
        self.set_file_texture_name(file_node=self.emissive_file_node, texture_path=texture_path)

    def edit_height_file_texture_node(self, texture_path: str) -> None:
        """Edits the height file texture node."""
        self.set_file_texture_name(file_node=self.height_file_node, texture_path=texture_path)

    def edit_metalness_file_texture_node(self, texture_path: str) -> None:
        """Edits the metalness file texture node."""
        self.set_file_texture_name(file_node=self.metalness_file_node, texture_path=texture_path)

    def edit_normal_file_texture_node(self, texture_path: str) -> None:
        """Edits the normal file texture node."""
        self.set_file_texture_name(file_node=self.normal_file_node, texture_path=texture_path)

    def edit_opacity_file_texture_node(self, texture_path: str) -> None:
        """Edits the opacity file texture node."""
        self.set_file_texture_name(file_node=self.opacity_file_node, texture_path=texture_path)

    def edit_roughness_file_texture_node(self, texture_path: str) -> None:
        """Edits the roughness file texture node."""
        self.set_file_texture_name(file_node=self.roughness_file_node, texture_path=texture_path)

    def get_base_color_color_space(self) -> str:
        """Gets the base color space."""
        return self.get_color_space(file_node=self.base_color_file_node)

    def get_base_color_file_texture_name(self) -> str:
        """Gets the base color file texture name."""
        return self.get_file_texture_name(file_node=self.base_color_file_node)

    @staticmethod
    def get_color_space(file_node: str) -> str:
        """Gets the color space."""
        return cmds.getAttr(f'{file_node}.colorSpace') if file_node else ''
    
    def get_emissive_color_space(self) -> str:
        """Gets the emissive color space."""
        return self.get_color_space(file_node=self.emissive_file_node)
    
    def get_emissive_file_texture_name(self) -> str:
        """Gets the emissive file texture name."""
        return self.get_file_texture_name(file_node=self.emissive_file_node)

    @staticmethod
    def get_file_node(channel_name: str, top_node: str) -> str:
        """Gets a file node."""
        if cmds.objectType(top_node, isType='file'):
            return top_node

        file_nodes = [node for node in cmds.listHistory(top_node) if cmds.objectType(node, isType='file')]

        if len(file_nodes) == 1:
            return file_nodes[0]
        else:
            if file_nodes:
                MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is more than one \'File\' node connected '
                                       f'to the \'{channel_name}\' channel.')

        return ''

    @staticmethod
    def get_file_texture_name(file_node: str) -> str:
        """Gets a file texture name."""
        if cmds.objExists(file_node):
            return cmds.getAttr(f'{file_node}.fileTextureName')

        return ''

    def get_height_color_space(self) -> str:
        """Gets the height color space."""
        return self.get_color_space(file_node=self.height_file_node)

    def get_height_file_texture_name(self) -> str:
        """Gets the height file texture name."""
        return self.get_file_texture_name(file_node=self.height_file_node)

    def get_material_file_nodes(self) -> None:
        """Gets the material file nodes."""
        material_connections = cmds.listHistory(self.material, levels=1)

        for material_connection in material_connections:
            if not material_connection == self.material:
                material_plug_nodes = cmds.listConnections(
                    material_connection,
                    source=False,
                    plugs=True,
                    type=self.MATERIAL_NODE)

                # Base color.
                if f'{self.material}.{self.BASE_COLOR_MATERIAL_INPUT_NAME}' in material_plug_nodes:
                    self.base_color_file_node = self.get_file_node(
                        channel_name='Base Color',
                        top_node=material_connection)

                # Roughness.
                if f'{self.material}.{self.ROUGHNESS_MATERIAL_INPUT_NAME}' in material_plug_nodes:
                    self.roughness_file_node = self.get_file_node(
                        channel_name='Roughness',
                        top_node=material_connection)

                # Metalness.
                if f'{self.material}.{self.METALNESS_MATERIAL_INPUT_NAME}' in material_plug_nodes:
                    self.metalness_file_node = self.get_file_node(
                        channel_name='Metalness',
                        top_node=material_connection)

                # Normal.
                if f'{self.material}.{self.NORMAL_MATERIAL_INPUT_NAME}' in material_plug_nodes:
                    self.normal_file_node = self.get_file_node(
                        channel_name='Normal',
                        top_node=material_connection)

                # Emissive.
                if f'{self.material}.{self.EMISSIVE_MATERIAL_INPUT_NAME}' in material_plug_nodes:
                    self.emissive_file_node = self.get_file_node(
                        channel_name='Emissive',
                        top_node=material_connection)

                # Opacity.
                if f'{self.material}.{self.OPACITY_MATERIAL_INPUT_NAME}' in material_plug_nodes:
                    self.opacity_file_node = self.get_file_node(
                        channel_name='Opacity',
                        top_node=material_connection)

        # Height.
        shading_engine = cmds.listConnections(self.material, source=False, type='shadingEngine')

        if shading_engine:
            shading_engine_connections = cmds.listConnections(
                f'{shading_engine[0]}.displacementShader',
                connections=True)

            if shading_engine_connections:
                for shading_engine_connection in shading_engine_connections:
                    if not cmds.nodeType(shading_engine_connection) == 'shadingEngine':
                        self.height_file_node = self.get_file_node(
                            channel_name='Height',
                            top_node=shading_engine_connection)

    def get_metalness_color_space(self) -> str:
        """Gets the metalness color space."""
        return self.get_color_space(file_node=self.metalness_file_node)

    def get_metalness_file_texture_name(self) -> str:
        """Gets the metalness file texture name."""
        return self.get_file_texture_name(file_node=self.metalness_file_node)

    def get_normal_color_space(self) -> str:
        """Gets the normal color space."""
        return self.get_color_space(file_node=self.normal_file_node)

    def get_normal_file_texture_name(self) -> str:
        """Gets the normal file texture name."""
        return self.get_file_texture_name(file_node=self.normal_file_node)

    def get_opacity_color_space(self) -> str:
        """Gets the opacity color space."""
        return self.get_color_space(file_node=self.opacity_file_node)

    def get_opacity_file_texture_name(self) -> str:
        """Gets the opacity file texture name."""
        return self.get_file_texture_name(file_node=self.opacity_file_node)

    def get_roughness_color_space(self) -> str:
        """Gets the roughness color space."""
        return self.get_color_space(file_node=self.roughness_file_node)

    def get_roughness_file_texture_name(self) -> str:
        """Gets the roughness file texture name."""
        return self.get_file_texture_name(file_node=self.roughness_file_node)

    @staticmethod
    def set_file_texture_name(file_node: str, texture_path: str) -> None:
        """Sets a file texture name."""
        if file_node:
            cmds.setAttr(f'{file_node}.fileTextureName', texture_path, type='string')
