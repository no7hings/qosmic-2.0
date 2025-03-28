# coding:utf-8
import enum
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .. import core as _mya_core


class AbsMotion(object):
    class ControlDirections(enum.IntEnum):
        Left = 0
        Right = 1
        Middle = 2
        Unknown = -1

    class MirrorSchemes(enum.IntEnum):
        LeftToRight = 0
        RightToLeft = 1
        Auto = 2

    @classmethod
    def find_one_control_fnc(cls, control_key, namespace):
        if namespace:
            _ = cmds.ls('{}:{}'.format(namespace, control_key), long=1)
            if _:
                return _[0]
        else:
            _ = cmds.ls(control_key, long=1)
            if _:
                return _[0]


class NodeMotion(AbsMotion):
    @classmethod
    def get(cls, path, key_includes=None):
        if isinstance(key_includes, (tuple, list)):
            keys = [x for x in key_includes if _mya_core.NodeAttribute.is_exists(path, x) is True]
        else:
            keys = _mya_core.NodeAttributes.get_all_keyable_names(path)

        list_ = []
        for i_atr_name in keys:
            # fixme: use attribute connection?
            i_curve_node = _mya_core.NodeAttributeKeyframeOpt(path, i_atr_name).find_curve_node()
            if i_curve_node is not None:
                i_curve_type = cmds.nodeType(i_curve_node)
                i_infinities = [
                    _mya_core.NodeAttribute.get_value(i_curve_node, 'preInfinity'),
                    _mya_core.NodeAttribute.get_value(i_curve_node, 'postInfinity')
                ]
                i_curve_points = _mya_core.NodeAttributeKeyframeOpt(path, i_atr_name).get_points()
                list_.append((i_atr_name, i_curve_type, i_infinities, i_curve_points))
            else:
                i_value = _mya_core.NodeAttribute.get_value(path, i_atr_name)
                list_.append((i_atr_name, i_value))
        return list_

    @classmethod
    def get_all_curve_nodes(cls, path, key_includes=None):
        if isinstance(key_includes, (tuple, list)):
            keys = [x for x in key_includes if _mya_core.NodeAttribute.is_exists(path, x) is True]
        else:
            keys = _mya_core.NodeAttributes.get_all_keyable_names(path)

        list_ = []
        for i_atr_name in keys:
            i_curve_node = _mya_core.NodeAttributeKeyframeOpt(path, i_atr_name).find_curve_node()
            if i_curve_node:
                list_.append(i_curve_node)
        return list_

    @classmethod
    def generate_motion_properties_fnc(cls, path, key_includes=None):
        if key_includes is None:
            key_includes = _mya_core.NodeAttributes.get_all_keyable_names(path)
        return _mya_core.EtrNodeOpt(path).generate_motion_properties(key_includes)

    @classmethod
    def generate_pose_properties_fnc(cls, path, key_includes=None):
        if key_includes is None:
            key_includes = _mya_core.NodeAttributes.get_all_keyable_names(path)
        return _mya_core.EtrNodeOpt(path).generate_pose_properties(key_includes)

    @classmethod
    def apply_motion_properties_fnc(cls, path, data, **kwargs):
        _mya_core.EtrNodeOpt(path).apply_motion_properties(data, **kwargs)

    @classmethod
    def apply_pose_properties_fnc(cls, path, data, **kwargs):
        _mya_core.EtrNodeOpt(path).apply_pose_properties(data, **kwargs)
