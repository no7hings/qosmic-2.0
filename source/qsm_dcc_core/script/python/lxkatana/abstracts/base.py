# coding:utf-8
import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxuniverse.core as unr_core
# katana
from ..core.wrap import *

from .. import core as ktn_core


class AbsKtnPort(bsc_dcc_abstracts.AbsDccPort):
    PATHSEP = '.'

    def __init__(self, node, name, port_assign):
        super(AbsKtnPort, self).__init__(node, name, port_assign)

    def _generate_ktn_port(self):
        if self.port_assign == unr_core.UnrPortAssign.VARIANTS:
            return NodegraphAPI.GetNode(self.obj.name).getParameter(self.port_path)
        elif self.port_assign == unr_core.UnrPortAssign.INPUTS:
            return NodegraphAPI.GetNode(self.obj.name).getInputPort(self.port_path)
        elif self.port_assign == unr_core.UnrPortAssign.OUTPUTS:
            return NodegraphAPI.GetNode(self.obj.name).getOutputPort(self.port_path)
        raise TypeError()

    def get_ktn_obj(self):
        return self.obj.ktn_obj

    ktn_obj = property(get_ktn_obj)

    @property
    def ktn_port(self):
        return self._generate_ktn_port()

    def get_type(self):
        ktn_port = self._generate_ktn_port()
        if ktn_port is not None:
            return ktn_port.getType()
        return ''

    type = property(get_type)

    def get_is_exists(self):
        ktn_port = self._generate_ktn_port()
        return ktn_port is not None

    def set_create(self, *args):
        ktn_port = self._generate_ktn_port()
        parent = bsc_core.PthPortMtd.get_dag_parent_path(
            path=self._port_path, pathsep=self.PATHSEP
        )
        if ktn_port is None:
            bsc_log.Log.trace_method_result(
                'port create',
                'attribute="{}"'.format(self.path)
            )
            if self.port_assign == unr_core.UnrPortAssign.VARIANTS:
                if parent is not None:
                    parent_ktn_port = self.ktn_obj.getParameter(parent)
                else:
                    parent_ktn_port = self.ktn_obj.getParameters()
                #
                if parent_ktn_port is not None:
                    type_, value = args[:2]
                    if type_ == 'string':
                        parent_ktn_port.createChildString(self.port_name, str(value))
            elif self.port_assign == unr_core.UnrPortAssign.INPUTS:
                return self.ktn_obj.addInputPort(self.port_name)
            elif self.port_assign == unr_core.UnrPortAssign.OUTPUTS:
                return self.ktn_obj.addOutputPort(self.port_name)

    def set_attributes(self, attributes):
        ktn_port = self._generate_ktn_port()
        if ktn_port is not None:
            attributes_ = ktn_port.getAttributes()
            attributes_.update(attributes)
            ktn_port.setAttributes(attributes_)

    def get_dcc_instance(self):
        ktn_port = self._generate_ktn_port()
        if ktn_port is None:
            ktn_port = self.set_create()
            return ktn_port, True
        return ktn_port, False

    def get_is_enumerate(self):
        pass

    def get(self, time=0):
        ktn_port = self._generate_ktn_port()
        if ktn_port is not None:
            children = ktn_port.getChildren() or []
            if children:
                return [i.getValue(time) for i in children]
            else:
                return ktn_port.getValue(time)

    def set(self, value, time=0):
        ktn_port = self._generate_ktn_port()
        if ktn_port is not None:
            ktn_core.NGPortOpt(ktn_port).set(value, time)

    def get_is_expression(self):
        return self.ktn_port.isExpression()

    def set_expression(self, expression):
        self.ktn_port.setExpression(expression)

    def get_expression(self):
        return self.ktn_port.getExpression()

    @classmethod
    def _set_constant_value_(cls, ktn_port, value, time=0):
        _value = value
        if isinstance(value, unicode):
            _value = str(value)
        #
        ktn_port.setValue(_value, time)

    @classmethod
    def _set_array_value_(cls, ktn_port, value, time=0):
        size = len(value)
        ktn_port.resizeArray(size)
        [ktn_port.getChildByIndex(i).setValue(value[i], time) for i in range(size)]

    @classmethod
    def _set_connect_(cls, source, target, validation=False):
        if validation is True:
            ktn_source = source.ktn_port
            ktn_target = target.ktn_port
            if ktn_source is not None and ktn_target is not None:
                ktn_source.connect(ktn_target)
                bsc_log.Log.trace_method_result(
                    'port connect',
                    'connection="{} >> {}"'.format(
                        source.path, target.path
                    )
                )
        else:
            source.ktn_port.connect(target.ktn_port)
            bsc_log.Log.trace_method_result(
                'port connect',
                'connection="{} >> {}"'.format(
                    source.path, target.path
                )
            )

    @classmethod
    def _set_disconnect_(cls, source, target):
        if source.ktn_port is not None and target.ktn_port is not None:
            source.ktn_port.disconnect(target.ktn_port)
            bsc_log.Log.trace_method_result(
                'port-disconnect',
                'connection="{} >> {}"'.format(
                    source.path, target.path
                )
            )

    def execute(self):
        NodegraphAPI.UserParameters.ExecuteButton(
            self.get_ktn_obj(), self.port_path
        )

    def get_source(self):
        ktn_output_ports = self.ktn_port.getConnectedPorts()
        if ktn_output_ports:
            ktn_source = ktn_output_ports[0]
            ktn_obj = ktn_source.getNode()
            #
            obj = self.obj.__class__(ktn_obj.getName())
            port_name = ktn_source.getName()
            # debug
            if ktn_source.getNode().getOutputPort(port_name) is None:
                return obj.get_input_port(
                    port_name
                ).get_source()
            return obj.get_output_port(
                port_name
            )

    def set_source(self, output_port, validation=False):
        self._set_connect_(output_port, self, validation)

    def set_disconnect(self):
        if self.port_assign == unr_core.UnrPortAssign.INPUTS:
            source = self.get_source()
            if source is not None:
                self._set_disconnect_(source, self)
        elif self.port_assign == unr_core.UnrPortAssign.OUTPUTS:
            targets = self.get_targets()
            for i_target in targets:
                self._set_disconnect_(self, i_target)

    def get_targets(self):
        lis = []
        input_ktn_ports = self.ktn_port.getConnectedPorts()
        if input_ktn_ports:
            for i_input_ktn_port in input_ktn_ports:
                i_ktn_obj = i_input_ktn_port.getNode()
                i_obj = self.obj.__class__(i_ktn_obj.getName())
                lis.append(
                    i_obj.get_input_port(i_input_ktn_port.getName())
                )
        return lis

    def set_target(self, input_port, force=False, validation=False):
        if force is True:
            input_port.set_create()
        #
        self._set_connect_(self, input_port, validation=validation)

    def _set_port_dag_create_(self, port_path):
        port_assign = self.port_assign
        return self.__class__(self.obj, port_path, port_assign)

    def get_children(self):
        list_ = []
        _ = self.ktn_port.getChildren() or []
        for i in _:
            list_.append(
                self.get_child(i.getName())
            )
        return list_

    def get_child(self, port_name):
        _ = [i.getName() for i in self.ktn_port.getChildren()]
        if port_name in _:
            port_path = self.PATHSEP.join([self.port_path, port_name])
            return self._set_port_dag_create_(port_path)

    def do_update(self):
        self._generate_ktn_port()


