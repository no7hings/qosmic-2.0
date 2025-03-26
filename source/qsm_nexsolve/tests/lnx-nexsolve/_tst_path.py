# coding:utf-8
import json

import lnx_nexsolve.core.path as p

paths = [
    '/',
    '/root',
    '/root/premiere',
    '/root/premiere/xml',
    '/root/premiere/xml/main',
    '/root/maya',
    '/root/maya/scene',
    '/root/maya/scene/A001_001_001',
    '/root/maya/scene/A001_001_002',
    '/root/maya/scene/A001_001_003',
    '/root/houdini',
    '/root/houdini/scene',
    '/root/houdini/scene/A001_001_003',
]


# print(p.Selection.fetchall(paths, '/root/m*'))
# print(p.Selection.fetchall(paths, '/root/*/scene//*_001_*'))


# path = p.PathOpt('/root/maya/scene/A001_001_001')
#
# print(path.get_parent())
# print(path.to_components())
# print(path.get_ancestors())

