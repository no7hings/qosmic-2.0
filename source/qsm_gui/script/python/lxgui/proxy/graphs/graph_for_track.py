# coding:utf-8
import os

import random

import lxbasic.model as bsc_model

import lxbasic.storage as bsc_storage

from ...qt.graph_widgets.track import graph as _graph_for_track
# proxy abstracts
from ...proxy import abstracts as _proxy_abstracts

import lxuniverse.objects as unr_objects


class PrxTrackWidget(
    _proxy_abstracts.AbsPrxWidget
):
    QT_WIDGET_CLS = _graph_for_track.QtTrackWidget

    def __init__(self, *args, **kwargs):
        super(PrxTrackWidget, self).__init__(*args, **kwargs)

        self._universe = unr_objects.ObjUniverse()

        self._track_obj_type = self._universe.create_obj_type('graph', 'track')
        self._type_raw = self._universe.create_type(self._universe.Category.CONSTANT, self._universe.Type.RAW)

        self._qt_widget._graph._set_graph_universe_(self._universe)

    def translate_graph_to(self, x, y):
        self._qt_widget._graph._graph_model.translate_to(x, y)

    def scale_graph_to(self, s_x, s_y):
        self._qt_widget._graph._graph_model.scale_to(s_x, s_y)

    def connect_stage_change_to(self, fnc):
        self._qt_widget._track_guide.stage_changed.connect(fnc)

    def connect_frame_accepted_to(self, fnc):
        self._qt_widget._track_timeline.frame_accepted.connect(fnc)

    def register_track_to_universe(
        self,
        key,
        clip_start, clip_end,
        start, speed, count,
        source_start, source_end,
        pre_cycle, post_cycle,
        scale_start, scale_end,
        pre_blend, post_blend,
        layer_index
    ):
        obj = self._track_obj_type.create_obj('/{}'.format(key))
        obj.create_parameter(self._type_raw, 'key').set(key)
        #
        obj.create_parameter(self._type_raw, 'clip_start').set(clip_start)
        obj.create_parameter(self._type_raw, 'clip_end').set(clip_end)
        #
        obj.create_parameter(self._type_raw, 'start').set(start)
        obj.create_parameter(self._type_raw, 'speed').set(speed)
        obj.create_parameter(self._type_raw, 'count').set(count)
        #
        obj.create_parameter(self._type_raw, 'source_start').set(source_start)
        obj.create_parameter(self._type_raw, 'source_end').set(source_end)
        obj.create_parameter(self._type_raw, 'pre_cycle').set(pre_cycle)
        obj.create_parameter(self._type_raw, 'post_cycle').set(post_cycle)
        # scale
        obj.create_parameter(self._type_raw, 'scale_start').set(scale_start)
        obj.create_parameter(self._type_raw, 'scale_end').set(scale_end)
        # blend
        obj.create_parameter(self._type_raw, 'pre_blend').set(pre_blend)
        obj.create_parameter(self._type_raw, 'post_blend').set(post_blend)
        #
        obj.create_parameter(self._type_raw, 'layer_index').set(layer_index)

    def set_graph_universe(self, universe):
        self._qt_widget._graph._set_graph_universe_(universe)
        
    def setup_graph_by_universe(self):
        self._qt_widget._graph._setup_graph_by_universe_()

    def get_stage_model(self):
        return self._qt_widget._track_guide._track_model_stage

    def get_current(self):
        return self._qt_widget._track_timeline._get_current_timeframe_()

    def set_current_frame(self, frame):
        self._qt_widget._track_timeline._set_current_timeframe_(frame)

    def restore(self):
        self._qt_widget._graph._restore_graph_()

    def create_node(self, *args, **kwargs):
        self._qt_widget._graph._create_node_(*args, **kwargs)

    def create_test(self):
        post_cycles = range(1, 5)

        pre_blends = range(4, 8)
        post_blends = range(4, 8)

        motion_json_ptn = 'Z:/libraries/lazy-resource/all/motion_splice/{name}/json/{name}.motion.json'

        keys = [
            'a_pose',
            'jog_backward',
            'idle_1',
            'slow_run',
            'medium_run',
            'fast_run',
            'jump',
        ]

        random.seed(1)

        clip_start = 1
        for i_index in range(10):
            i_name = random.choice(keys)
            i_post_cycle = random.choice(post_cycles)
            i_pre_blend = random.choice(pre_blends)
            i_post_blend = random.choice(post_blends)

            i_motion_json = motion_json_ptn.format(name=i_name)

            if os.path.exists(i_motion_json) is False:
                raise RuntimeError()

            i_data = bsc_storage.StgFileOpt(i_motion_json).set_read()

            i_source_count = i_data['frame_count']

            i_clip_end = bsc_model.TrackModel.compute_end(
                clip_start, 1, i_source_count-1, i_post_cycle
            )

            self._qt_widget._graph._create_node_(
                key='{}_{}'.format(i_name, i_index),
                clip_start=clip_start, clip_end=i_clip_end,
                start=clip_start, speed=1.0, count=None,
                source_start=1, source_end=i_source_count-1,
                pre_cycle=1, post_cycle=i_post_cycle,
                scale_start=None, scale_end=None, scale_offset=None,
                pre_blend=i_pre_blend, post_blend=i_post_blend,
                layer_index=i_index,
                is_bypass=0, is_trash=0,
                motion_json=i_motion_json,
            )
            clip_start = i_clip_end+1

    def get_all_layer_names(self):
        return self._qt_widget._track_guide._track_model_stage.get_all_layer_names()

    def get_all_track_keys(self):
        return self._qt_widget._track_guide._track_model_stage.get_all_layer_names()
