"""
========================================================================================================================
Name: edit_network_network_v_ray.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-05-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
from maurice_texture_connector.core.edit_material_network import EditMaterialNetwork


class EditMaterialNetworkVRay(EditMaterialNetwork):
    """Edit material network V-Ray."""
    MATERIAL_NODE = 'VRayMtl'

    BASE_COLOR_MATERIAL_INPUT_NAME = 'color'
    METALNESS_MATERIAL_INPUT_NAME = 'metalness'
    NORMAL_MATERIAL_INPUT_NAME = 'bumpMap'
    OPACITY_MATERIAL_INPUT_NAME = 'opacityMap'
    ROUGHNESS_MATERIAL_INPUT_NAME = 'reflectionGlossiness'

    def __init__(self, material: str):
        """Initializes class attributes."""
        super(EditMaterialNetworkVRay, self).__init__(material)
