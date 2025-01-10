# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import lxbasic.model as bsc_model

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ..base import util as _bsc_util

from . import layer as _layer


class MtgStage(object):
    @classmethod
    def find_all_valid_rig_namespaces(cls):
        key = _bsc_util.MtgLayerNamespace.MASTER_LAYER_KEY

        list_ = []
        _ = cmds.ls('*:{}'.format(key), long=1)
        for i in _:
            i_name = i.split('|')[-1]
            i_namespace = i_name[:-len(key)-1]
            list_.append(i_namespace)
        return list_

    @classmethod
    def get_current_rig_namespace(cls):
        return _layer.MtgRoot.get_current_rig_namespace()

    @classmethod
    def update_by_stage(cls, rig_namespace, stage, current_frame=None):
        start_frame, end_frame = stage.track_start, stage.track_end

        qsm_mya_core.Frame.update_frame(start_frame, end_frame, current_frame)

        mtg_master_layer = _layer.MtgMasterLayer.find_one_master_layer(rig_namespace)

        tvl = stage.generate_travel()

        while tvl.is_valid():
            frame_range, track_model = tvl.current_data()

            is_start, is_end = tvl.is_start(), tvl.is_end()

            # when is start restore follow camera
            if is_start is True:
                mtg_master_layer.restore_root_loc_curves()

            if track_model is not None:
                pre_blend, post_blend = track_model.pre_blend, track_model.post_blend

                frame_range_index = track_model.get_frame_range_index(frame_range)
                key = track_model.key

                layer_name = _bsc_util.MtgRigNamespace.to_layer_name(rig_namespace, key)
                mtg_layer = _layer.MtgLayer(layer_name)

                for i_key in bsc_model.TrackModel.MAIN_KEYS:
                    mtg_layer.set(i_key, track_model.get(i_key))

                valid_start, valid_end = track_model.get_valid_start(), track_model.get_valid_end()

                mtg_layer.set('valid_start', valid_start)
                mtg_layer.set('valid_end', valid_end)
                mtg_layer.set('output_end', frame_range[-1])

                # check is start frame range
                if frame_range_index == 0:
                    # restore curves
                    mtg_layer.restore_main_weight_curve()
                    mtg_layer.restore_root_start_input_transformation_curves()

                next_is_valid = tvl.next_is_valid()

                if next_is_valid is False:
                    data_next = tvl.next_data()
                    if data_next is not None:
                        frame_range_next, track_model_next = data_next
                        frame_range = (frame_range[0], frame_range_next[-1])

                mtg_layer.update_main_weight(
                    frame_range, is_start, is_end, pre_blend, post_blend
                )

                model_last = tvl.last_model()
                if model_last:
                    key_last = model_last.key
                    layer_name_last = _bsc_util.MtgRigNamespace.to_layer_name(rig_namespace, key_last)
                    mtg_layer_last = _layer.MtgLayer(layer_name_last)
                    mtg_layer.update_root_start_fnc(mtg_layer, mtg_layer_last, frame_range[0])
                else:
                    if is_start:
                        # update root start
                        mtg_layer.update_root_start_by_self_fnc(mtg_layer, frame_range[0], frame_range[1])
                    else:
                        model_last_last = tvl.last_last_model()
                        if model_last_last:
                            key_last = model_last_last.key
                            layer_name_last = _bsc_util.MtgRigNamespace.to_layer_name(rig_namespace, key_last)
                            mtg_layer_last = _layer.MtgLayer(layer_name_last)
                            mtg_layer.update_root_start_fnc(mtg_layer, mtg_layer_last, frame_range[0])
                # todo: may chr is not move
                mtg_master_layer.update_root_loc_for(
                    mtg_layer, is_start, valid_start, valid_end
                )
            else:
                # when current is empty, use last model, ignore start
                if is_start is False:
                    model_last = tvl.last_model()
                    if model_last:
                        key_last = model_last.key
                        layer_name_last = _bsc_util.MtgRigNamespace.to_layer_name(rig_namespace, key_last)
                        mtg_layer_last = _layer.MtgLayer(layer_name_last)
                        start_frame, end_frame = frame_range
                        mtg_master_layer.update_root_loc_end_for(
                            mtg_layer_last, start_frame, end_frame
                        )

            tvl.next()

        # update bypass and trash
        for i_tack_model in stage.get_all_models():
            i_key = i_tack_model.key
            i_layer_name = _bsc_util.MtgRigNamespace.to_layer_name(rig_namespace, i_key)
            i_layer_opt = _layer.MtgLayer(i_layer_name)
            i_layer_opt.set('is_bypass', i_tack_model.is_bypass)
            i_layer_opt.set('is_trash', i_tack_model.is_trash)

        # flush maya undo, use montage GUI undo
        qsm_mya_core.Undo.flush()

    @classmethod
    def generate_stage_model_fnc(cls, track_data_list):
        model_stage = bsc_model.TrackModelStage()
        for i_track_data in track_data_list:
            model_stage.create_one(widget=None, **i_track_data)
        return model_stage

    def __init__(self, rig_namespace):
        self._master_layer_location = _layer.MtgMasterLayer.find_one_master_layer_location(rig_namespace)

    def generate_track_data(self):
        list_ = []
        if self._master_layer_location is None:
            return

        mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)
        for i_path in mtg_master_layer.get_all_layer_locations():
            i_track_data = _layer.MtgLayer(i_path).generate_track_kwargs()
            list_.append(i_track_data)
        return list_

    def generate_stage_model(self):
        model_stage = bsc_model.TrackModelStage()
        for i_track_data in self.generate_track_data():
            model_stage.create_one(widget=None, **i_track_data)
        return model_stage

    def look_from_persp_cam(self):
        _layer.MtgMasterLayer(self._master_layer_location).look_from_persp_cam()

    def get_all_layer_locations(self):
        if self._master_layer_location is None:
            return []

        mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)
        return mtg_master_layer.get_all_layer_locations()

    def get_all_layer_names(self):
        if self._master_layer_location is None:
            return []

        mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)
        return mtg_master_layer.get_all_layer_names()

    def get_all_track_keys(self):
        if self._master_layer_location is None:
            return []

        mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)
        layer_names = mtg_master_layer.get_all_layer_names()
        return [x.split(':')[-1] for x in layer_names]

    def export_track_data(self, track_json_path):
        data = self.generate_track_data()

        bsc_storage.StgFileOpt(
            track_json_path
        ).set_write(
            data
        )

    def import_track_json(self, track_json_path):
        track_data_list = bsc_storage.StgFileOpt(track_json_path).set_read()

        mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)
        rig_namespace = mtg_master_layer.get_rig_namespace()

        with bsc_log.LogProcessContext.create(maximum=len(track_data_list)) as l_p:
            for i_track_data in track_data_list:
                mtg_master_layer.create_layer(**i_track_data)

                l_p.do_update()

        stage = self.generate_stage_model_fnc(track_data_list)

        self.update_by_stage(rig_namespace, stage)
        
    def update_track_json(self, track_json_path):
        track_data_list = bsc_storage.StgFileOpt(track_json_path).set_read()

        mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)
        rig_namespace = mtg_master_layer.get_rig_namespace()

        stage = self.generate_stage_model_fnc(track_data_list)

        self.update_by_stage(rig_namespace, stage)
        
    def do_delete(self):
        if self._master_layer_location is not None:
            mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)

            mtg_master_layer.do_delete()

    def do_bake(self):
        if self._master_layer_location is not None:
            mtg_master_layer = _layer.MtgMasterLayer(self._master_layer_location)

            mtg_master_layer.do_bake()
