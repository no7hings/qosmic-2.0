# coding:utf-8
import collections

import lxcontent.core as ctt_core
# katana
from ...core.wrap import *


class LookContent(object):
    GEOMETRY_PATH_NAME = 'path'
    MATERIAL_PATH_NAME = 'shop_materialpath'
    PROPERTY_LABEL = 'ar_'

    def __init__(self, root, look='default'):
        self._hou_root = hou.node(root)
        self._raw_content = ctt_core.Properties(None, collections.OrderedDict())
        self._look = look
        self._set_run_()

    def _set_run_(self):
        if self._hou_root is not None:
            self._hou_objs = self._hou_root.allNodes()
            self._hou_geos = []
            for hou_obj in self._hou_objs:
                if hou_obj.type().nameWithCategory() == 'Object/geo':
                    self._hou_geos.append(hou_obj)
            self._set_property_assign_update_()

    def _set_property_assign_update_(self):
        for hou_geo in self._hou_geos:
            render_node = hou_geo.renderNode()
            if render_node is not None:
                geometry = render_node.geometry()
                geometry_path_attr = geometry.findPrimAttrib(self.GEOMETRY_PATH_NAME)
                material_path_attr = geometry.findPrimAttrib(self.MATERIAL_PATH_NAME)
                if geometry_path_attr and material_path_attr:
                    property_set = collections.OrderedDict()
                    for parameter in hou_geo.parms():
                        parameter_name = parameter.name()
                        if parameter_name.startswith(self.PROPERTY_LABEL):
                            property_name = parameter_name[len(self.PROPERTY_LABEL):]
                            property_set[property_name] = parameter.eval()
                    for prim in geometry.iterPrims():
                        geometry_path = prim.stringAttribValue(geometry_path_attr)
                        material_path = prim.stringAttribValue(material_path_attr)
                        material_assign_key_path = '{}.material_assigns.{}'.format(self._look, geometry_path)
                        if not self._raw_content.get(material_assign_key_path):
                            self._raw_content.set(
                                material_assign_key_path,
                                material_path
                            )
                        property_assign_key_path = '{}.property_assigns.{}'.format(self._look, geometry_path)
                        if not self._raw_content.get(property_assign_key_path):
                            self._raw_content.set(
                                property_assign_key_path,
                                property_set
                            )

    def get_raw(self):
        return self._raw_content.value

    def __str__(self):
        return self._raw_content.__str__()
