# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core


class ACResource(object):
    def __init__(self, namespace):
        self._namespace = namespace

    @classmethod
    def find_setch_fnc(cls, namespace, key):
        _ = cmds.ls('{}:ACBRig_{}lN'.format(namespace, key), long=1)
        if _:
            return _[0]

    @classmethod
    def create_locators(cls, data):
        translate_atr_names = [
            'translateX', 'translateY', 'translateZ',
        ]

        rotate_atr_names = [
            'rotateX', 'rotateY', 'rotateZ'
        ]

        for k, v in data.items():
            i_flag, i_locator = qsm_mya_core.VectorLocator.create('|sketch_{}_loc'.format(k))

            i_translate_curve_opts = []
            for j_atr_name in translate_atr_names:
                j_curve_name = qsm_mya_core.NodeAttributeKeyframe.find_curve_node(i_locator, j_atr_name)
                if j_curve_name is None:
                    j_curve_name = qsm_mya_core.NodeAttributeKeyframe.create_at(
                        i_locator, j_atr_name, 0
                    )

                i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(j_curve_name)
                i_translate_curve_opts.append(i_curve_opt)

            i_rotate_curve_opts = []
            for j_atr_name in rotate_atr_names:
                j_curve_name = qsm_mya_core.NodeAttributeKeyframe.find_curve_node(i_locator, j_atr_name)
                if j_curve_name is None:
                    j_curve_name = qsm_mya_core.NodeAttributeKeyframe.create_at(
                        i_locator, j_atr_name, 0
                    )

                i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(j_curve_name)
                i_rotate_curve_opts.append(i_curve_opt)

            for j_idx, j in enumerate(v):
                j_frame, j_matrix, j_translate, j_rotate = j

                for x_idx, x in enumerate(j_translate):
                    i_translate_curve_opts[x_idx].create_value_at_time(j_frame, x)

                for x_idx, x in enumerate(j_rotate):
                    i_rotate_curve_opts[x_idx].create_value_at_time(j_frame, x)

    def apply_to_sketches(self, data):
        translate_atr_names = [
            'translateX', 'translateY', 'translateZ',
        ]

        rotate_atr_names = [
            'rotateX', 'rotateY', 'rotateZ'
        ]

        for k, v in data.items():
            i_sketch = self.find_setch_fnc(self._namespace, k)
            if not i_sketch:
                continue

            i_translate_curve_opts = []
            for j_atr_name in translate_atr_names:
                j_curve_name = qsm_mya_core.NodeAttributeKeyframe.find_curve_node(i_sketch, j_atr_name)
                if j_curve_name is None:
                    j_curve_name = qsm_mya_core.NodeAttributeKeyframe.create_at(
                        i_sketch, j_atr_name, 0
                    )
                i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(j_curve_name)
                i_translate_curve_opts.append(i_curve_opt)

            i_rotate_curve_opts = []
            for j_atr_name in rotate_atr_names:
                j_curve_name = qsm_mya_core.NodeAttributeKeyframe.find_curve_node(i_sketch, j_atr_name)
                if j_curve_name is None:
                    j_curve_name = qsm_mya_core.NodeAttributeKeyframe.create_at(
                        i_sketch, j_atr_name, 0
                    )
                i_curve_opt = qsm_mya_core.AnmCurveNodeOpt(j_curve_name)
                i_rotate_curve_opts.append(i_curve_opt)

            with qsm_mya_core.auto_keyframe_context(True):
                for j_idx, j in enumerate(v):
                    j_frame, j_matrix, j_translate, j_rotate = j

                    qsm_mya_core.Frame.set_current(j_frame)
                    # if k in {
                    #     '7_1', '8_1',
                    #     '3_4', '3_8', '3_12', '3_16', '3_20',
                    #     '4_4', '4_8', '4_12', '4_16', '4_20',
                    # }:
                    #     qsm_mya_core.Transform.set_world_transformation(i_sketch, j_translate, j_rotate)
                    # else:
                    #     qsm_mya_core.Transform.set_world_translation(i_sketch, j_translate)
                    qsm_mya_core.Transform.set_world_rotation(i_sketch, j_rotate)

    @classmethod
    def test(cls):
        namespace = 'HumanBRIG'
        data = bsc_storage.StgFileOpt(
            'Z:/resources/anim_craft/Bow_Crouch_2_Idle_Aim.json'
        ).set_read()

        cls.create_locators(data)
        # cls(namespace).apply_to_sketches(
        #     data
        # )

