"""
========================================================================================================================
Name: create_material_network_arnold.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
import maya.cmds as cmds

from maurice_texture_connector.core.create_material_network import CreateMaterialNetwork


class CreateMaterialNetworkArnold(CreateMaterialNetwork):
    """Create material network Arnold."""
    MATERIAL_NODE = 'aiStandardSurface'

    BASE_COLOR_MATERIAL_INPUT_NAME = 'baseColor'
    EMISSIVE_MATERIAL_INPUT_NAME = 'emissionColor'
    METALNESS_MATERIAL_INPUT_NAME = 'metalness'
    NORMAL_MATERIAL_INPUT_NAME = 'normalCamera'
    OPACITY_MATERIAL_INPUT_NAME = 'opacity'
    ROUGHNESS_MATERIAL_INPUT_NAME = 'specularRoughness'

    TRIPLANAR_INPUT_NAME = 'input'
    TRIPLANAR_ALPHA_OUTPUT_NAME = 'outColorR'
    TRIPLANAR_COLOR_OUTPUT_NAME = 'outColor'

    def __init__(self) -> None:
        super(CreateMaterialNetworkArnold, self).__init__()

    def create_emissive_network(self) -> None:
        """Create the emissive network."""
        super(CreateMaterialNetworkArnold, self).create_emissive_network()

        cmds.setAttr(f'{self.material}.emission', 1)

    def create_triplanar_node_network(self, name: str) -> str:
        """Creates the triplanar node network."""
        super(CreateMaterialNetworkArnold, self).create_triplanar_node_network(name)

        triplanar_node = cmds.shadingNode('aiTriplanar', asTexture=True, name=f'{name}_aiTriplanar')

        cmds.setAttr(f'{triplanar_node}.coordSpace', 0)

        for axis in ['X', 'Y', 'Z']:
            cmds.connectAttr(f'{self.float_constant_node}.outFloat', f'{triplanar_node}.scale{axis}', force=True)

        return triplanar_node
