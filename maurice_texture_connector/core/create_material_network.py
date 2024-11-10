"""
========================================================================================================================
Name: create_material_network.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-10-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
from maya.api.OpenMaya import MGlobal
import maya.cmds as cmds

from pathlib import Path
import os
import re

import maurice_texture_connector.utils as maurice_utils
import maurice_texture_connector as maurice


class CreateMaterialNetwork(object):
    """Create material network."""
    MATERIAL_NODE = None
    USE_BUMP_2D_NODE = True

    BASE_COLOR_MATERIAL_INPUT_NAME = None
    EMISSIVE_MATERIAL_INPUT_NAME = None
    METALNESS_MATERIAL_INPUT_NAME = None
    NORMAL_MATERIAL_INPUT_NAME = None
    OPACITY_MATERIAL_INPUT_NAME = None
    ROUGHNESS_MATERIAL_INPUT_NAME = None

    TRIPLANAR_INPUT_NAME = None
    TRIPLANAR_ALPHA_OUTPUT_NAME = None
    TRIPLANAR_COLOR_OUTPUT_NAME = None

    def __init__(self):
        """Initializes class attributes."""
        self.file_digits_suffix = None
        self.file_stem = None
        self.name = None
        self.use_triplanar = False
        self.use_multi_tiled = False

        # Maya node class variables.
        self.float_constant_node = ''
        self.material = ''
        self.place_2d_texture_node = ''
        self.shading_engine_node = ''

        # Base color class variables.
        self.base_color_file_node = ''
        self.base_color_file_paths = []
        self.base_color_suffix = ''
        self.base_color_triplanar_node = ''
        self.is_base_color_enabled = False

        # Roughness class variables.
        self.roughness_file_node = ''
        self.roughness_file_paths = []
        self.roughness_suffix = ''
        self.roughness_triplanar_node = ''
        self.is_roughness_enabled = False

        # Metalness class variables.
        self.metalness_file_node = ''
        self.metalness_file_paths = []
        self.metalness_suffix = ''
        self.metalness_triplanar_node = ''
        self.is_metalness_enabled = False

        # Normal class variables.
        self.normal_file_node = ''
        self.normal_file_paths = []
        self.normal_suffix = ''
        self.normal_triplanar_node = ''
        self.is_normal_enabled = False

        # Height class variables.
        self.height_displacement_shader_node = ''
        self.height_file_node = ''
        self.height_file_paths = []
        self.height_suffix = ''
        self.height_triplanar_node = ''
        self.is_height_enabled = False

        # Emissive class variables.
        self.emissive_file_node = ''
        self.emissive_file_paths = []
        self.emissive_suffix = ''
        self.emissive_triplanar_node = ''
        self.is_emissive_enabled = False

        # Opacity class variables.
        self.opacity_file_node = ''
        self.opacity_file_paths = []
        self.opacity_suffix = ''
        self.opacity_triplanar_node = ''
        self.is_opacity_enabled = False

    @staticmethod
    def are_plugins_loaded(render_engine_plugin_name: str, use_triplanar: bool) -> bool:
        """Checks if the required plugins are loaded."""
        plugins_loaded = cmds.pluginInfo(listPlugins=True, query=True)

        if render_engine_plugin_name not in plugins_loaded:
            MGlobal.displayError(f'[{maurice.TEXTURE_CONNECTOR}] \'{render_engine_plugin_name}\' plugin is not loaded.')
            return False
        elif 'lookdevKit' not in plugins_loaded and use_triplanar:
            MGlobal.displayError(f'[{maurice.TEXTURE_CONNECTOR}] \'lookdevKit\' plugin is not loaded.')
            return False
        else:
            return True

    def create(self, name: str, image_path: str, use_texture_base_name: bool, use_triplanar: bool) -> None:
        """Creates the material network."""
        self.name = name
        self.use_triplanar = use_triplanar

        if not self.name and not use_texture_base_name:
            MGlobal.displayError(f'[{maurice.TEXTURE_CONNECTOR}] No name for the material.')
            return
        elif not maurice_utils.is_image(image_path):
            MGlobal.displayError(f'[{maurice.TEXTURE_CONNECTOR}] The file is not an image.')
            return
        elif use_texture_base_name:
            self.name = self.get_texture_base_name(image_path)

            if not self.name:
                MGlobal.displayError(f'[{maurice.TEXTURE_CONNECTOR}] Suffix not found.')
                return

        objects = cmds.ls(long=True, selection=True)

        cmds.undoInfo(chunkName='mgMaterialNetwork', openChunk=True)

        self.get_textures_paths(image_path)
        self.create_material()

        if self.is_base_color_enabled and self.base_color_file_paths:
            self.create_base_color_network()

        if self.is_roughness_enabled and self.roughness_file_paths:
            self.create_roughness_network()

        if self.is_metalness_enabled and self.metalness_file_paths:
            self.create_metalness_network()

        if self.is_normal_enabled and self.normal_file_paths:
            self.create_normal_network()

        if self.is_height_enabled and self.height_file_paths:
            self.create_height_network()

        if self.is_emissive_enabled and self.emissive_file_paths:
            self.create_emissive_network()

        if self.is_opacity_enabled and self.opacity_file_paths:
            self.create_opacity_network()

        cmds.select(clear=True)

        if objects:
            cmds.sets(objects, edit=True, forceElement=self.shading_engine_node)

        cmds.select(self.material, replace=True)

        MGlobal.displayInfo(f'[{maurice.TEXTURE_CONNECTOR}] Created material network successfully.')

        cmds.undoInfo(chunkName='mgMaterialNetwork', closeChunk=True)

    def create_standard_network(self, material_input_name: str, suffix: str, out_alpha: bool = False) -> tuple:
        """Creates the standard network."""
        name = f'{self.name}_{suffix}'

        file_node = self.create_file_node_network(name=name)
        triplanar_node = ''

        if self.use_triplanar:
            triplanar_node = self.create_triplanar_node_network(name=name)
            out = self.TRIPLANAR_ALPHA_OUTPUT_NAME if out_alpha else self.TRIPLANAR_COLOR_OUTPUT_NAME

            cmds.connectAttr(
                f'{file_node}.outColor',
                f'{triplanar_node}.{self.TRIPLANAR_INPUT_NAME}',
                force=True)

            cmds.connectAttr(
                f'{triplanar_node}.{out}',
                f'{self.material}.{material_input_name}',
                force=True)
        else:
            out = 'outAlpha' if out_alpha else 'outColor'

            cmds.connectAttr(
                f'{file_node}.{out}',
                f'{self.material}.{material_input_name}',
                force=True)

        return file_node, triplanar_node

    def create_base_color_network(self) -> None:
        """Create the base color network."""
        self.base_color_file_node, self.base_color_triplanar_node = self.create_standard_network(
            material_input_name=self.BASE_COLOR_MATERIAL_INPUT_NAME,
            suffix=self.base_color_suffix)

        if self.base_color_file_paths:
            self.set_color_texture_file_node_settings(
                file_node=self.base_color_file_node,
                file_texture_name=self.base_color_file_paths[0],
                use_multi_tiled=self.use_multi_tiled)

    def create_bump_2d_node(self) -> str:
        """Creates the bump 2D node."""
        bump_2d_node = cmds.shadingNode('bump2d', asUtility=True, name=f'{self.name}_bump2d')
        cmds.setAttr(f'{bump_2d_node}.bumpInterp', 1)

        return bump_2d_node

    def create_emissive_network(self) -> None:
        """Create the emissive network."""
        self.emissive_file_node, self.emissive_triplanar_node = self.create_standard_network(
            material_input_name=self.EMISSIVE_MATERIAL_INPUT_NAME,
            suffix=self.emissive_suffix)

        if self.emissive_file_paths:
            self.set_color_texture_file_node_settings(
                file_node=self.emissive_file_node,
                file_texture_name=self.emissive_file_paths[0],
                use_multi_tiled=self.use_multi_tiled)

    def create_file_node_network(self, name: str) -> str:
        """Creates the file node network."""
        if not cmds.objExists(self.place_2d_texture_node):
            self.create_place_2d_texture_node()

        file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=f'{name}_file')

        attributes = (
            '.coverage',
            '.translateFrame',
            '.rotateFrame',
            '.mirrorU',
            '.mirrorV',
            '.stagger',
            '.wrapU',
            '.wrapV',
            '.repeatUV',
            '.offset',
            '.rotateUV',
            '.noiseUV',
            '.vertexUvOne',
            '.vertexUvTwo',
            '.vertexUvThree',
            '.vertexCameraOne'
        )

        for attr in attributes:
            cmds.connectAttr(f'{self.place_2d_texture_node}{attr}', f'{file_node}{attr}', force=True)

        cmds.connectAttr(f'{self.place_2d_texture_node}.outUvFilterSize', f'{file_node}.uvFilterSize')
        cmds.connectAttr(f'{self.place_2d_texture_node}.outUV', f'{file_node}.uv')

        return file_node

    def create_float_constant_node(self) -> None:
        """Creates the float constant node."""
        self.float_constant_node = cmds.shadingNode('floatConstant', asUtility=True, name=f'{self.name}_floatConstant')

    def create_height_network(self) -> None:
        """Creates the height network."""
        name = f'{self.name}_{self.height_suffix}'

        self.height_displacement_shader_node = cmds.shadingNode(
            'displacementShader',
            asShader=True,
            name=f'{name}_displacementShader')

        self.height_file_node = self.create_file_node_network(name=name)

        if self.use_triplanar:
            self.height_triplanar_node = self.create_triplanar_node_network(name)

            cmds.connectAttr(
                f'{self.height_file_node}.outColor',
                f'{self.height_triplanar_node}.{self.TRIPLANAR_INPUT_NAME}',
                force=True)
            cmds.connectAttr(
                f'{self.height_triplanar_node}.{self.TRIPLANAR_ALPHA_OUTPUT_NAME}',
                f'{self.height_displacement_shader_node}.displacement',
                force=True)
        else:
            cmds.connectAttr(
                f'{self.height_file_node}.outAlpha',
                f'{self.height_displacement_shader_node}.displacement',
                force=True)

        cmds.connectAttr(
            f'{self.height_displacement_shader_node}.displacement',
            f'{self.shading_engine_node}.displacementShader',
            force=True)

        if self.height_file_paths:
            self.set_data_texture_file_node_settings(
                file_node=self.height_file_node,
                file_texture_name=self.height_file_paths[0],
                use_multi_tiled=self.use_multi_tiled)

    def create_material(self):
        """Creates the material."""
        self.material = cmds.shadingNode(
            self.MATERIAL_NODE,
            asShader=True,
            name=f'{self.name}_{self.MATERIAL_NODE}')

        self.shading_engine_node = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{self.name}SG')

        cmds.connectAttr(
            f'{self.material}.outColor',
            f'{self.shading_engine_node}.surfaceShader',
            force=True)

    def create_metalness_network(self) -> None:
        """Creates the metalness network."""
        self.metalness_file_node, self.metalness_triplanar_node = self.create_standard_network(
            material_input_name=self.METALNESS_MATERIAL_INPUT_NAME,
            out_alpha=True,
            suffix=self.metalness_suffix)

        if self.metalness_file_paths:
            self.set_data_texture_file_node_settings(
                file_node=self.metalness_file_node,
                file_texture_name=self.metalness_file_paths[0],
                use_multi_tiled=self.use_multi_tiled)

    def create_normal_network(self) -> None:
        """Crates the normal network."""
        name = f'{self.name}_{self.normal_suffix}'
        bump_2d_node = ''

        self.normal_file_node = self.create_file_node_network(name=name)

        if self.USE_BUMP_2D_NODE:
            bump_2d_node = self.create_bump_2d_node()

            cmds.connectAttr(f'{self.normal_file_node}.outColorR',
                             f'{bump_2d_node}.bumpValue',
                             force=True)

        if self.use_triplanar:
            self.normal_triplanar_node = self.create_triplanar_node_network(name=name)

            if self.USE_BUMP_2D_NODE:
                cmds.connectAttr(f'{bump_2d_node}.outNormal',
                                 f'{self.normal_triplanar_node}.{self.TRIPLANAR_INPUT_NAME}',
                                 force=True)
            else:
                cmds.connectAttr(f'{self.normal_file_node}.outColor',
                                 f'{self.normal_triplanar_node}.{self.TRIPLANAR_INPUT_NAME}',
                                 force=True)

            cmds.connectAttr(f'{self.normal_triplanar_node}.outColor',
                             f'{self.material}.{self.NORMAL_MATERIAL_INPUT_NAME}',
                             force=True)
        else:
            if self.USE_BUMP_2D_NODE:
                cmds.connectAttr(f'{bump_2d_node}.outNormal',
                                 f'{self.material}.{self.NORMAL_MATERIAL_INPUT_NAME}',
                                 force=True)
            else:
                cmds.connectAttr(f'{self.normal_file_node}.outColor',
                                 f'{self.material}.{self.NORMAL_MATERIAL_INPUT_NAME}',
                                 force=True)

        if self.normal_file_paths:
            self.set_data_texture_file_node_settings(
                file_node=self.normal_file_node,
                file_texture_name=self.normal_file_paths[0],
                use_multi_tiled=self.use_multi_tiled)

    def create_place_2d_texture_node(self) -> None:
        """Creates the place 2D texture node."""
        self.place_2d_texture_node = cmds.shadingNode(
            'place2dTexture',
            asUtility=True,
            name=f'{self.name}_place2dTexture')

    def create_opacity_network(self) -> None:
        """Creates the opacity network."""
        self.opacity_file_node, self.opacity_triplanar_node = self.create_standard_network(
            material_input_name=self.OPACITY_MATERIAL_INPUT_NAME,
            suffix=self.opacity_suffix)

        if self.opacity_file_paths:
            self.set_data_texture_file_node_settings(
                file_node=self.opacity_file_node,
                file_texture_name=self.opacity_file_paths[0],
                use_multi_tiled=self.use_multi_tiled)

    def create_roughness_network(self) -> None:
        """Creates the roughness network."""
        self.roughness_file_node, self.roughness_triplanar_node = self.create_standard_network(
            material_input_name=self.ROUGHNESS_MATERIAL_INPUT_NAME,
            out_alpha=True,
            suffix=self.roughness_suffix)

        if self.roughness_file_paths:
            self.set_data_texture_file_node_settings(
                file_node=self.roughness_file_node,
                file_texture_name=self.roughness_file_paths[0],
                use_multi_tiled=self.use_multi_tiled)

    def create_triplanar_node_network(self, name: str) -> any:
        """Creates the triplanar node network."""
        if not cmds.objExists(self.float_constant_node):
            self.create_float_constant_node()

    @staticmethod
    def extract_pattern_match(file_stem: str, pattern_suffix: str) -> list:
        """Extracts the patter match."""
        pattern = re.compile(f'_{pattern_suffix}(_|$)', re.IGNORECASE)
        pattern_split = pattern.split(file_stem, 1)

        return pattern_split

    def get_material(self):
        """Gets the material."""
        return self.material

    def get_texture_base_name(self, file_path: str) -> str:
        """Gets the texture base name."""
        self.get_multi_tiled_mode(file_path)

        suffixes = (
            self.base_color_suffix,
            self.roughness_suffix,
            self.metalness_suffix,
            self.normal_suffix,
            self.height_suffix,
            self.emissive_suffix,
            self.opacity_suffix
        )

        for suffix in suffixes:
            pattern_split = self.extract_pattern_match(self.file_stem, suffix)

            if len(pattern_split) > 1:
                base_name = pattern_split[0]

                return base_name

        return ''

    def get_textures_paths(self, texture_path: str) -> None:
        """Gets the textures paths."""
        self.base_color_file_paths.clear()
        self.roughness_file_paths.clear()
        self.metalness_file_paths.clear()
        self.normal_file_paths.clear()
        self.height_file_paths.clear()
        self.emissive_file_paths.clear()
        self.opacity_file_paths.clear()

        texture_folder = os.path.dirname(texture_path)
        texture_base_name = self.get_texture_base_name(texture_path)
        files_in_folder = maurice_utils.get_files_in_folder(texture_folder)

        for file in files_in_folder.items():
            file_short_name, file_path = file

            if maurice_utils.is_image(file_path):
                file_stem = Path(file_short_name).stem

                if self.use_multi_tiled:
                    file_stem = file_stem.removesuffix(f'.{self.file_digits_suffix}')

                if file_stem.startswith(texture_base_name):
                    base_color_pattern_split = self.extract_pattern_match(file_stem, self.base_color_suffix)
                    roughness_pattern_split = self.extract_pattern_match(file_stem, self.roughness_suffix)
                    metalness_pattern_split = self.extract_pattern_match(file_stem, self.metalness_suffix)
                    normal_pattern_split = self.extract_pattern_match(file_stem, self.normal_suffix)
                    height_pattern_split = self.extract_pattern_match(file_stem, self.height_suffix)
                    emissive_pattern_split = self.extract_pattern_match(file_stem, self.emissive_suffix)
                    opacity_pattern_split = self.extract_pattern_match(file_stem, self.opacity_suffix)

                    if len(base_color_pattern_split) > 1:
                        self.base_color_file_paths.append(file_path)

                    if len(roughness_pattern_split) > 1:
                        self.roughness_file_paths.append(file_path)

                    if len(metalness_pattern_split) > 1:
                        self.metalness_file_paths.append(file_path)

                    if len(normal_pattern_split) > 1:
                        self.normal_file_paths.append(file_path)

                    if len(height_pattern_split) > 1:
                        self.height_file_paths.append(file_path)

                    if len(emissive_pattern_split) > 1:
                        self.emissive_file_paths.append(file_path)

                    if len(opacity_pattern_split) > 1:
                        self.opacity_file_paths.append(file_path)

    def get_multi_tiled_mode(self, file_path: str) -> None:
        """Gets if the texture is multi tiled."""
        self.file_stem = Path(file_path).stem
        self.file_stem, *digits_suffix = self.file_stem.rsplit('.', 1)

        if digits_suffix and digits_suffix[0].isdigit():
            self.file_digits_suffix = digits_suffix[0]
            self.file_stem = self.file_stem.removesuffix(f'.{self.file_digits_suffix}')
            self.use_multi_tiled = True

    def set_base_color_settings(self, enabled: bool, suffix: str) -> None:
        """Sets base color settings."""
        if not suffix:
            MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is no suffix for base color.')

        self.base_color_suffix = suffix
        self.is_base_color_enabled = enabled

    def set_color_texture_file_node_settings(self, file_node: str, file_texture_name: str,
                                             use_multi_tiled: bool) -> None:
        """Sets the color texture file node settings."""
        self.set_texture_file_node_settings(
            file_node=file_node,
            file_texture_name=file_texture_name,
            use_multi_tiled=use_multi_tiled)

    def set_data_texture_file_node_settings(self, file_node: str, file_texture_name: str,
                                            use_multi_tiled: bool) -> None:
        """Sets the data texture file node settings."""
        self.set_texture_file_node_settings(
            file_node=file_node,
            file_texture_name=file_texture_name,
            use_multi_tiled=use_multi_tiled)

        cmds.setAttr(f'{file_node}.alphaIsLuminance', True)
        cmds.setAttr(f'{file_node}.colorSpace', 'Raw', type='string')

    def set_emissive_settings(self, enabled: bool, suffix: str) -> None:
        """Sets emissive settings."""
        if not suffix:
            MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is no suffix for emissive.')

        self.emissive_suffix = suffix
        self.is_emissive_enabled = enabled

    def set_height_settings(self, enabled: bool, suffix: str) -> None:
        """Sets height settings."""
        if not suffix:
            MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is no suffix for height')

        self.height_suffix = suffix
        self.is_height_enabled = enabled

    def set_metalness_settings(self, enabled: bool, suffix: str) -> None:
        """Sets metalness settings."""
        if not suffix:
            MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is no suffix for metalness.')

        self.metalness_suffix = suffix
        self.is_metalness_enabled = enabled

    def set_normal_settings(self, enabled: bool, suffix: str) -> None:
        """Sets normal settings."""
        if not suffix:
            MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is no suffix for normal')

        self.normal_suffix = suffix
        self.is_normal_enabled = enabled

    def set_opacity_settings(self, enabled: bool, suffix: str) -> None:
        """Sets opacity settings."""
        if not suffix:
            MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is no suffix for opacity.')

        self.opacity_suffix = suffix
        self.is_opacity_enabled = enabled

    def set_roughness_settings(self, enabled: bool, suffix: str) -> None:
        """Sets roughness settings."""
        if not suffix:
            MGlobal.displayWarning(f'[{maurice.TEXTURE_CONNECTOR}] There is no suffix for roughness.')

        self.roughness_suffix = suffix
        self.is_roughness_enabled = enabled

    @staticmethod
    def set_texture_file_node_settings(file_node: str, file_texture_name: str, use_multi_tiled: bool) -> None:
        """Sets the texture file node settings."""
        cmds.setAttr(f'{file_node}.ignoreColorSpaceFileRules', True)
        cmds.setAttr(f'{file_node}.fileTextureName', file_texture_name, type='string')

        if use_multi_tiled:
            cmds.setAttr(f'{file_node}.uvTilingMode', 3)