# noinspection PyUnusedLocal
class AbsKtnObj(bsc_dcc_abstracts.AbsDccNode):
    PATHSEP = '/'
    DCC_CONNECTION_CLS = None

    def __init__(self, path):
        if not path.startswith(self.PATHSEP):
            path = self._get_ktn_obj_path_(path)
        else:
            path = path
        super(AbsKtnObj, self).__init__(path)

    def get_type(self):
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is not None:
            return ktn_obj.getType()
        return ''

    type = property(get_type)

    def get_icon(self):
        return bsc_resource.RscExtendIcon.get('application/katana')

    icon = property(get_icon)

    @property
    def ktn_obj(self):
        return self._generate_ktn_obj()

    def _generate_ktn_obj(self):
        return NodegraphAPI.GetNode(self.name)

    def set_create(self, obj_type_name):
        ktn_obj = self._generate_ktn_obj()
        if ktn_obj is None:
            parent = self.get_parent()
            parent_ktn_obj = parent.ktn_obj
            if parent_ktn_obj is not None:
                ktn_obj = NodegraphAPI.CreateNode(obj_type_name, parent_ktn_obj)
                if ktn_obj is None:
                    raise TypeError('unknown-obj-type: "{}"'.format(obj_type_name))
                name_ktn_port = ktn_obj.getParameter('name')
                if name_ktn_port is not None:
                    name_ktn_port.setValue(self.name, 0)
                #
                ktn_obj.setName(self.name)
                bsc_log.Log.trace_method_result(
                    'obj create',
                    'obj="{}", type="{}"'.format(self.path, obj_type_name)
                )
                return ktn_obj

    def set_shader_type(self, type_name):
        ktn_obj = self._generate_ktn_obj()
        if ktn_obj is not None:
            type_ktn_port = ktn_obj.getParameter('nodeType')
            if type_ktn_port is not None:
                type_ktn_port.setValue(type_name, 0)

    def get_dcc_instance(self, obj_type_name, base_obj_type_name=None, *args, **kwargs):
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is None:
            ktn_obj = self.set_create(obj_type_name)
            return ktn_obj, True
        else:
            exists_obj_type_name = ktn_obj.getType()
            if base_obj_type_name is not None:
                check_exists_obj_type_name = base_obj_type_name
            else:
                check_exists_obj_type_name = obj_type_name
            #
            if exists_obj_type_name != check_exists_obj_type_name:
                self.do_delete()
                ktn_obj = self.set_create(obj_type_name)
                return ktn_obj, True
        return ktn_obj, False

    def get_is_exists(self):
        return NodegraphAPI.GetNode(self.name) is not None

    @classmethod
    def _get_ktn_obj_path_args_(cls, name):
        def _rcs_fnc(name_):
            _ktn_obj = NodegraphAPI.GetNode(name_)
            if _ktn_obj is not None:
                _parent = _ktn_obj.getParent()
                if _parent is None:
                    list_.append('')
                else:
                    _parent_name = _parent.getName()
                    list_.append(_parent_name)
                    _rcs_fnc(_parent_name)

        #
        list_ = [name]
        _rcs_fnc(name)
        list_.reverse()
        return list_

    @classmethod
    def _get_ktn_obj_path_(cls, name):
        return cls.PATHSEP.join(cls._get_ktn_obj_path_args_(name))

    def create_dag_fnc(self, path):
        return self.__class__(path)

    def get_descendant_paths(self):
        def _rcs_fnc(lis_, path_):
            lis_.append(path_)
            _name = path_.split(pathsep)[-1]
            _ktn_obj = NodegraphAPI.GetNode(_name)
            if hasattr(_ktn_obj, 'getChildren'):
                _ = _ktn_obj.getChildren() or []
                if _:
                    for _i in _:
                        _i_path = '{}{}{}'.format(self.path, pathsep, _i.getName())
                        _rcs_fnc(lis_, _i_path)

        lis = []
        pathsep = self.pathsep
        _rcs_fnc(lis, self.name)
        return lis

    def get_child_paths(self):
        lis = []
        ktn_obj = self._generate_ktn_obj()
        if ktn_obj is not None:
            if hasattr(ktn_obj, 'getChildren'):
                _ = ktn_obj.getChildren() or []
                for i in _:
                    lis.append('{}{}{}'.format(self.path, self.pathsep, i.getName()))
        return lis

    def _get_child_(self, path):
        return self.__class__(path)

    def do_delete(self):
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is not None:
            ktn_obj.delete()
            bsc_log.Log.trace_method_result(
                'obj-delete',
                '"{}"'.format(self.path)
            )

    def set_rename(self, new_name):
        if isinstance(new_name, unicode):
            new_name = str(new_name)
        #
        ktn_obj = NodegraphAPI.GetNode(self.name)
        if ktn_obj is not None:
            name_ktn_port = ktn_obj.getParameter('name')
            if name_ktn_port is not None:
                name_ktn_port.setValue(new_name, 0)
            ktn_obj.setName(new_name)
            return self.__class__(new_name)

    def clear_children(self):
        [i.do_delete() for i in self.get_children()]

    def get_source_ktn_connections(self):
        lis = []
        ktn_obj = self._generate_ktn_obj()
        _ = ktn_obj.getInputPorts() or []
        for target_ktn_port in _:
            source_ktn_ports = target_ktn_port.getConnectedPorts()
            if source_ktn_ports:
                for source_ktn_port in source_ktn_ports:
                    lis.append((target_ktn_port, source_ktn_port))
        return lis

    def _get_source_connection_raw_(self, **kwargs):
        inner = kwargs.get('inner') or False
        # print inner
        lis = []
        ktn_obj = self._generate_ktn_obj()
        _ = ktn_obj.getInputPorts() or []
        for target_ktn_port in _:
            source_ktn_ports = target_ktn_port.getConnectedPorts()
            if source_ktn_ports:
                for i_source_ktn_port in source_ktn_ports:
                    i_source_ktn_obj = i_source_ktn_port.getNode()
                    i_source_obj_name = i_source_ktn_obj.getName()
                    i_source_port_name = i_source_ktn_port.getName()
                    i_source_atr_path = bsc_core.PthAttributeMtd.join_by(
                        i_source_obj_name, i_source_port_name
                    )
                    target_obj_name = target_ktn_port.getNode().getName()
                    target_port_name = target_ktn_port.getName()
                    target_atr_path = bsc_core.PthAttributeMtd.join_by(
                        target_obj_name, target_port_name
                    )
                    lis.append(
                        (i_source_atr_path, target_atr_path)
                    )
        return lis

    # def get_all_source_objs(self, *args, **kwargs):
    #     # TODO, fix this code
    #     return [self.__class__(i.getName()) for i in ktn_core.NGNodeOpt(self._generate_ktn_obj()).get_all_source_objs()]

    def get_target_connections(self):
        lis = []
        ktn_obj = self._generate_ktn_obj()
        _ = ktn_obj.getOutputPorts() or []
        for source_ktn_port in _:
            target_ktn_ports = source_ktn_port.getConnectedPorts()
            if target_ktn_ports:
                for target_ktn_port in target_ktn_ports:
                    source_ktn_obj = source_ktn_port.getNode()
                    target_ktn_obj = target_ktn_port.getNode()
                    source_port = self.__class__(source_ktn_obj.getName()).get_output_port(source_ktn_port.getName())
                    target_port = self.__class__(target_ktn_obj.getName()).get_input_port(target_ktn_port.getName())
                    lis.append(self.DCC_CONNECTION_CLS(source_port, target_port))
        return lis

    #
    def get_sources(self):
        pass

    @ktn_core.Modifier.undo_debug_run
    def set_source_objs_layout(self, layout=('r-l', 't-b'), size=(320, 960)):
        def rcs_fnc_(obj_, column_):
            _source_objs = obj_.get_source_objs()
            if _source_objs:
                _ktn_obj = obj_.ktn_obj
                column_ += 1
                if column_ not in ktn_obj_in_column_dict:
                    _i_ktn_objs = []
                    ktn_obj_in_column_dict[column_] = _i_ktn_objs
                else:
                    _i_ktn_objs = ktn_obj_in_column_dict[column_]
                #
                for _row, _i in enumerate(_source_objs):
                    _i_ktn_obj = _i.ktn_obj
                    if _i_ktn_obj not in ktn_obj_stack:
                        ktn_obj_stack.append(_i_ktn_obj)
                        _i_ktn_objs.append(_i_ktn_obj)
                        rcs_fnc_(_i, column_)

        #
        ktn_obj = self.ktn_obj
        ktn_obj_stack = []
        ktn_obj_in_column_dict = {}
        #
        ktn_parent = ktn_obj.getParent()
        #
        layout_x, layout_y = layout
        x, y = NodegraphAPI.GetNodePosition(ktn_obj)
        w, h = size
        rcs_fnc_(self, 0)
        if ktn_obj_in_column_dict:
            for column, v in ktn_obj_in_column_dict.items():
                c = len(v)
                if layout_x == 'r-l':
                    s_x = x-column*w*2
                elif layout_x == 'l-r':
                    s_x = x+column*w*2
                else:
                    raise ValueError()
                #
                if layout_y == 't-b':
                    s_y = y+c*h/2
                elif layout_y == 'b-t':
                    s_y = y-c*h/2
                else:
                    raise ValueError()
                if v:
                    for j_seq, j_ktn_obj in enumerate(v):
                        i_x = s_x
                        if layout_y == 't-b':
                            i_y = s_y-j_seq*h
                        elif layout_y == 'b-t':
                            i_y = s_y+j_seq*h
                        else:
                            raise ValueError()
                        #
                        j_atr = dict(
                            x=i_x,
                            y=i_y,
                        )
                        j_atr_ = j_ktn_obj.getAttributes()
                        j_atr_.update(j_atr)
                        j_ktn_parent = j_ktn_obj.getParent()
                        if j_ktn_parent.getName() == ktn_parent.getName():
                            j_ktn_obj.setAttributes(j_atr_)
            #
            bsc_log.Log.trace_method_result(
                'network-layout',
                'obj="{}"'.format(self.path)
            )

    def set_source_objs_colour(self):
        source_objs = self.get_all_source_objs()
        for obj in source_objs:
            obj.set_colour_by_type_name()

    def get_position(self):
        ktn_obj = self._generate_ktn_obj()
        return NodegraphAPI.GetNodePosition(ktn_obj)

    def set_sources_disconnect(self):
        ktn_connections = self.get_source_ktn_connections()
        for s_ktn_obj, t_ktn_obj in ktn_connections:
            s_ktn_obj.disconnect(t_ktn_obj)

    def get_as_dict(self, keys):
        dic = {}
        for i_key in keys:
            port = self.get_port(i_key)
            if port.get_is_exists() is True:
                dic[i_key] = port.get()
            else:
                bsc_log.Log.trace_method_warning(
                    'property-get',
                    'port: "{}" is Non-exists'.format(port.path)
                )
        return dic

    def set_as_dict(self, dict_):
        for k, v in dict_.items():
            i_p = self.get_port(k)
            if i_p.get_is_exists() is True:
                i_p.set(v)
                bsc_log.Log.trace_method_result(
                    'property-set',
                    'port: "{}" >> "{}"'.format(i_p.path, v)
                )
            else:
                bsc_log.Log.trace_method_warning(
                    'property-set',
                    'port: "{}" is Non-exists'.format(i_p.path)
                )

    def get_input_ports(self):
        _ = self.ktn_obj.getInputPorts() or []
        return [self.get_input_port(i.getName()) for i in _]

    def set_colour_by_type_name(self):
        type_name = self.type_name
        r, g, b = bsc_core.RawTextOpt(type_name).to_rgb(maximum=1)
        attributes = self.ktn_obj.getAttributes()
        attributes['ns_colorr'] = r
        attributes['ns_colorg'] = g
        attributes['ns_colorb'] = b
        self.ktn_obj.setAttributes(attributes)

    def get_leaf_ports(self):
        def rcs_fnc_(ktn_port_, parent_port_path):
            _port_name = ktn_port_.getName()
            if parent_port_path is not None:
                _port_path = port_pathsep.join([parent_port_path, _port_name])
            else:
                _port_path = _port_name
            _children = ktn_port_.getChildren()
            if _children:
                for _child in _children:
                    rcs_fnc_(_child, _port_path)
            else:
                _type = ktn_port_.getType()
                if _type != 'group':
                    lis.append(
                        self.get_port(_port_path)
                    )

        #
        lis = []
        port_pathsep = self.DCC_PORT_CLS.PATHSEP
        root_ktn_port = self.ktn_obj.getParameters()
        for i in root_ktn_port.getChildren():
            rcs_fnc_(i, None)

        return lis

    def get_attributes(self):
        attributes = ctt_core.Properties(self)
        ports = self.get_leaf_ports()
        for port in ports:
            attributes.set(
                port.port_path, port.get()
            )
        return attributes

    def set_attributes(self):
        pass

    def __get_ktn_port_(self, port_path):
        return NodegraphAPI.GetNode(self.path).getParameter(port_path)

    @ktn_core.Modifier.undo_debug_run
    def create_customize_attributes(self, attributes):
        ktn_core.NGNodeCustomizePortOpt(self._generate_ktn_obj()).set_ports_add(attributes)

    def set_input_port_add(self, port_path):
        ktn_obj = self._generate_ktn_obj()
        _ = ktn_obj.getInputPort(port_path)
        if _ is None:
            self.ktn_obj.addInputPort(port_path)

    def set_output_port_add(self, port_path):
        ktn_obj = self._generate_ktn_obj()
        _ = ktn_obj.getOutputPort(port_path)
        if _ is None:
            self.ktn_obj.addOutputPort(port_path)

    def set_expression(self, key, value):
        self.get_port(key).set_expression(value)

    def get_is_bypassed(self):
        return self._generate_ktn_obj().isBypassed()


