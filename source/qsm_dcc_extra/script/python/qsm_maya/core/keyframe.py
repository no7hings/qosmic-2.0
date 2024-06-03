# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class AnimationCurveOpt(object):
    DATA_KEYS = [
        'inAngle', 'outAngle',
        'inWeight', 'outWeight',
        'inTangentType', 'outTangentType'
    ]

    def __init__(self, path, atr_name):
        self._path = path
        self._atr_name = atr_name

    def get_index_count(self):
        return cmds.keyframe(
            self._path,
            query=True,
            attribute=self._atr_name,
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

    def get_in_angle_at(self, index):
        _ = cmds.keyTangent(
            self._path,
            query=1,
            attribute=self._atr_name,
            index=(index, index),
            inAngle=1
        )
        if _:
            pass

    def get_tangent_at(self, index):
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

    def set_tangent_at(self, time, tangent):
        for i_seq, i_key in enumerate(self.DATA_KEYS):
            i_value = tangent[i_seq]

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
            i_tangent = self.get_tangent_at(i_index)
            list_.append((i_time, i_value, i_tangent))
        return list_

    def set_points(self, points, frame_offset=0):
        for i in points:
            i_time, i_value, i_tangent = i
            self.set_value_at_time(i_time+frame_offset, i_value)
            self.set_tangent_at(i_time+frame_offset, i_tangent)

    def offset_all_values(self, offset_value):
        index_count = self.get_index_count()
        for i_index in range(index_count):
            i_time = self.get_time_at(i_index)
            i_value = self.get_value_at(i_index)
            i_value_new = i_value+offset_value
            self.set_value_at_time(i_time, i_value_new)


class Keyframes(object):

    @classmethod
    def get_all(cls, path, atr_name):
        pass