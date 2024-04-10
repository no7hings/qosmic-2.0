# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# katana
from ... import core as ktn_core

from ... import abstracts as ktn_abstracts
# katana dcc
from . import node as ktn_dcc_obj_node


# noinspection PyUnusedLocal
class AndShader(ktn_abstracts.AbsKtnObj):
    DCC_PORT_CLS = ktn_dcc_obj_node.Port
    DCC_CONNECTION_CLS = ktn_dcc_obj_node.Connection

    def __init__(self, path):
        super(AndShader, self).__init__(path)

    def get_shader_type_name(self):
        return self.get_port('nodeType').get()

    def set_shader_type_name(self, obj_type_name):
        self.get_port('nodeType').set(obj_type_name)
        self.ktn_obj.checkDynamicParameters()

    def set_shader_create(self, obj_type_name):
        self.get_dcc_instance('ArnoldShadingNode')
        self.get_port('nodeType').set(obj_type_name)
        self.ktn_obj.checkDynamicParameters()

    def get_shader_enable_port(self, port_name):
        return self.get_port(
            'parameters.{}.enable'.format(port_name)
        )

    def get_shader_value_port(self, port_name):
        return self.get_port(
            'parameters.{}.value'.format(port_name)
        )

    def get_shader_port_value(self, port_name):
        port = self.get_shader_value_port(port_name)
        if port:
            return port.get()

    def set_shader_port_value(self, port_name, value):
        self.get_shader_enable_port(port_name).set(True)
        self.get_shader_value_port(port_name).set(value)

    def set_colour_by_type_name(self):
        type_name = self.get_shader_type_name()
        r, g, b = bsc_core.RawTextOpt(type_name).to_rgb(maximum=1)
        attributes = self.ktn_obj.getAttributes()
        attributes['ns_colorr'] = r
        attributes['ns_colorg'] = g
        attributes['ns_colorb'] = b
        self.ktn_obj.setAttributes(attributes)

    def set_duplicate_with_source(self):
        print self.get_shader_properties()
        # source_objs = self.get_all_source_objs()
        # for source_obj in source_objs:
        #     print source_obj.get_shader_properties()

    def get_shader_properties(self):
        properties = ctt_core.Properties(self)
        properties.set(
            'type', self.get_shader_type_name(),
        )
        properties.set(
            'path', self.path,
        )
        attributes = self.get_shader_attributes()
        properties.set(
            'attributes', attributes.value
        )
        return properties

    def get_shader_ports(self):
        return self.get_port('parameters').get_children()

    def get_shader_attributes(self):
        attributes = ctt_core.Properties(self)
        ports = self.get_shader_ports()
        for port in ports:
            port_name = port.port_name
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


class AndStandardSurface(AndShader):
    def __init__(self, path):
        super(AndStandardSurface, self).__init__(path)

    @ktn_core.Modifier.undo_debug_run
    def set_port_user_data_create(self, data_type_name, port_name, attribute_name, default_value):
        name = self.name
        parent_path = self.get_parent_path()
        #
        multiply_obj_type_name = 'multiply'
        multiply_path = '{}/{}__{}__{}'.format(parent_path, name, port_name, multiply_obj_type_name)
        multiply = AndShader(
            multiply_path
        )
        input_port = self.get_input_port(port_name)
        if multiply.get_is_exists() is False:
            multiply.set_shader_create(multiply_obj_type_name)
            #
            source = input_port.get_source()
            if source is not None:
                multiply.get_input_port('input1').set_source(source)
            else:
                multiply.set_shader_port_value('input1', self.get_shader_port_value(port_name))
            #
            multiply.get_output_port('out').set_target(
                input_port
            )
            #
            user_data_obj_type_name = 'user_data_{}'.format(data_type_name)
            user_data_path = '{}/{}__{}__{}'.format(parent_path, name, port_name, user_data_obj_type_name)
            user_data = AndShader(
                user_data_path
            )
            user_data.set_shader_create(user_data_obj_type_name)
            user_data.set_shader_port_value('attribute', attribute_name)
            user_data.set_shader_port_value('default', default_value)
            user_data.get_output_port('out').set_target(
                multiply.get_input_port('input2')
            )

        self.set_source_objs_layout()


