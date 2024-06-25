# coding:utf-8
import copy

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import attribute as _attribute

from . import reference as _reference

from . import connection as _connection


class AnimationCurveOpt(object):
    DATA_KEYS = [
        'inAngle', 'outAngle',
        'inWeight', 'outWeight',
        'inTangentType', 'outTangentType',
    ]

    def __init__(self, path, atr_name):
        self._path = path
        self._atr_name = atr_name

    def get_node(self):
        _ = cmds.keyframe(
            self._path,
            attribute=self._atr_name,
            query=True,
            name=True
        )
        if _:
            return _[0]

    def get_index_count(self):
        return cmds.keyframe(
            self._path,
            attribute=self._atr_name,
            query=True,
            keyframeCount=True
        ) or []

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

    def set_value_at_time(self, time, value):
        cmds.setKeyframe(
            self._path,
            attribute=self._atr_name,
            time=(time, time),
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

    def set_tangents_at(self, time, tangents):
        # fixme: set TangentType first? or weight first?
        tangents = copy.copy(tangents)
        tangents.reverse()
        keys = copy.copy(self.DATA_KEYS)
        keys.reverse()
        for i_seq, i_key in enumerate(keys):
            i_value = tangents[i_seq]

            i_kwargs = dict(
                attribute=self._atr_name,
                time=(time, time)
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

    def set_points(self, points, frame_offset=0):
        for i in points:
            i_time, i_value, i_tangents = i
            self.set_value_at_time(i_time+frame_offset, i_value)
            self.set_tangents_at(i_time+frame_offset, i_tangents)

        if points:
            first_points = points[0]
            i_time, i_value, i_tangents = first_points
            self.set_value_at_time(i_time+frame_offset, i_value)
            self.set_tangents_at(i_time+frame_offset, i_tangents)

    def offset_all_values(self, offset_value):
        index_count = self.get_index_count()
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_value_new = i_value+offset_value
            self.set_value_at_time(i_time, i_value_new)


class Keyframe(object):

    @classmethod
    def apply_value(cls, path, atr_data, force=False):
        atr_name, value = atr_data
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
                result = _attribute.NodeAttribute.break_source(path, atr_name)
                if result is False:
                    return
            else:
                return
        value_dst = _attribute.NodeAttribute.get_value(path, atr_name)
        if value != value_dst:
            _attribute.NodeAttribute.set_value(path, atr_name, value)

    @classmethod
    def apply_curve(cls, path, atr_data, frame_offset=0, force=False):
        atr_name, curve_type, infinities, curve_points = atr_data
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

        AnimationCurveOpt(path, atr_name).set_points(curve_points, frame_offset=frame_offset)

        _attribute.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', infinities[0]
        )
        _attribute.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', infinities[1]
        )


class Keyframes(object):

    @classmethod
    def get_all(cls, path, atr_name):
        pass