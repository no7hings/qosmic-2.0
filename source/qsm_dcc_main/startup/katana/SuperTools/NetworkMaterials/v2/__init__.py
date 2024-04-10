# uncompyle6 version 3.8.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Oct 30 2018, 23:45:53) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
# Warning: this version of Python has problems handling the Python 3 byte type in constants properly.

# Embedded file name: SuperTools/NetworkMaterials/v1/__init__.py
# Compiled at: 2022-08-18 19:44:51
"""
Module containing methods to locally import NetworkMaterialCreate and
NetworkMaterialEdit parameter editor classes.
"""
from __future__ import absolute_import
from .NetworkMaterialCreateNode import NetworkMaterialCreateNode

def GetNetworkMaterialCreateEditor():
    """
    @rtype: C{NetworkMaterialCreateEditor} class
    @return: Class of editor tab for NetworkMaterialCreate nodes.
    """
    from .NetworkMaterialCreateEditor import NetworkMaterialCreateEditor
    return NetworkMaterialCreateEditor


def GetNetworkMaterialEditEditor():
    """
    @rtype: C{NetworkMaterialEditEditor} class
    @return: Class of editor tab for NetworkMaterialEdit nodes.
    """
    from .NetworkMaterialEditEditor import NetworkMaterialEditEditor
    return NetworkMaterialEditEditor