class AbsKtnObjs(bsc_dcc_abstracts.AbsDccNodes):
    def __init__(self, *args):
        super(AbsKtnObjs, self).__init__(*args)

    @classmethod
    def pre_run_fnc(cls):
        pass

    @classmethod
    def get_paths(cls, **kwargs):
        cls.pre_run_fnc()
        #
        lis = []
        for i in cls.DCC_TYPES_INCLUDE:
            _ = NodegraphAPI.GetAllNodesByType(i) or []
            for ktn_node in _:
                obj_path = cls.DCC_NODE_CLS._get_ktn_obj_path_(ktn_node.getName())
                lis.append(obj_path)
        return lis


class AbsKtnObjConnection(bsc_dcc_abstracts.AbsDccNodeConnection):
    def __init__(self, source, target):
        super(AbsKtnObjConnection, self).__init__(source, target)


class AbsKtnFileReferenceObj(
    AbsKtnObj,
    bsc_dcc_abstracts.AbsDccNodeFileReferenceDef
):
    def __init__(self, path, file_path=None):
        super(AbsKtnFileReferenceObj, self).__init__(path)
        # init file reference
        self._init_dcc_node_file_reference_def_(file_path)


class AbsSGKtnObj(bsc_dcc_abstracts.AbsDccNode):
    def __init__(self, path):
        super(AbsSGKtnObj, self).__init__(path)

    @property
    def type(self):
        return ''

    @property
    def icon(self):
        return ''

    def get_is_exists(self):
        pass
