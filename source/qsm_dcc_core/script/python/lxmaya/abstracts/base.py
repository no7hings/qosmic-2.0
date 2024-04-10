# coding:utf-8
import six

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

from ..core.wrap import *

from .. import core as mya_core


# noinspection PyUnusedLocal
class ObjPortsOpt(object):
    def __init__(self, obj_path):
        self._obj_path = obj_path

    def get_port_names(self):
        return cmds.listAttr(
            self._obj_path, read=1, write=1, inUse=1, multi=1
        ) or []

    @classmethod
    def _get_ports_raw_(cls, obj_path, port_names):
        lis = []
        #
        if port_names:
            for port_name in port_names:
                print port_name
        return lis


class AbsMyaPort(bsc_dcc_abstracts.AbsDccPort):
    PATHSEP = mya_core.MyaUtil.PORT_PATHSEP
    KEY = 'port'

    def __init__(self, obj, path, port_assign=None):
        super(AbsMyaPort, self).__init__(obj, path, port_assign=port_assign)
        self._obj_atr_query = mya_core.CmdAtrQueryOpt(self.path)

    def get_type(self):
        if self.get_is_exists() is True:
            return cmds.getAttr(self.path, type=True)
        elif self.get_query_is_exists() is True:
            return self._obj_atr_query.type

    type = property(get_type)

    def get_data_type(self):
        if self._obj_atr_query.get_is_exists() is True:
            return self._obj_atr_query.type
        return ''

    data_type = property(get_data_type)

    def get_port_query(self):
        return self._obj_atr_query

    port_query = property(get_port_query)

    def get_is_exists(self):
        return cmds.objExists(self.path)

    def get_query_is_exists(self):
        return self._obj_atr_query.get_is_exists()

    def set_create(self, raw_type, default_raw=None):
        if self.get_is_exists() is False:
            if raw_type == 'string':
                cmds.addAttr(
                    self.obj.path,
                    longName=self.name,
                    dataType=raw_type
                )
            else:
                cmds.addAttr(
                    self.obj.path,
                    longName=self.name,
                    attributeType=raw_type
                )
            if default_raw is not None:
                self.set(default_raw)

    def get(self, as_string=False):
        if self.type == 'message':
            return None
        if self.get_is_exists() is True:
            if as_string is True:
                return cmds.getAttr(self.path, asString=True) or ''
            #
            _ = cmds.getAttr(self.path)
            if self.get_channel_names():
                return _[0]
            return _

    def get_enumerate_strings(self):
        if self.get_is_exists() is True:
            return mya_core.CmdPortOpt(self.obj.path, self.port_path).get_enumerate_strings()
        return []

    def get_is_value_changed(self):
        return self.get_default() != self.get()

    def get_default(self):
        _ = self._obj_atr_query.get_default()
        if self.type == 'bool':
            return bool(int(_))
        return _

    def set(self, value):
        if self.get_is_exists() is True:
            if self.has_source() is False:
                if self.type == 'string':
                    if isinstance(value, six.string_types):
                        cmds.setAttr(self.path, value, type=self.type)
                    else:
                        bsc_log.Log.trace_method_warning(
                            'port set',
                            'attribute="{}", value="{}" is not available'.format(self.path, value)
                        )
                elif self.type == 'enum':
                    if isinstance(value, six.string_types):
                        enumerate_strings = self._obj_atr_query.get_enumerate_strings()
                        index = enumerate_strings.index(value)
                        cmds.setAttr(self.path, index)
                    else:
                        cmds.setAttr(self.path, value)
                else:
                    if isinstance(value, (tuple, list)):
                        if self.type == 'matrix':
                            # ((1, 1, 1), ...)
                            if isinstance(value[0], (tuple, list)):
                                value = [j for i in value for j in i]
                            #
                            cmds.setAttr(self.path, value, type='matrix')
                        else:
                            cmds.setAttr(self.path, *value, clamp=1)
                    else:
                        # Debug ( Clamp Maximum or Minimum Value )
                        cmds.setAttr(self.path, value, clamp=1)
                #
            else:
                bsc_log.Log.trace_method_warning(
                    'port set',
                    'attribute="{}" has source'.format(self.path)
                )

    def _set_as_array_(self, values):
        parent_path = self.get_parent_path()
        for seq, value in enumerate(values):
            parent_path_ = '{}[{}]'.format(parent_path, seq)
            atr_path = self.PATHSEP.join(
                [self.obj.path, parent_path_, self.port_name]
            )
            if self.type == 'string':
                cmds.setAttr(atr_path, value, type=self.type)
            else:
                if isinstance(value, (tuple, list)):
                    cmds.setAttr(atr_path, *value)
                else:
                    # Debug ( Clamp Maximum or Minimum Value )
                    cmds.setAttr(atr_path, value, clamp=1)

    def set_source(self, output_port, validation=False):
        self._set_connect_(output_port, self, validation=validation)

    def set_source_disconnect(self):
        source = self.get_source()
        if source:
            cmds.disconnectAttr(
                source.path, self.path
            )

    def get_source(self):
        _ = cmds.connectionInfo(
            self.path,
            sourceFromDestination=1
        )
        if _:
            a = bsc_core.PthAttributeOpt(_)
            obj_path = a.obj_path
            port_path = a.port_path
            return self.obj.__class__(obj_path).get_port(port_path)

    def has_source(self):
        _ = cmds.connectionInfo(self.path, isExactDestination=1)
        if self.get_has_channels():
            if _ is True:
                return _
            return True in [i.has_source() for i in self.get_channels()]
        return _

    def set_target(self, input_port, validation=False):
        self._set_connect_(self, input_port, validation=validation)

    def get_has_targets(self):
        return cmds.connectionInfo(self.path, isExactSource=1)

    #
    def get_targets(self):
        lis = []
        _ = cmds.connectionInfo(
            self.path,
            destinationFromSource=1
        ) or []
        for i in _:
            a = bsc_core.PthAttributeOpt(i)
            i_obj_path = a.obj_path
            i_port_path = a.port_path
            lis.append(
                self.obj.__class__(i_obj_path).get_port(i_port_path)
            )
        return lis

    # array
    def get_element_indices(self):
        return mya_core.CmdAtrQueryOpt(self.path).get_element_indices()

    # channel
    def get_channel_names(self, alpha=False):
        return mya_core.CmdAtrQueryOpt(self.path).get_channel_names(alpha=alpha)

    def get_has_channels(self, alpha=False):
        return self.get_channel_names(alpha=alpha) != []

    def get_channel_count(self, alpha=False):
        return len(self.get_channel_names(alpha=alpha))

    def get_alpha_channel_name(self):
        return mya_core.CmdAtrQueryOpt(self.path).get_alpha_channel_name()

    def get_alpha_channel(self):
        channel_name = self.get_alpha_channel_name()
        if channel_name is not None:
            return self.obj.get_port(channel_name)

    def get_has_alpha_channel(self):
        return self.get_alpha_channel_name() is not None

    def get_channels(self, alpha=False):
        lis = []
        if self.get_has_channels(alpha=alpha):
            channel_names = self.get_channel_names(alpha=alpha)
            for channel_name in channel_names:
                channel = self.obj.get_port(
                    '{}.{}'.format(self.port_path, channel_name)
                )
                lis.append(channel)
        return lis

    def get_channel_at(self, index, alpha=False):
        channels = self.get_channels(alpha=alpha)
        if index < len(channels):
            return channels[index]

    def get_is_channel(self):
        return self._obj_atr_query.get_is_channel()

    def get_parent_path(self):
        return self._obj_atr_query.get_parent_path()

    def get_parent(self):
        _ = self.get_parent_path()
        if _ is not None:
            return self.__class__(
                self.obj, _
            )

    @classmethod
    def _set_connect_(cls, source, target, validation=False):
        source_path, target_path = source.path, target.path
        if cmds.isConnected(source_path, target_path) is False:
            if validation is False:
                cmds.connectAttr(source_path, target_path, force=1)
            else:
                source_data_type, target_data_type = (
                    source.data_type,
                    target.data_type
                )
                if source_data_type == target_data_type:
                    cmds.connectAttr(source_path, target_path, force=1)
                else:
                    source_is_channel = source.get_is_channel()
                    source_has_channels = source.get_has_channels()
                    target_is_channel = target.get_is_channel()
                    target_has_channels = target.get_has_channels()
                    check = [source_is_channel, source_has_channels, target_is_channel, target_has_channels]
                    # port / channel >> port / channel
                    if check in [
                        # port >> port
                        [False, False, False, False],
                        # port >> channel
                        [False, False, True, False],
                        # channel >> channel
                        [True, False, True, False],
                        # channel >> port
                        [True, False, False, False],
                    ]:
                        if cmds.isConnected(source_path, target_path) is False:
                            cmds.connectAttr(source_path, target_path, force=1)
                            bsc_log.Log.trace_method_result(
                                'port connect',
                                u'connection="{} >> {}"'.format(
                                    source_path,
                                    target_path
                                )
                            )
                    # port / channel >> [channel, channel, ...]
                    elif check in [
                        # port >> [channel, channel, ...]
                        [False, False, False, True],
                        # channel >> [channel, channel, ...]
                        [True, False, False, True],
                    ]:
                        target_channels = target.get_channels()
                        for target_channel in target_channels:
                            source_path, target_path = (
                                source.path, target_channel.path
                            )
                            if cmds.isConnected(source_path, target_path) is False:
                                cmds.connectAttr(source_path, target_path, force=1)
                                bsc_log.Log.trace_method_result(
                                    'port connect',
                                    u'connection="{} >> {}"'.format(
                                        source_path, target_path
                                    )
                                )
                    # [channel, channel, ...] >> [channel, channel, ...]
                    elif check == [False, True, False, True]:
                        source_channels = source.get_channels()
                        for seq, source_channel in enumerate(source_channels):
                            target_channel = target.get_channel_at(seq)
                            if target_channel is not None:
                                source_path, target_path = (
                                    source_channel.path, target_channel.path
                                )
                                if cmds.isConnected(source_path, target_path) is False:
                                    cmds.connectAttr(source_path, target_path, force=1)
                                    bsc_log.Log.trace_method_result(
                                        'port connect',
                                        u'connection="{} >> {}"'.format(
                                            source_path, target_path
                                        )
                                    )
                    # [channel, channel, ...] >> port / channel
                    elif check in [
                        # [channel, channel, ...] >> port
                        [False, True, False, False],
                        # [channel, channel, ...] >> channel
                        [False, True, True, False],
                    ]:
                        # alpha_channel = source.get_alpha_channel()
                        # if alpha_channel is not None:
                        #     source_channel = alpha_channel
                        # else:
                        #     source_channels = source.get_channels()
                        #     source_channel = source_channels[0]
                        #
                        source_channels = source.get_channels()
                        source_channel = source_channels[0]
                        #
                        source_path, target_path = (
                            source_channel.path, target.path
                        )
                        if cmds.isConnected(source_path, target_path) is False:
                            cmds.connectAttr(source_path, target_path, force=1)
                            bsc_log.Log.trace_method_result(
                                'port connect',
                                u'connection="{} >> {}"'.format(
                                    source_path, target_path
                                )
                            )
                    else:
                        bsc_log.Log.trace_method_warning(
                            'port connect',
                            u'connection="{} >> {}" is not available'.format(
                                source_path, target_path
                            )
                        )

    def get_is_locked(self):
        return cmds.getAttr(
            self.path, lock=1
        )

    def set_unlock(self):
        cmds.setAttr(
            self.path, lock=0
        )
        bsc_log.Log.trace_method_result(
            'port unlock',
            'attribute="{}"'.format(self.path)
        )


