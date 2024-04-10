# coding:utf-8
import collections

import lxcontent.core as ctt_core

import lxresource as bsc_resource


class AbsLookOpt(object):
    def __init__(self, *args):
        self._obj = args[0]

    @property
    def obj(self):
        return self._obj

    def get_material_paths(self):
        return [self.obj.get_input_port('material').get()]


class ShapeLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(ShapeLookOpt, self).__init__(*args)

        self._node_configure = ctt_core.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml('arnold/node')
        )
        self._node_configure.do_flatten()

        self._convert_configure = ctt_core.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml('arnold/convert')
        )
        self._convert_configure.do_flatten()

    def get_material_assigns(self):
        material_assigns = collections.OrderedDict()
        material_paths = self.get_material_paths()
        if material_paths:
            for material_path in material_paths:
                material_assigns['all'] = material_path
        return material_assigns

    def get_properties(self):
        properties = collections.OrderedDict()
        obj_type_name = self.obj.type.name
        keys = self._node_configure.get('properties.{}'.format(obj_type_name))
        for key in keys:
            port = self.obj.get_input_port(key)
            if port is not None:
                if port.get_is_enumerate():
                    raw = port.get_as_index()
                else:
                    raw = port.get()
                properties[key] = raw
        return properties

    def convert_render_properties_to(self, application):
        dic = collections.OrderedDict()
        dic_ = self.get_properties()
        convert_dict = self._convert_configure.get(
            'properties.to-{}.{}'.format(application, self.obj.type.name)
        )
        for k, v in convert_dict.items():
            if k in dic_:
                dic[v] = dic_[k]
        return dic

    def get_visibilities(self):
        visibilities = collections.OrderedDict()
        keys = self._node_configure.get('visibilities')
        for key in keys:
            port = self.obj.get_input_port(key)
            if port is not None:
                visibilities[key] = port.get()
        return visibilities

    def set_visibilities_convert_to(self, application):
        dic = collections.OrderedDict()
        dic_ = self.get_visibilities()
        convert_dict = self._convert_configure.get(
            'visibilities.to-{}'.format(application)
        )
        for k, v in convert_dict.items():
            if k in dic_:
                dic[v] = dic_[k]
        return dic
