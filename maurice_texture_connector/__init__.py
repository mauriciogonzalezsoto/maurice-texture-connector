"""
========================================================================================================================
Name: __init__.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-05-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
import maya.api.OpenMaya as om

import sys

from maurice_texture_connector.utils import get_ppi


if sys.version_info.major < 3:
    om.MGlobal.displayError('[Maurice] The current version of Python is not supported.')
    sys.exit()


AUTHOR = 'Mauricio Gonzalez Soto'
VERSION = '1.0.0'
PPI = get_ppi()

TEXTURE_CONNECTOR_WINDOW_NAME = 'mauriceTextureConnector'
TEXTURE_CONNECTOR = 'Texture Connector'

from maurice_texture_connector.ui.texture_connector_ui import TextureConnectorUI
