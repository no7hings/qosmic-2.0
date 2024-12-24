# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class NodeAttribute:
    @classmethod
    def to_atr_path(cls, path, atr_name=None):
        if atr_name is None:
            return path
        return '{}.{}'.format(path, atr_name)

    @classmethod
    def to_node_path(cls, name):
        _ = cmds.ls(name, long=1)
        if not _:
            raise RuntimeError()
        return _[0]

    @classmethod
    def get_type(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), type=1)

    @classmethod
    def get_value(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name))

    @classmethod
    def get_is_value(cls, path, atr_name, value):
        if cls.is_exists(path, atr_name):
            _ = cls.get_value(path, atr_name)
            if value == _:
                return True
        return False

    @classmethod
    def get_channel_box_enable(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), channelBox=True, keyable=True)

    @classmethod
    def get_is_locked(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), lock=1)

    @classmethod
    def get_as_string(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), asString=True) or ''

    @classmethod
    def set_value(cls, path, atr_name, value):
        # value may over maximum value?
        cmds.setAttr(cls.to_atr_path(path, atr_name), value, clamp=1)

    @classmethod
    def set_as_tuple(cls, path, atr_name, value):
        cmds.setAttr(cls.to_atr_path(path, atr_name), *value, clamp=1)

    @classmethod
    def set_as_string(cls, path, atr_name, value):
        cmds.setAttr(cls.to_atr_path(path, atr_name), value, type='string')

    @classmethod
    def is_lock(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), lock=1)

    @classmethod
    def set_visible(cls, path, boolean):
        cmds.setAttr(
            cls.to_atr_path(path, 'visibility'), boolean
        )

    @classmethod
    def is_exists(cls, path, atr_name):
        return cmds.objExists(
            cls.to_atr_path(path, atr_name)
        )

    @classmethod
    def unlock(cls, path, atr_name):
        cmds.setAttr(cls.to_atr_path(path, atr_name), lock=0)

    @classmethod
    def is_settable(cls, path, atr_name):
        return cmds.getAttr(cls.to_atr_path(path, atr_name), settable=1)

    # source
    @classmethod
    def connect_from(cls, path, atr_name, source):
        atr_path_tgt = cls.to_atr_path(path, atr_name)
        cmds.connectAttr(source, atr_path_tgt, force=1)

    @classmethod
    def has_source(cls, path, atr_name):
        return cmds.connectionInfo(
            cls.to_atr_path(path, atr_name),
            isDestination=1
        )

    @classmethod
    def break_source(cls, path, atr_name):
        atr_path_tgt = cls.to_atr_path(path, atr_name)
        atr_path_src = cmds.connectionInfo(
            atr_path_tgt,
            sourceFromDestination=1
        )
        if atr_path_src:
            path_src = atr_path_src.split('.')[0]
            if not cmds.referenceQuery(path_src, isNodeReferenced=1):
                cmds.disconnectAttr(atr_path_src, atr_path_tgt)
                return True
        return False

    @classmethod
    def get_source(cls, path, atr_name, skip_conversion_nodes=1):
        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name),
            destination=0, source=1, plugs=1,
            skipConversionNodes=skip_conversion_nodes
        )
        if _:
            return _[0]

    @classmethod
    def get_source_node(cls, path, atr_name, node_type=None, skip_conversion_nodes=0, shapes=1):
        # ignore when attribute is non exists
        atr_path = cls.to_atr_path(path, atr_name)
        if cmds.objExists(atr_path) is False:
            return

        kwargs = dict(
            destination=0, source=1, shapes=shapes,
            skipConversionNodes=skip_conversion_nodes
        )
        if node_type is not None:
            kwargs['type'] = node_type

        _ = cmds.listConnections(
            atr_path, **kwargs
        ) or []
        if _:
            return cls.to_node_path(_[0])

    # targets
    @classmethod
    def connect_to(cls, path, atr_name, target):
        atr_path_src = cls.to_atr_path(path, atr_name)
        cmds.connectAttr(atr_path_src, target, force=1)

    @classmethod
    def break_targets(cls, path, atr_name):
        atr_path_src = cls.to_atr_path(path, atr_name)
        atr_path_tgt_s = cmds.connectionInfo(
            atr_path_src,
            destinationFromSource=1
        ) or []
        for i_atr_path_tgt in atr_path_tgt_s:
            i_path_tgt = i_atr_path_tgt.split('.')[0]
            if not cmds.referenceQuery(i_path_tgt, isNodeReferenced=1):
                cmds.disconnectAttr(atr_path_src, i_atr_path_tgt)

    @classmethod
    def get_targets(cls, path, atr_name):
        return cmds.listConnections(
            cls.to_atr_path(path, atr_name), destination=1, source=0, plugs=1
        ) or []

    @classmethod
    def get_all_source_connections(cls, node_or_attribute):
        list_ = []
        _ = cmds.listConnections(node_or_attribute, destination=0, source=1, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq%2:
                source_atr_path = i
                target_atr_path = _[seq - 1]
                #
                list_.append((source_atr_path, target_atr_path))
        return list_

    @classmethod
    def get_all_target_connections(cls, node_or_attribute):
        lis = []
        _ = cmds.listConnections(node_or_attribute, destination=1, source=0, connections=1, plugs=1) or []
        # ["source-atr-node_or_attribute", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq%2:
                source_atr_path = _[seq-1]
                target_atr_path = i
                #
                lis.append((source_atr_path, target_atr_path))
        return lis

    @classmethod
    def get_target_nodes(cls, path, atr_name, node_type=None, skip_conversion_nodes=0, shapes=1):
        kwargs = dict(
            destination=1, source=0, skipConversionNodes=skip_conversion_nodes, shapes=shapes
        )
        if node_type is not None:
            kwargs['type'] = node_type

        return [cls.to_node_path(x) for x in cmds.listConnections(cls.to_atr_path(path, atr_name), **kwargs) or []]

    @classmethod
    def create_as_string(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, dataType='string')

        if default is not None:
            cls.set_as_string(path, atr_name, default)

    @classmethod
    def create_as_group(cls, path, atr_name, child_number):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(
                path, longName=atr_name, numberOfChildren=child_number, attributeType='compound'
            )

    @classmethod
    def create_as_boolean(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, attributeType='bool', keyable=1)
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_time(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, attributeType='time', keyable=1)
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_message(cls, path, atr_name, default=None, **kwargs):
        if cls.is_exists(path, atr_name) is False:
            options = dict(
                longName=atr_name, attributeType='message', keyable=1
            )
            options.update(**kwargs)
            cmds.addAttr(path, **options)
        if default is not None:
            cmds.connectAttr(
                default+'.message', path+'.'+atr_name
            )

    @classmethod
    def set_as_message(cls, path, atr_name, value):
        cmds.connectAttr(
            value+'.message', path+'.'+atr_name
        )

    @classmethod
    def get_as_message(cls, path, atr_name):
        _ = cmds.listConnections(
            cls.to_atr_path(path, atr_name), destination=0, source=1
        )
        if _:
            return _[0].split('.')[0]

    @classmethod
    def create_as_integer(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(path, longName=atr_name, attributeType='long', keyable=1)
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_float(cls, path, atr_name, default=None, **kwargs):
        if cls.is_exists(path, atr_name) is False:
            options = dict(
                longName=atr_name, attributeType='double', keyable=1
            )
            options.update(**kwargs)
            cmds.addAttr(path, **options)
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_length(cls, path, atr_name, default=None, **kwargs):
        if cls.is_exists(path, atr_name) is False:
            options = dict(
                longName=atr_name, attributeType='doubleLinear', keyable=1
            )
            options.update(**kwargs)
            cmds.addAttr(path, **options)
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_size(cls, path, atr_name, default=None, **kwargs):
        if cls.is_exists(path, atr_name) is False:
            options = dict(
                longName=atr_name, attributeType='double2', keyable=1
            )
            options.update(**kwargs)
            cmds.addAttr(path, **options)

            cmds.addAttr(
                path, longName=atr_name+'Width', attributeType='double', parent=atr_name, keyable=1
            )
            cmds.addAttr(
                path, longName=atr_name+'Height', attributeType='double', parent=atr_name, keyable=1
            )
        if default is not None:
            cls.set_as_tuple(path, atr_name, default)

    @classmethod
    def create_as_float3(cls, path, atr_name, default=None, **kwargs):
        if cls.is_exists(path, atr_name) is False:
            options = dict(
                longName=atr_name, attributeType='double3', keyable=1
            )
            options.update(**kwargs)
            cmds.addAttr(path, **options)
            cmds.addAttr(
                path, longName=atr_name+'X', attributeType='double', parent=atr_name, keyable=1
            )
            cmds.addAttr(
                path, longName=atr_name+'Y', attributeType='double', parent=atr_name, keyable=1
            )
            cmds.addAttr(
                path, longName=atr_name+'Z', attributeType='double', parent=atr_name, keyable=1
            )
        if default is not None:
            cls.set_as_tuple(path, atr_name, default)

    @classmethod
    def create_as_angle(cls, path, atr_name, default=None, **kwargs):
        if cls.is_exists(path, atr_name) is False:
            options = dict(
                longName=atr_name, attributeType='doubleAngle', keyable=1
            )
            options.update(**kwargs)
            cmds.addAttr(path, **options)
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_enumerate(cls, path, atr_name, options, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(
                path, longName=atr_name, attributeType='enum', enumName=':'.join(options), keyable=1
            )
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def create_as_matrix(cls, path, atr_name, default=None):
        if cls.is_exists(path, atr_name) is False:
            cmds.addAttr(
                path, longName=atr_name, dataType='matrix', keyable=1
            )
        if default is not None:
            cls.set_value(path, atr_name, default)

    @classmethod
    def get_array_indices(cls, path, atr_name):
        if cls.is_exists(path, atr_name) is True:
            return cmds.getAttr(
                cls.to_atr_path(path, atr_name),
                multiIndices=1,
                silent=1
            ) or []
        return []


class NodeAttributes:

    @classmethod
    def get_all_keyable_names(cls, node):
        return cmds.listAttr(node, keyable=1, unlocked=1) or []

    @classmethod
    def get_all_names(cls, node):
        return cmds.listAttr(
            node,
            read=1,
            write=1,
            inUse=1,
            # fixme: use multi?
            # multi=1
        ) or []
