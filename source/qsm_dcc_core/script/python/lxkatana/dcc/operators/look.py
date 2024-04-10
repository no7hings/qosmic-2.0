# coding:utf-8
import re

import lxbasic.core as bsc_core

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxcontent.core as ctt_core


class AndShaderOpt(bsc_dcc_abstracts.AbsNodeOpt):
    def __init__(self, *args, **kwargs):
        super(AndShaderOpt, self).__init__(*args, **kwargs)
        
    def get_type_name(self):
        return self._obj.get_port('nodeType').get()

    def set_type_name(self, obj_type_name):
        self._obj.get_port('nodeType').set(obj_type_name)
        self._obj.ktn_obj.checkDynamicParameters()

    def set_create(self, obj_type_name):
        ktn_obj, is_create = self._obj.get_dcc_instance('ArnoldShadingNode')
        self._obj.get_port('nodeType').set(obj_type_name)
        self._obj.ktn_obj.checkDynamicParameters()
        return is_create

    def get_enable_port(self, and_port_path):
        return self._obj.get_port(
            'parameters.{}.enable'.format(and_port_path)
        )

    def get_value_port(self, and_port_path):
        return self._obj.get_port(
            'parameters.{}.value'.format(and_port_path)
        )

    def get_port_value(self, and_port_path):
        port = self.get_value_port(and_port_path)
        if port:
            return port.get()

    def get(self, key):
        return self.get_port_value(key)

    def set_port_value(self, and_port_path, value):
        self.get_enable_port(and_port_path).set(True)
        self.get_value_port(and_port_path).set(value)

    def set(self, key, value):
        self.set_port_value(key, value)

    def set_colour_by_type_name(self):
        type_name = self.get_type_name()
        r, g, b = bsc_core.RawTextOpt(type_name).to_rgb(maximum=1)
        attributes = self._obj.ktn_obj.getAttributes()
        attributes['ns_colorr'] = r
        attributes['ns_colorg'] = g
        attributes['ns_colorb'] = b
        self._obj.ktn_obj.setAttributes(attributes)

    def set_duplicate_with_source(self):
        print self.get_properties()
        # source_objs = self._obj.get_all_source_objs()
        # for source_obj in source_objs:
        #     print source_obj.get_properties()

    def get_properties(self):
        properties = ctt_core.Properties(self)
        properties.set(
            'type', self.get_type_name(),
        )
        properties.set(
            'path', self._obj.path,
        )
        attributes = self._obj.get_attributes()
        properties.set(
            'attributes', attributes.value
        )
        return properties

    def get_ports(self):
        return self._obj.get_port('parameters').get_children()

    def get_attributes(self):
        attributes = ctt_core.Properties(self)
        ports = self.get_ports()
        for port in ports:
            enable_port = port.get_child('enable')
            value_port = port.get_child('value')
            if enable_port is not None:
                attributes.set(
                    enable_port.port_path, enable_port.get()
                )
                attributes.set(
                    value_port.port_path, value_port.get()
                )
        return attributes

    def get_port_source(self, and_port_path):
        return self._obj.get_input_port(and_port_path).get_source()

    def set_port_source(self, and_port_path, source, validation=False):
        self._obj.get_input_port(and_port_path).set_source(source, validation)

    def set_port_source_disconnect(self, and_port_path):
        self._obj.get_input_port(and_port_path).set_disconnect()

    def get_port_targets(self, and_port_path):
        return self._obj.get_output_port(and_port_path).get_targets()

    def set_port_target(self, and_port_path, target, validation=False):
        self._obj.get_output_port(and_port_path).set_target(target, validation)

    def set_port_targets_disconnect(self, and_port_path):
        self._obj.get_output_port(and_port_path).set_disconnect()


class MaterialOpt(bsc_dcc_abstracts.AbsNodeOpt):
    def __init__(self, *args, **kwargs):
        super(MaterialOpt, self).__init__(*args, **kwargs)

    def get_sg_path(self):
        location = self.obj.get_parent().get_port('rootLocation').get()
        name = self.obj.name
        return '{}/{}'.format(location.rstrip('/'), name)


class MaterialAssignOpt(bsc_dcc_abstracts.AbsNodeOpt):
    def __init__(self, *args, **kwargs):
        super(MaterialAssignOpt, self).__init__(*args, **kwargs)

    def get_material_path(self):
        return self.obj.get('args.materialAssign.value')

    def set_material_path(self, path):
        self.obj.set('args.materialAssign.value', path)

    def assign_material(self, material):
        self.set_material_path(
            MaterialOpt(material).get_sg_path()
        )

    def get_geometry_paths(self):
        dcc_node = self.obj
        p = '[(](.*?)[)]'
        cel_port = dcc_node.get_port('CEL')
        value = cel_port.get()
        if value:
            _ = re.findall(p, value)
            if _:
                return _[0].split(' ')
            else:
                return [value]
        return []

    def set_geometry_paths(self, paths):
        pass

    def set_geometry_path_append(self, path):
        dcc_node = self.obj
        p = '[(](.*?)[)]'
        cel_port = dcc_node.get_port('CEL')
        value = cel_port.get()
        if value:
            _ = re.findall(p, value)
            if _:
                cel_value = '({} {})'.format(_[0], path)
            else:
                cel_value = '({} {})'.format(value, path)
        else:
            cel_value = path
        cel_port.set(cel_value)


class PropertiesAssignOpt(bsc_dcc_abstracts.AbsNodeOpt):
    def __init__(self, *args, **kwargs):
        super(PropertiesAssignOpt, self).__init__(*args, **kwargs)

    def get_geometry_paths(self):
        dcc_node = self.obj
        p = '[(](.*?)[)]'
        cel_port = dcc_node.get_port('CEL')
        value = cel_port.get()
        if value:
            _ = re.findall(p, value)
            if _:
                return _[0].split(' ')
            else:
                return [value]
        return MaterialAssignOpt(self.obj).get_geometry_paths()

    def set_geometry_paths(self, paths):
        pass

    def set_geometry_path_append(self, path):
        MaterialAssignOpt(self.obj).set_geometry_path_append(path)

    def set_properties(self, properties):
        pass

    def set_visibilities(self, visibilities):
        pass
