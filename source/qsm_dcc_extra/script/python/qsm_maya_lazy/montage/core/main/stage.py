# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.model as bsc_model

import qsm_maya.core as qsm_mya_core

from ..base import keyframe as _bsc_keyframe

from . import layer as _layer


class MtgStage(object):

    @classmethod
    def find_master_layer_path(cls):
        _ = cmds.ls('*:MASTER_LAYER', long=1)
        if _:
            for i in _:
                if cmds.objExists('{}.qsm_type'.format(i)):
                    if cmds.getAttr('{}.qsm_type'.format(i)) == 'motion_master_layer':
                        return i

    def __init__(self):
        self._master_layer = self.find_master_layer_path()

    def generate_track_data(self):
        list_ = []
        if self._master_layer is None:
            return

        layer = _layer.MtgMasterLayer(self._master_layer)
        for i_path in layer.get_all_layers():
            i_kwargs = _layer.MtgLayer(i_path).generate_kwargs()
            list_.append(i_kwargs)
        return list_

    def generate_stage_model(self):
        stage_model = bsc_model.TrackStageModel()
        for i_kwargs in self.generate_track_data():
            stage_model.create_one(widget=None, **i_kwargs)
        return stage_model

    def get_all_layers(self):
        if self._master_layer is None:
            return []

        layer = _layer.MtgMasterLayer(self._master_layer)
        return layer.get_all_layers()

    def get_all_layer_names(self):
        if self._master_layer is None:
            return []

        layer = _layer.MtgMasterLayer(self._master_layer)
        return layer.get_all_layer_names()

    @classmethod
    def generate_root_locator(cls):
        stage = cls().generate_stage_model()
        tvl = stage.generate_travel()

        atr_names = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ',
        ]

        curve_opt_dict = {}

        path = '|ROOT_LOCATOR'

        qsm_mya_core.VectorLocator.create(path)

        for i_atr_name in atr_names:
            i_curve_opt = qsm_mya_core.AnmCurveNodeOpt.create(
                path, i_atr_name, keep_namespace=True, curve_type=_bsc_keyframe.ControlCurve.CURVE_TYPE_MAP[i_atr_name]
            )
            curve_opt_dict[i_atr_name] = i_curve_opt

        while tvl.is_valid():
            frame_range, track_model = tvl.current_data()
            namespace = track_model.key

            start_frame, end_frame = frame_range

            root_start = '{}:ROOT_START'.format(namespace)
            root_end = '{}:ROOT_END'.format(namespace)

            values_start = []
            translate_start = qsm_mya_core.Transform.get_world_translation(root_start)
            values_start.extend(translate_start)
            rotate_start = qsm_mya_core.Transform.get_world_rotation(root_start)
            values_start.extend(rotate_start)

            for i_idx, i_atr_name in enumerate(atr_names):
                i_curve_opt = curve_opt_dict[i_atr_name]
                i_curve_opt.create_value_at_time(start_frame, values_start[i_idx])
                i_curve_opt.set_tangent_types_at_time(start_frame, 'clamped', 'clamped')

            if tvl.is_end():
                values_end = []
                translate_end = qsm_mya_core.Transform.get_world_translation(root_end)
                values_end.extend(translate_end)
                rotate_end = qsm_mya_core.Transform.get_world_rotation(root_end)
                values_end.extend(rotate_end)
                for i_idx, i_atr_name in enumerate(atr_names):
                    i_curve_opt = curve_opt_dict[i_atr_name]
                    i_curve_opt.create_value_at_time(end_frame, values_end[i_idx])
                    i_curve_opt.set_tangent_types_at_time(end_frame, 'clamped', 'clamped')

            tvl.next()

    @classmethod
    def test(cls):
        cls.generate_root_locator()
