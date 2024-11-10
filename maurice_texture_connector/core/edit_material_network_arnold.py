"""
========================================================================================================================
Name: edit_material_network_arnold.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-09-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
from maurice_texture_connector.core.edit_material_network import EditMaterialNetwork


class EditMaterialNetworkArnold(EditMaterialNetwork):
    """Edit material network Arnold."""
    MATERIAL_NODE = 'aiStandardSurface'

    BASE_COLOR_MATERIAL_INPUT_NAME = 'baseColor'
    EMISSIVE_MATERIAL_INPUT_NAME = 'emissionColor'
    METALNESS_MATERIAL_INPUT_NAME = 'metalness'
    NORMAL_MATERIAL_INPUT_NAME = 'normalCamera'
    OPACITY_MATERIAL_INPUT_NAME = 'opacity'
    ROUGHNESS_MATERIAL_INPUT_NAME = 'specularRoughness'

    def __init__(self, material: str):
        """Initializes class attributes."""
        super(EditMaterialNetworkArnold, self).__init__(material)
