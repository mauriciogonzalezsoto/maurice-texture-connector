"""
========================================================================================================================
Name: edit_material_network_redshift.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-05-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
from maurice_texture_connector.core.edit_material_network import EditMaterialNetwork


class EditMaterialNetworkRedshift(EditMaterialNetwork):
    """Edit material network Redshift."""
    MATERIAL_NODE = 'RedshiftStandardMaterial'

    BASE_COLOR_MATERIAL_INPUT_NAME = 'base_color'
    METALNESS_MATERIAL_INPUT_NAME = 'metalness'
    NORMAL_MATERIAL_INPUT_NAME = 'bump_input'
    OPACITY_MATERIAL_INPUT_NAME = 'opacity_color'
    ROUGHNESS_MATERIAL_INPUT_NAME = 'refl_roughness'

    def __init__(self, material: str):
        """Initializes class attributes."""
        super(EditMaterialNetworkRedshift, self).__init__(material)
