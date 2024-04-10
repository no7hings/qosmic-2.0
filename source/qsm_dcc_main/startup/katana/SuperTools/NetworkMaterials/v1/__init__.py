# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/v1/__init__.py
# Compiled at: 2021-06-28 21:25:19
"""
Module containing methods to locally import NetworkMaterialCreate and
NetworkMaterialEdit parameter editor classes.
"""
from NetworkMaterialCreateNode import NetworkMaterialCreateNode

def GetNetworkMaterialCreateEditor():
    """
    @rtype: C{NetworkMaterialCreateEditor} class
    @return: Class of editor tab for NetworkMaterialCreate nodes.
    """
    from NetworkMaterialCreateEditor import NetworkMaterialCreateEditor
    return NetworkMaterialCreateEditor


def GetNetworkMaterialEditEditor():
    """
    @rtype: C{NetworkMaterialEditEditor} class
    @return: Class of editor tab for NetworkMaterialEdit nodes.
    """
    from NetworkMaterialEditEditor import NetworkMaterialEditEditor
    return NetworkMaterialEditEditor