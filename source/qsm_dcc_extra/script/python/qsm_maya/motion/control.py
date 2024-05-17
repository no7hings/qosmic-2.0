# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core


class ControlOpt(object):
    @classmethod
    def to_control_name(cls, path):
        return path.split('|')[-1].split(':')[-1]

    @classmethod
    def apply_value(cls, path, atr_data, force=False):
        atr_name, value = atr_data
        if qsm_mya_core.NodeAttribute.is_exists(path, atr_name) is False:
            return
        if qsm_mya_core.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if qsm_mya_core.Reference.is_from_reference(path) is True:
                return
            if force is True:
                qsm_mya_core.NodeAttribute.unlock(path, atr_name)
            else:
                return
        if qsm_mya_core.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                result = qsm_mya_core.NodeAttribute.break_source(path, atr_name)
                if result is False:
                    return
            else:
                return
        value_dst = qsm_mya_core.NodeAttribute.get_value(path, atr_name)
        if value != value_dst:
            qsm_mya_core.NodeAttribute.set_value(path, atr_name, value)

    @classmethod
    def apply_curve(cls, path, atr_data, frame_offset=0, force=False):
        atr_name, curve_type, infinities, curve_points = atr_data
        if qsm_mya_core.NodeAttribute.is_exists(path, atr_name) is False:
            return
        if qsm_mya_core.NodeAttribute.is_lock(path, atr_name) is True:
            # when node is from reference, ignore
            if qsm_mya_core.Reference.is_from_reference(path) is True:
                return
            if force is True:
                qsm_mya_core.NodeAttribute.unlock(path, atr_name)
            else:
                return
        if qsm_mya_core.NodeAttribute.has_source(path, atr_name) is True:
            if force is True:
                qsm_mya_core.NodeAttribute.break_source(path, atr_name)
            else:
                return

        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            atr_name.replace('.', '_')
        )
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        i_atr_path_src = '{}.output'.format(curve_name_new)
        i_atr_path_dst = '{}.{}'.format(path, atr_name)
        qsm_mya_core.Connection.create(i_atr_path_src, i_atr_path_dst)

        qsm_mya_core.AnimationCurveOpt(path, atr_name).set_points(curve_points, frame_offset=frame_offset)

        qsm_mya_core.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', infinities[0]
        )
        qsm_mya_core.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', infinities[0]
        )

    def __init__(self, path):
        self._path = path

    def get_animation(self):
        list_ = []
        for i_atr_name in qsm_mya_core.NodeAttributes.get_all_keyable_names(self._path):
            i_curve_name = qsm_mya_core.NodeAttribute.get_source_node(self._path, i_atr_name, 'animCurve')
            if i_curve_name is not None:
                i_curve_type = cmds.nodeType(i_curve_name)
                i_infinities = [
                    qsm_mya_core.NodeAttribute.get_value(i_curve_name, 'preInfinity'),
                    qsm_mya_core.NodeAttribute.get_value(i_curve_name, 'postInfinity')
                ]
                i_curve_points = qsm_mya_core.AnimationCurveOpt(self._path, i_atr_name).get_points()
                list_.append((i_atr_name, i_curve_type, i_infinities, i_curve_points))
            else:
                i_value = qsm_mya_core.NodeAttribute.get_value(self._path, i_atr_name)
                list_.append((i_atr_name, i_value))
        return list_

    def apply_animation(self, motion, frame_offset=0, force=False):
        for i_atr_data in motion:
            if len(i_atr_data) == 2:
                self.apply_value(self._path, i_atr_data, force=force)
            else:
                self.apply_curve(self._path, i_atr_data, frame_offset=frame_offset, force=force)

    def transfer_animation_to(self, path_dst, **kwargs):
        motion = self.get_animation()
        self.__class__(path_dst).apply_animation(motion, **kwargs)