class AndRamp(AndShader):
    DCC_PORT_CLS = ktn_dcc_obj_node.Port
    DCC_CONNECTION_CLS = ktn_dcc_obj_node.Connection

    def __init__(self, path):
        super(AndRamp, self).__init__(path)
        self._ramp_dict = {}

    def _set_ramp_value_(self, key, value):
        bsc_log.Log.trace_method_result(
            'arnold-ramp-set',
            'attribute="{}"'.format(key)
        )
        cur_size = len(value)
        self.set_ramp_size(cur_size)
        #
        self.get_port('parameters.{}.enable'.format(key)).set(False)
        self.get_port('parameters.{}.value'.format(key)).set(value)
        #
        bsc_log.Log.trace_method_result(
            'arnold-ramp-set',
            'value="{}"'.format(self.get_port('parameters.{}.value'.format(key)).get())
        )

    def get_ramp_size(self):
        return self.get_port('parameters.ramp.value').get()

    def set_ramp_size(self, value):
        self.get_port('parameters.ramp.enable').set(True)
        self.get_port('parameters.ramp.value').set(value)

    def get_ramp_positions(self):
        return self.get_port('parameters.ramp_Knots.value').get()

    def set_ramp_positions(self, value):
        self.get_port('parameters.ramp_Knots.enable').set(True)
        self.get_port('parameters.ramp_Knots.value').set(value)
        # print self.get_port('parameters.ramp_Knots').ktn_port.getXML()

    def get_ramp_interpolation(self):
        return self.get_port('parameters.ramp_Interpolation.value').get()

    def set_ramp_interpolation(self, value):
        self.get_port('parameters.ramp_Interpolation.enable').set(True)
        self.get_port('parameters.ramp_Interpolation.value').set(value)

    def get_ramp_colors(self):
        return self.get_port('parameters.ramp_Colors.value').get()

    def set_ramp_colors(self, value):
        self.get_port('parameters.ramp_Colors.enable').set(True)
        self.get_port('parameters.ramp_Colors.value').set(value)

    def get_ramp_floats(self):
        return self.get_port('parameters.ramp_Floats.value').get()

    def set_ramp_floats(self, value):
        self.get_port('parameters.ramp_Floats.enable').set(True)
        self.get_port('parameters.ramp_Floats.value').set(value)
        # print self.get_port('parameters.ramp_Floats').ktn_port.getXML()

    def get_ramp_value(self):
        return self.get_port('parameters.ramp_Floats.value').get()

    def set_ramp_value(self, value):
        return self.get_port('parameters.ramp_Floats.value').set(value)

    def get_ramp(self):
        if self.get_port('nodeType').get() == 'ramp_float':
            return (
                self.get_ramp_positions(),
                self.get_ramp_interpolation(),
                self.get_ramp_floats()
            )
        elif self.get_port('nodeType').get() == 'ramp_rgb':
            return (
                self.get_ramp_positions(),
                self.get_ramp_interpolation(),
                self.get_ramp_colors()
            )

    def _set_ramp_value_update_(self, key, value):
        self._ramp_dict[key] = value

    def _get_ramp_mark_(self):
        return self._ramp_dict

    def _set_ramp_dict_(self, value_dict, interpolation_dict):
        positions = value_dict.keys()
        positions.sort()
        #
        size = len(positions)+2
        #
        self.set_ramp_size(size)
        self.set_ramp_positions([positions[0]]+positions+[positions[-1]])
        #
        interpolations = [interpolation_dict[i] for i in positions]
        interpolation = interpolations[0]
        #
        interpolation = max(min(interpolation, 3), 0)
        strings = ['constant', 'linear', 'catmull-rom', 'bspline']
        self.get_port('parameters.ramp_Interpolation.value').set(strings[interpolation])
        #
        values = [value_dict[i] for i in positions]
        type_ = self.get_port('nodeType').get()
        if type_ == 'ramp_rgb':
            values_ = [values[0]]+values+[values[-1]]
            colors = [j for i in values_ for j in i]
            self.set_ramp_colors(colors)
        elif type_ == 'ramp_float':
            values_ = [values[0]]+values+[values[-1]]
            floats = values_
            self.set_ramp_floats(floats)

    def _set_ramp_dict_save_(self, value_dict, interpolation_dict):
        tags = [
            ('lx_ramp_values', value_dict),
            ('lx_ramp_interpolations', interpolation_dict),
        ]
        #
        for k, v in tags:
            port_path = k
            port = self.get_port(port_path)
            if port.get_is_exists() is True:
                port.set(str(v))
            else:
                port.set_create('string', str(v))

    def _set_ramp_dict_write0_(self):
        type_ = self.get_port('nodeType').get()
        interpolations = self._ramp_dict['ramp_Interpolation']
        if type_ == 'ramp_rgb':
            values = self._ramp_dict['ramp_Colors']
        elif type_ == 'ramp_float':
            values = self._ramp_dict['ramp_Floats']
        else:
            raise
        #
        value_dict = {}
        interpolation_dict = {}
        position_array = self._ramp_dict['ramp_Knots']
        for seq, position in enumerate(position_array):
            value_dict[position] = values[seq]
            interpolation_dict[position] = interpolations[seq]
        #
        self._set_ramp_dict_(value_dict, interpolation_dict)
        self._set_ramp_dict_save_(value_dict, interpolation_dict)

    def _set_ramp_dict_write1_(self):
        type_ = self.get_port('nodeType').get()
        if type_ == 'ramp_rgb':
            keys = ['ramp_Knots', 'ramp_Interpolation', 'ramp_Colors']
        elif type_ == 'ramp_float':
            keys = ['ramp_Knots', 'ramp_Interpolation', 'ramp_Floats']
        else:
            raise
        for dcc_port_key in keys:
            count = self.get_ramp_size()
            if dcc_port_key in ['ramp_Interpolation']:
                strings = ['constant', 'linear', 'catmull-rom', 'bspline']
                values = [strings.index(self.get_shader_port_value(dcc_port_key))]*int(count)
            elif dcc_port_key in ['ramp_Colors']:
                _ = self.get_shader_port_value(dcc_port_key)
                values = bsc_core.RawListMtd.grid_to(_, 3)
            else:
                values = self.get_shader_port_value(dcc_port_key)

            self._set_ramp_value_update_(dcc_port_key, values)

        type_ = self.get_port('nodeType').get()
        interpolations = self._ramp_dict['ramp_Interpolation']
        if type_ == 'ramp_rgb':
            values = self._ramp_dict['ramp_Colors']
        elif type_ == 'ramp_float':
            values = self._ramp_dict['ramp_Floats']
        else:
            raise
        #
        value_dict = {}
        interpolation_dict = {}
        position_array = self._ramp_dict['ramp_Knots']
        for seq, position in enumerate(position_array):
            value_dict[position] = values[seq]
            interpolation_dict[position] = interpolations[seq]
        #
        self._set_ramp_dict_save_(value_dict, interpolation_dict)

    def _set_ramp_dict_read_(self):
        values_port = self.get_port('lx_ramp_values')
        interpolations_port = self.get_port('lx_ramp_interpolations')
        if values_port and interpolations_port:
            value_dict = eval(values_port.get() or '{}')
            interpolation_dict = eval(interpolations_port.get() or '{}')
            if value_dict and interpolation_dict:
                self._set_ramp_dict_(value_dict, interpolation_dict)


# noinspection PyUnusedLocal
class Material(ktn_abstracts.AbsKtnObj):
    DCC_PORT_CLS = ktn_dcc_obj_node.Port
    DCC_CONNECTION_CLS = ktn_dcc_obj_node.Connection

    DCC_SOURCE_NODE_CLS = AndShader

    def __init__(self, path):
        super(Material, self).__init__(path)

    def get_scene_graph_path(self):
        location = self.get_parent().get_port('rootLocation').get()
        # name = self.name
        # return '{}/{}'.format(location.rstrip('/'), name)
