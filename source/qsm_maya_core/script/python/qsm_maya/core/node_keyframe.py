# coding:utf-8
import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import reference as _reference

from . import connection as _connection


class NodeAttributeKeyframe:
    @classmethod
    def find_curve_node(cls, path, atr_name):
        _ = cmds.findKeyframe(
            path, curve=1, at=atr_name
        )
        if _:
            return _[0]

    @classmethod
    def find_layer_node(cls, path, atr_name):
        _ = cmds.listConnections(
            _attribute.NodeAttribute.to_atr_path(path, atr_name),
            destination=0, source=1
        ) or []
        if _:
            node = _[0]
            if cmds.nodeType(node).startswith('animBlendNodeAdditive'):
                return node
        return None

    @classmethod
    def create_at(cls, path, atr_name, frame=0):
        cmds.setKeyframe(path, attribute=atr_name, time=frame)
        return cls.find_curve_node(path, atr_name)


class NodeAttributeKeyframeOpt(object):
    DATA_KEYS = [
        'inAngle', 'outAngle',
        'inWeight', 'outWeight',
        'inTangentType', 'outTangentType',
    ]

    def __init__(self, path, atr_name):
        self._path = path
        self._atr_name = atr_name

    def find_curve_node(self):
        return NodeAttributeKeyframe.find_curve_node(self._path, self._atr_name)

    def has_keyframe(self):
        return bool(self.find_curve_node())

    def get_index_count(self):
        return cmds.keyframe(
            self._path,
            attribute=self._atr_name,
            query=True,
            keyframeCount=True
        ) or 0

    def get_time_at(self, index):
        _ = cmds.keyframe(
            self._path,
            query=1,
            attribute=self._atr_name,
            index=(index, index),
            timeChange=1
        )
        if _:
            return _[0]

    def create_value_at_time(self, frame, value):
        cmds.setKeyframe(
            self._path,
            attribute=self._atr_name,
            time=(frame, frame),
            value=value
        )

    def get_value_at(self, index):
        _ = cmds.keyframe(
            self._path,
            query=1,
            attribute=self._atr_name,
            index=(index, index),
            valueChange=1
        )
        if _:
            return _[0]

    def set_out_tangent_type_at_time(self, frame, tangent_type):
        cmds.keyTangent(
            self._path, attribute=self._atr_name,
            time=(frame, frame), outTangentType=tangent_type
        )

    def get_tangents_at(self, index):
        list_ = []
        for i_key in self.DATA_KEYS:
            i_kwargs = dict(
                query=1,
                attribute=self._atr_name,
                index=(index, index),
            )
            i_kwargs[i_key] = 1
            _ = cmds.keyTangent(
                self._path, **i_kwargs
            )
            if _:
                list_.append(_[0])
            else:
                list_.append(None)
        return list_

    def set_tangents_at_time(self, frame, tangents):
        # fixme: set TangentType first? or weight first?
        tangents = copy.copy(tangents)
        tangents.reverse()
        keys = copy.copy(self.DATA_KEYS)
        keys.reverse()
        for i_seq, i_key in enumerate(keys):
            i_value = tangents[i_seq]

            i_kwargs = dict(
                attribute=self._atr_name,
                time=(frame, frame)
            )
            i_kwargs[i_key] = i_value
            cmds.keyTangent(
                self._path, **i_kwargs
            )

    def get_points(self):
        index_count = self.get_index_count()
        list_ = []
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_tangent = self.get_tangents_at(i_index)
            list_.append((i_time, i_value, i_tangent))
        return list_

    def set_points(self, points, frame_offset=0, value_factor=1):
        for i in points:
            i_time, i_value, i_tangents = i
            # fixme: time is None?
            if i_time is None:
                continue
            self.create_value_at_time(i_time+frame_offset, i_value*value_factor)
            self.set_tangents_at_time(i_time+frame_offset, i_tangents)

        if points:
            # fix tangent bug
            first_points = points[0]
            f_time, f_value, f_tangents = first_points
            # fixme: time is None?
            if f_time is None:
                return
            self.create_value_at_time(f_time+frame_offset, f_value*value_factor)
            self.set_tangents_at_time(f_time+frame_offset, f_tangents)

    def offset_all_values(self, offset_value):
        index_count = self.get_index_count()
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_value_new = i_value+offset_value
            self.create_value_at_time(i_time, i_value_new)

    def get_curve_data(self):
        curve_node = self.find_curve_node()
        return dict(
            type=cmds.nodeType(curve_node),
            points=self.get_points(),
            pre_infinity=cmds.getAttr(curve_node+'.preInfinity'),
            post_infinity=cmds.getAttr(curve_node+'.postInfinity')
        )
    
    @classmethod
    def apply_curve_data_to(cls, path, atr_name, data, frame_offset=0, force=False, mirror_keys=None):
        curve_type = data['type']
        curve_points = data['points']
        pre_infinity = data['pre_infinity']
        post_infinity= data['post_infinity']
        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return

        mirror_keys = mirror_keys or []
        if atr_name in mirror_keys:
            value_factor = -1
        else:
            value_factor = 1

        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return

        if _attribute.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if _reference.Reference.is_from_reference(path) is True:
                return
            if force is True:
                _attribute.NodeAttribute.unlock(path, atr_name)
            else:
                return

        if _attribute.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                _attribute.NodeAttribute.break_source(path, atr_name)
            else:
                return

        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            atr_name.replace('.', '_')
        )
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        i_atr_path_src = '{}.output'.format(curve_name_new)
        i_atr_path_dst = '{}.{}'.format(path, atr_name)
        _connection.Connection.create(i_atr_path_src, i_atr_path_dst)

        NodeAttributeKeyframeOpt(path, atr_name).set_points(
            curve_points, frame_offset=frame_offset, value_factor=value_factor
        )

        _attribute.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', pre_infinity
        )
        _attribute.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', post_infinity
        )

    def get_value_data(self):
        return dict(
            type=_attribute.NodeAttribute.get_type(self._path, self._atr_name),
            value=_attribute.NodeAttribute.get_value(self._path, self._atr_name)
        )

    @classmethod
    def apply_value_data_to(cls, path, atr_name, data, force=False, mirror_keys=None):
        # ignore non exists
        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return

        value = data['value']

        mirror_keys = mirror_keys or []
        if atr_name in mirror_keys:
            value = -value
        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return

        # ignore same value
        value_dst = _attribute.NodeAttribute.get_value(path, atr_name)
        if value == value_dst:
            return

        # try to unlock
        if _attribute.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if _reference.Reference.is_from_reference(path) is True:
                return

            if force is True:
                _attribute.NodeAttribute.unlock(path, atr_name)
            else:
                return

        # try to break source
        if _attribute.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                result = _attribute.NodeAttribute.break_source(path, atr_name)
                if result is False:
                    return
            else:
                return

        # ignore when is non settable
        if _attribute.NodeAttribute.is_settable(path, atr_name) is False:
            return

        _attribute.NodeAttribute.set_value(path, atr_name, value)

    @classmethod
    def apply_pose(cls, path, atr_name, data, mirror_keys=None):
        # ignore non exists
        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return

        if _attribute.NodeAttribute.is_settable(path, atr_name) is False:
            return

        value = data['value']

        mirror_keys = mirror_keys or []
        if atr_name in mirror_keys:
            value = -value
        if _attribute.NodeAttribute.is_exists(path, atr_name) is False:
            return

        # ignore same value
        value_dst = _attribute.NodeAttribute.get_value(path, atr_name)
        if value == value_dst:
            return

        _attribute.NodeAttribute.set_value(path, atr_name, value)


class NodeKeyframe(object):
    @classmethod
    def find_curve_nodes(cls, path):
        return cmds.findKeyframe(
            path, curve=1
        ) or []

    @classmethod
    def has_curve_node(cls, path):
        return bool(cls.find_curve_nodes(path))