class AbsMyaNodeConnection(bsc_dcc_abstracts.AbsDccNodeConnection):
    def __init__(self, source, target):
        super(AbsMyaNodeConnection, self).__init__(source, target)


class AbsMyaShapeDef(object):
    PATHSEP = None
    TRANSFORM_CLS = None

    def _set_ma_shape_def_init_(self, shape_path):
        transform_path = self.PATHSEP.join(shape_path.split(self.PATHSEP)[:-1])
        self._transform = self.TRANSFORM_CLS(transform_path)

    def get_transform(self):
        return self._transform

    transform = property(get_transform)


class AbsMaUuidDef(object):
    def _set_ma_uuid_def_(self, uuid):
        self._uuid = uuid

    def get_unique_id(self):
        return self._uuid

    unique_id = property(get_unique_id)

    @property
    def path(self):
        raise NotImplementedError()

    def set_unique_id(self, unique_id):
        if cmds.objExists(self.path):
            if not cmds.ls(unique_id, long=1):
                cmds.rename(self.path, unique_id, uuid=1)
                bsc_log.Log.trace_result('set unique-id: "{}" >> "{}"'.format(self.path, unique_id))
            else:
                bsc_log.Log.trace_warning('unique-id: "{}" is Exists'.format(unique_id))


# noinspection PyUnusedLocal
class AbsMyaNode(
    bsc_dcc_abstracts.AbsDccNode,
    AbsMaUuidDef
):
    KEY = 'maya node'
    PATHSEP = mya_core.MyaUtil.OBJ_PATHSEP

    def __init__(self, path):
        _ = path
        if cmds.objExists(_):
            uuid = cmds.ls(_, uuid=1)[0]
            path_arg = cmds.ls(_, long=1)[0]
        else:
            uuid = None
            path_arg = _
        #
        self._set_ma_uuid_def_(uuid)
        super(AbsMyaNode, self).__init__(path_arg)

    def get_type(self):
        if cmds.objExists(self.path) is True:
            return cmds.nodeType(self.path)
        return '*'

    type = property(get_type)

    def get_api_type(self):
        return cmds.nodeType(self.get_path(), apiType=1)

    api_type = property(get_api_type)

    def get_icon(self):
        if mya_core.MyaUtil.get_is_ui_mode():
            import lxgui.qt.core as gui_qt_core

            return gui_qt_core.GuiQtMaya.generate_qt_icon_by_name(self.type)

    icon = property(get_icon)

    @classmethod
    def _to_full_path(cls, string):
        if cmds.objExists(string) is True:
            if not string.startswith(mya_core.MyaUtil.OBJ_PATHSEP):
                return cmds.ls(string, long=1)[0]
            return string
        return string

    def _update_path_(self):
        if self.get_unique_id():
            _ = cmds.ls(self.get_unique_id(), long=1)
            print _
            if _:
                self._path = _[0]

    def get_is_exists(self):
        return cmds.objExists(self.path)

    def get_is_referenced(self):
        return cmds.referenceQuery(self.path, isNodeReferenced=1)

    def get_is_lock(self):
        return cmds.lockNode(self.path, query=1, lock=1) == [True]

    def set_unlock(self):
        cmds.lockNode(self.path, lock=0)
        cmds.warning('unlock node: {}'.format(self.path))
        bsc_log.Log.trace_method_result(
            self.KEY,
            'unlock node: {}'.format(self.path)
        )

    def set_lock(self):
        cmds.lockNode(self.path, lock=1)
        cmds.warning('lock node: {}'.format(self.path))
        bsc_log.Log.trace_method_result(
            self.KEY,
            'lock node: {}'.format(self.path)
        )

    # noinspection PyUnusedLocal
    def do_delete(self, force=False):
        if self.get_is_exists() is True:
            if self.get_is_lock() is True:
                self.set_unlock()
            #
            cmds.delete(self.path)
            bsc_log.Log.trace_method_result(
                self.KEY,
                'delete: "{}"'.format(self.path)
            )

    def set_to_world(self):
        if self.get_is_exists() is True:
            cmds.parent(self.path, world=1)

    # noinspection PyUnusedLocal
    def set_rename(self, new_name, force=False):
        if self.get_is_exists() is True:
            cmds.rename(self.path, new_name)
            self._update_path_()
            bsc_log.Log.trace_method_result(
                self.KEY,
                'rename: "{}" >> "{}"'.format(self.path, new_name)
            )

    def set_repath(self, new_obj_path):
        new_dcc_path_dag_opt = bsc_core.PthNodeOpt(new_obj_path)
        new_dcc_parent_dag_opt = new_dcc_path_dag_opt.get_parent()
        new_parent_dcc_obj = self.__class__(new_dcc_parent_dag_opt.path)
        if new_parent_dcc_obj.get_is_exists() is True:
            self.set_parent(new_parent_dcc_obj)
            new_name = new_dcc_path_dag_opt.name
            if new_name != self.name:
                self._update_path_()
                self.set_rename(new_name)

    def set_boolean_attribute_add(self, port_path, value=False):
        attribute = self.get_port(port_path)
        attribute.set_create(raw_type='bool')
        attribute.set(value)

    # naming overlapped
    def get_is_naming_overlapped(self):
        return len(self.get_naming_overlapped_paths()) > 1

    def get_naming_overlapped_paths(self):
        return cmds.ls(self.name) or []

    # instance
    def get_is_instanced(self):
        dag_node = om2.MFnDagNode(om2.MGlobal.getSelectionListByName(self.path).getDagPath(0))
        return dag_node.isInstanced()

    # history
    def get_history_paths(self):
        return mya_core.MyaNodeUtil.get_all_history_paths(self.path)

    def set_history_clear(self):
        cmds.delete(self.path, constructionHistory=1)

    def get_source_node_paths(self, type_includes=None):
        if type_includes:
            lis = []
            for node_type in type_includes:
                _ = cmds.listConnections(self.path, destination=0, source=1, type=node_type) or []
                for i in _:
                    lis.append(i)
            return lis
        return cmds.listConnections(self.path, destination=0, source=1) or []

    def get_target_node_paths(self, type_includes=None):
        if type_includes:
            lis = []
            for node_type in type_includes:
                _ = cmds.listConnections(self.path, destination=1, source=0, type=node_type) or []
                for i in _:
                    lis.append(i)
            return lis
        return cmds.listConnections(self.path, destination=1, source=0) or []

    def create_ancestors(self):
        if self.path:
            if cmds.objExists(self.path) is False:
                paths = self.get_ancestor_paths()
                paths.reverse()
                #
                parent_string = None
                for i in paths:
                    name = i.split(self.PATHSEP)[-1]
                    if name:
                        if cmds.objExists(i) is False:
                            if parent_string is not None:
                                parent_string = cmds.group(empty=1, name=name, parent=parent_string)
                            else:
                                parent_string = cmds.group(empty=1, name=name)
                            #
                            bsc_log.Log.trace_method_result(
                                self.KEY,
                                u'create transform: "{}", parent is "{}"'.format(name, parent_string)
                            )
                        else:
                            parent_string = i

    def set_dag_components_create(self):
        if self.path:
            if cmds.objExists(self.path) is False:
                paths = self.get_dag_component_paths()
                paths.reverse()
                #
                parent_string = None
                for i in paths:
                    name = i.split(self.PATHSEP)[-1]
                    if name:
                        if cmds.objExists(i) is False:
                            if parent_string is not None:
                                parent_string = cmds.group(empty=1, name=name, parent=parent_string)
                            else:
                                parent_string = cmds.group(empty=1, name=name)
                            #
                            bsc_log.Log.trace_method_result(
                                'transform-obj-create',
                                u'obj-name="{}"'.format(name)
                            )
                        else:
                            parent_string = i

    def parent_to_path(self, parent_path, create_parent=False):
        if parent_path == self.PATHSEP:
            if cmds.listRelatives(self.path, parent=1):
                cmds.parent(self.path, world=1)
                bsc_log.Log.trace_method_result(
                    'parent set',
                    u'obj="{}"'.format(self.PATHSEP)
                )
        else:
            parent_obj = self.__class__(parent_path)
            self.set_parent(parent_obj, create_parent)

    def set_parent(self, parent_obj, create_parent=False):
        if parent_obj.get_is_exists() is True:
            current_parent_path = self.get_parent_path()
            if current_parent_path != parent_obj.path:
                cmds.parent(self.path, parent_obj.path)
                #
                bsc_log.Log.trace_method_result(
                    'parent set',
                    'obj="{}"'.format(parent_obj.path)
                )
            else:
                bsc_log.Log.trace_method_warning(
                    'parent set',
                    'obj="{}" is already child for "{}"'.format(self.get_path(), parent_obj.get_path())
                )
        else:
            bsc_log.Log.trace_method_warning(
                'parent set',
                'obj="{}" is non-exists'.format(parent_obj.path)
            )

    def get_dcc_instance(self, obj_type, obj_path=None, *args, **kwargs):
        if obj_path is None:
            obj_path = self.path
        #
        parent_path = self.PATHSEP.join(obj_path.split(self.PATHSEP)[:-1]) or None
        name = obj_path.split(self.PATHSEP)[-1]
        _ = obj_path
        is_create = False
        if 'compose' in kwargs:
            is_compose = kwargs['compose']
        else:
            is_compose = False
        #
        if cmds.objExists(obj_path) is False:
            is_create = True
            if is_compose is True:
                shape_name = '{}Shape'.format(name)
                shape_path = self.PATHSEP.join([obj_path, shape_name])
                _ = shape_path
                if cmds.objExists(shape_path) is False:
                    cmds.createNode('transform', name=name, parent=parent_path, skipSelect=1)
                    cmds.createNode(obj_type, name=shape_name, parent=obj_path, skipSelect=1)
            else:
                self.set_create(obj_type)
                # cmds.createNode(obj_type, name=name, parent=parent_path, skipSelect=1)
        return _, is_create

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            parent_path = self.get_parent_path()
            name = self.name
            bsc_log.Log.trace_method_result(
                'obj create',
                'obj="{}", type="{}"'.format(self.path, obj_type)
            )
            if parent_path is not None:
                return cmds.createNode(obj_type, name=name, parent=parent_path, skipSelect=1)
            else:
                return cmds.createNode(obj_type, name=name, skipSelect=1)

    def set_display_enable(self, boolean):
        self.get_port('visibility').set(boolean)

    def get_is_transform(self):
        if cmds.objExists(self.path):
            if cmds.nodeType(self.path) == 'transform':
                shape_paths = cmds.listRelatives(self.path, children=1, shapes=1, noIntermediate=0, fullPath=1) or []
                if shape_paths:
                    return True
                return False
            return False
        return False

    def get_is_shape(self):
        if cmds.objExists(self.path):
            if cmds.nodeType(self.path) != 'transform':
                transform_paths = cmds.listRelatives(self.path, parent=1, fullPath=1, type='transform') or []
                shape_paths = cmds.listRelatives(self.path, children=1, shapes=1, noIntermediate=0, fullPath=1) or []
                if transform_paths and not shape_paths:
                    return True
                return False
            return False
        return False

    def get_is_group(self):
        if cmds.objExists(self.path):
            if cmds.nodeType(self.path) == 'transform':
                shape_paths = cmds.listRelatives(self.path, children=1, shapes=1, noIntermediate=0, fullPath=1) or []
                if shape_paths:
                    return True
                return False
            return False
        return False

    # node is transform + shape
    def get_is_compose(self):
        return self.get_is_transform() or self.get_is_shape()

    def set_instance_to(self, obj_path):
        dcc_obj = self.__class__(obj_path)
        if dcc_obj.get_is_exists() is False:
            name = dcc_obj.name
            results = cmds.duplicate(
                self.path, name=name,
                instanceLeaf=1, returnRootsOnly=1
            )
            dcc_obj.create_ancestors()
            cmds.parent(results[0], dcc_obj.get_parent_path())

    def get_is_reference(self):
        return cmds.referenceQuery(self._path, isNodeReferenced=1)

    def _get_source_connection_raw_(self):
        lis = []
        _ = cmds.listConnections(self.path, destination=0, source=1, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq%2:
                source_atr_path = i
                target_atr_path = _[seq-1]
                #
                lis.append((source_atr_path, target_atr_path))
        return lis

    def _get_target_connection_raw_(self):
        lis = []
        _ = cmds.listConnections(self.path, destination=1, source=0, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq%2:
                source_atr_path = _[seq-1]
                target_atr_path = i
                #
                lis.append((source_atr_path, target_atr_path))
        return lis

    def set_visible(self, boolean):
        self.get_port('visibility').set(boolean)

    def make_identity(self, translate=1, rotate=1, scale=1):
        cmds.makeIdentity(
            self._path, apply=1, translate=translate, rotate=rotate, scale=scale
        )


class AbsMyaNodeForFileReference(
    AbsMyaNode,
    bsc_dcc_abstracts.AbsDccNodeFileReferenceDef
):
    def __init__(self, path, file_path=None):
        super(AbsMyaNodeForFileReference, self).__init__(path)
        # init file reference
        self._init_dcc_node_file_reference_def_(file_path)


class AbsMyaNodes(bsc_dcc_abstracts.AbsDccNodes):
    def __init__(self, *args):
        super(AbsMyaNodes, self).__init__(*args)

    @classmethod
    def get_paths(cls, reference=True, paths_exclude=None):
        def set_exclude_filter_fnc_(paths):
            if paths_exclude is not None:
                [paths.remove(_i) for _i in paths_exclude if _i in paths]
            return paths

        _ = cmds.ls(type=cls.DCC_TYPES_INCLUDE, long=1) or []
        if paths_exclude is not None:
            return set_exclude_filter_fnc_(_)
        if reference is True:
            return _
        return set_exclude_filter_fnc_(
            [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]
        )
