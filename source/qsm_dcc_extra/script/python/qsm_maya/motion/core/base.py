# coding:utf-8
import enum
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core


class MotionBase(object):
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


class Motion(MotionBase):
    @classmethod
    def get(cls, path, key_includes=None):
        if isinstance(key_includes, (tuple, list)):
            keys = [x for x in key_includes if _mya_core.NodeAttribute.is_exists(path, x) is True]
        else:
            keys = _mya_core.NodeAttributes.get_all_keyable_names(path)

        list_ = []
        for i_atr_name in keys:
            # fixme: use attribute connection?
            i_curve_node = _mya_core.NodePortAnmCurveOpt(path, i_atr_name).find_node()
            if i_curve_node is not None:
                i_curve_type = cmds.nodeType(i_curve_node)
                i_infinities = [
                    _mya_core.NodeAttribute.get_value(i_curve_node, 'preInfinity'),
                    _mya_core.NodeAttribute.get_value(i_curve_node, 'postInfinity')
                ]
                i_curve_points = _mya_core.NodePortAnmCurveOpt(path, i_atr_name).get_points()
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
            i_curve_node = _mya_core.NodePortAnmCurveOpt(path, i_atr_name).find_node()
            if i_curve_node:
                list_.append(i_curve_node)
        return list_

    @classmethod
    def apply(cls, path, data, **kwargs):
        force = kwargs.get('force', False)
        frame_offset = kwargs.get('frame_offset', 0)
        mirror_keys = kwargs.get('mirror_keys', [])
        data_includes = kwargs.get('data_includes', ['value', 'curve'])
        for i_atr_data in data:
            # value
            if len(i_atr_data) == 2:
                cls.apply_value(
                    path, i_atr_data, force=force, mirror_keys=mirror_keys
                )
            # curve
            if len(i_atr_data) == 4:
                cls.apply_curve(
                    path, i_atr_data, force=force, frame_offset=frame_offset, mirror_keys=mirror_keys
                )

    @classmethod
    def apply_value(cls, path, data, force, mirror_keys):
        key, value = data
        mirror_keys = mirror_keys or []
        if key in mirror_keys:
            value = -value
        if _mya_core.NodeAttribute.is_exists(path, key) is False:
            return
        # ignore same value
        value_dst = _mya_core.NodeAttribute.get_value(path, key)
        if value == value_dst:
            return

        if _mya_core.NodeAttribute.is_exists(path, key) is False:
            return
        # try to unlock
        if _mya_core.NodeAttribute.is_lock(path, key) is True:
            # when node is from reference, ignore
            if _mya_core.Reference.is_from_reference(path) is True:
                return

            if force is True:
                _mya_core.NodeAttribute.unlock(path, key)
            else:
                return
        # try to break source
        if _mya_core.NodeAttribute.has_source(path, key) is True:
            if force is True:
                result = _mya_core.NodeAttribute.break_source(path, key)
                if result is False:
                    return
            else:
                return

        _mya_core.NodeAttribute.set_value(path, key, value)

    @classmethod
    def apply_curve(cls, path, data, force, frame_offset, mirror_keys):
        key, curve_type, infinities, curve_points = data
        if _mya_core.NodeAttribute.is_exists(path, key) is False:
            return

        mirror_keys = mirror_keys or []
        if key in mirror_keys:
            value_factor = -1
        else:
            value_factor = 1

        if _mya_core.NodeAttribute.is_exists(path, key) is False:
            return

        if _mya_core.NodeAttribute.is_lock(path, key) is True:
            # when node is from reference, ignore
            if _mya_core.Reference.is_from_reference(path) is True:
                return
            if force is True:
                _mya_core.NodeAttribute.unlock(path, key)
            else:
                return

        if _mya_core.NodeAttribute.has_source(path, key) is True:
            if force is True:
                _mya_core.NodeAttribute.break_source(path, key)
            else:
                return

        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            key.replace('.', '_')
        )
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        i_atr_path_src = '{}.output'.format(curve_name_new)
        i_atr_path_dst = '{}.{}'.format(path, key)
        _mya_core.Connection.create(i_atr_path_src, i_atr_path_dst)

        _mya_core.NodePortAnmCurveOpt(path, key).set_points(
            curve_points, frame_offset=frame_offset, value_factor=value_factor
        )

        _mya_core.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', infinities[0]
        )
        _mya_core.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', infinities[1]
        )
