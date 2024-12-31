# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core


class ControlCurve(object):
    CURVE_TYPE_MAP = dict(
        translateX='animCurveTL',
        translateY='animCurveTL',
        translateZ='animCurveTL',
        rotateX='animCurveTA',
        rotateY='animCurveTA',
        rotateZ='animCurveTA',
        scaleX='animCurveTU',
        scaleY='animCurveTU',
        scaleZ='animCurveTU',
        visiblity='animCurveTU'
    )

    @classmethod
    def create(cls, path, atr_key, atr_name, values, start_frame, translation_scale=1.0):
        curve_name = '{}_{}'.format(
            path.split('|')[-1].split(':')[-1],
            atr_name.replace('.', '_')
        )
        curve_type = cls.CURVE_TYPE_MAP[atr_key]
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        atr_path_src = '{}.output'.format(curve_name_new)
        atr_path_tgt = '{}.{}'.format(path, atr_name)
        qsm_mya_core.Connection.create(atr_path_src, atr_path_tgt)

        curve_opt = qsm_mya_core.AnmCurveNodeOpt(curve_name_new)

        if atr_key in {
            'translateX',
            'translateY',
            'translateZ'
        }:
            value_scale = translation_scale
        else:
            value_scale = 1.0

        for i_index, i_value in enumerate(values):
            i_frame = i_index+start_frame
            curve_opt.create_value_at_time(i_frame, i_value*value_scale)

        return curve_name_new


class SketchCurve(object):
    CURVE_TYPE_MAP = dict(
        translateX='animCurveTL',
        translateY='animCurveTL',
        translateZ='animCurveTL',
        rotateX='animCurveTA',
        rotateY='animCurveTA',
        rotateZ='animCurveTA',
        scaleX='animCurveTU',
        scaleY='animCurveTU',
        scaleZ='animCurveTU',
        visiblity='animCurveTU'
    )

    @classmethod
    def to_curve_node_name(cls, sketch_path, atr_name):
        return '{}_{}'.format(
            sketch_path.split('|')[-1],
            atr_name.replace('.', '_')
        )

    @classmethod
    def create(cls, sketch_path, atr_name):
        curve_name = cls.to_curve_node_name(sketch_path, atr_name)
        if qsm_mya_core.Node.is_exists(curve_name) is True:
            return curve_name

        curve_type = cls.CURVE_TYPE_MAP[atr_name]
        curve_name_new = cmds.createNode(curve_type, name=curve_name, skipSelect=1)

        atr_path_src = '{}.output'.format(curve_name_new)
        atr_path_tgt = '{}.{}'.format(sketch_path, atr_name)
        qsm_mya_core.Connection.create(atr_path_src, atr_path_tgt)
        # setAttr "test:Hip_L_rotateZ.postInfinity" 4;
        qsm_mya_core.NodeAttribute.set_value(
            curve_name_new, 'preInfinity', 4
        )
        qsm_mya_core.NodeAttribute.set_value(
            curve_name_new, 'postInfinity', 4
        )
        return curve_name_new

    @classmethod
    def find_node(cls, sketch_path, atr_name):
        return qsm_mya_core.NodeAttribute.get_source_node(
            sketch_path, atr_name
        )

    @classmethod
    def appy_data(cls, curve_node, atr_name, values, start_frame, translation_scale):
        curve_opt = qsm_mya_core.AnmCurveNodeOpt(curve_node)

        if atr_name in {
            'translateX',
            'translateY',
            'translateZ'
        }:
            value_scale = translation_scale
        else:
            value_scale = 1.0

        for i_index, i_value in enumerate(values):
            i_frame = i_index+start_frame
            curve_opt.create_value_at_time(i_frame, i_value*value_scale)