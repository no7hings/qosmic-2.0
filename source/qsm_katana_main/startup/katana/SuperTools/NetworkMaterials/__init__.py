# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/__init__.py
# Compiled at: 2021-06-28 21:25:16
"""
Copyright (c) 2019 The Foundry Visionmongers Ltd. All Rights Reserved.
"""
import sys

import os

c = os.environ['KATANA_VERSION'] > '4.5'

try:
    if c is True:
        import v2 as NetworkMaterials
        sys.stdout.write('"NetworkMaterials" use version 2.0' + '\n')
    else:
        import v1 as NetworkMaterials
        sys.stdout.write('"NetworkMaterials" use version 1.0' + '\n')
except ImportError:
    NetworkMaterialCreate = None
    NetworkMaterialEdit = None

try:
    if c is True:
        from v2.NetworkMaterialCreateNode import NetworkMaterialCreateNode
    else:
        from v1.NetworkMaterialCreateNode import NetworkMaterialCreateNode
except ImportError:
    NetworkMaterialCreateNode = None

try:
    if c is True:
        from v2.NetworkMaterialEditNode import NetworkMaterialEditNode
    else:
        from v1.NetworkMaterialEditNode import NetworkMaterialEditNode
except ImportError:
    NetworkMaterialEditNode = None

PluginRegistry = []
if NetworkMaterialCreateNode:
    PluginRegistry.append(('SuperTool',
     2,
     'NetworkMaterialCreate',
     (
      NetworkMaterialCreateNode,
      NetworkMaterials.GetNetworkMaterialCreateEditor)))
if NetworkMaterialEditNode:
    PluginRegistry.append(('SuperTool',
     2,
     'NetworkMaterialEdit',
     (
      NetworkMaterialEditNode,
      NetworkMaterials.GetNetworkMaterialEditEditor)))