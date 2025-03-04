# coding:utf-8
# coding:utf-8
from __future__ import print_function

import lnx_screw.core as c

c.Stage('resource_manifest').create_node_type_assign(
    '/resource_mocap_fbx_18', '/type/cache/mocap_fbx'
)