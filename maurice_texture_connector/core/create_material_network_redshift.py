"""
========================================================================================================================
Name: create_material_network_redshift.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-05-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
import maya.cmds as cmds

from maurice_texture_connector.core.create_material_network import CreateMaterialNetwork


class CreateMaterialNetworkRedshift(CreateMaterialNetwork):
    """Create material network Redshift."""
    MATERIAL_NODE = 'RedshiftStandardMaterial'

    BASE_COLOR_MATERIAL_INPUT_NAME = 'base_color'
    METALNESS_MATERIAL_INPUT_NAME = 'metalness'
    NORMAL_MATERIAL_INPUT_NAME = 'bump_input'
    OPACITY_MATERIAL_INPUT_NAME = 'opacity_color'
    ROUGHNESS_MATERIAL_INPUT_NAME = 'refl_roughness'

    TRIPLANAR_INPUT_NAME = 'imageX'
    TRIPLANAR_ALPHA_OUTPUT_NAME = 'outAlpha'
    TRIPLANAR_COLOR_OUTPUT_NAME = 'outColor'

    def __init__(self):
        super(CreateMaterialNetworkRedshift, self).__init__()

    def create_triplanar_node_network(self, name: str) -> str:
        """Creates the triplanar node network."""
        super(CreateMaterialNetworkRedshift, self).create_triplanar_node_network(name)

        triplanar_node = cmds.shadingNode('RedshiftTriPlanar', asTexture=True, name=f'{name}_RedshiftTriPlanar')

        cmds.setAttr(f'{triplanar_node}.projSpaceType', 0)

        cmds.connectAttr(f'{self.float_constant_node}.outFloat', f'{triplanar_node}.scale.scale0', force=True)
        cmds.connectAttr(f'{self.float_constant_node}.outFloat', f'{triplanar_node}.scale.scale1', force=True)
        cmds.connectAttr(f'{self.float_constant_node}.outFloat', f'{triplanar_node}.scale.scale2', force=True)

        return triplanar_node