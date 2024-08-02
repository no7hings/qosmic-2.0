# coding:utf-8
import random

import lxbasic.model as bsc_model

from ...qt.graphs import graph_for_track as _graph_for_track
# proxy abstracts
from ...proxy import abstracts as _proxy_abstracts

import lxuniverse.objects as unr_objects


class PrxTrackView(
    _proxy_abstracts.AbsPrxWidget
):
    QT_WIDGET_CLS = _graph_for_track.QtTrackView

    def __init__(self, *args, **kwargs):
        super(PrxTrackView, self).__init__(*args, **kwargs)

        self._universe = unr_objects.ObjUniverse()

        self._track_obj_type = self._universe.create_obj_type('graph', 'track')
        self._type_raw = self._universe.create_type(self._universe.Category.CONSTANT, self._universe.Type.RAW)

        self._qt_widget._graph._set_graph_universe_(self._universe)

    def translate_graph_to(self, x, y):
        self._qt_widget._graph._translate_graph_to_(x, y)

    def scale_graph_to(self, s_x, s_y):
        self._qt_widget._graph._scale_graph_to_(s_x, s_y)

    def connect_stage_change_to(self, fnc):
        self._qt_widget._track_stage.stage_changed.connect(fnc)

    def connect_frame_accepted_to(self, fnc):
        self._qt_widget._track_timeline.frame_accepted.connect(fnc)

    def register_track_to_universe(
        self,
        key,
        clip_start, clip_end,
        start, speed,
        source_start, source_end,
        pre_cycle, post_cycle,
        layer_index
    ):
        obj = self._track_obj_type.create_obj('/{}'.format(key))
        obj.create_parameter(self._type_raw, 'key').set(key)
        obj.create_parameter(self._type_raw, 'clip_start').set(clip_start)
        obj.create_parameter(self._type_raw, 'clip_end').set(clip_end)
        obj.create_parameter(self._type_raw, 'start').set(start)
        obj.create_parameter(self._type_raw, 'speed').set(speed)
        obj.create_parameter(self._type_raw, 'source_start').set(source_start)
        obj.create_parameter(self._type_raw, 'source_end').set(source_end)
        obj.create_parameter(self._type_raw, 'pre_cycle').set(pre_cycle)
        obj.create_parameter(self._type_raw, 'post_cycle').set(post_cycle)
        obj.create_parameter(self._type_raw, 'layer_index').set(layer_index)

    def set_graph_universe(self, universe):
        self._qt_widget._graph._set_graph_universe_(universe)
        
    def setup_graph_by_universe(self):
        self._qt_widget._graph._setup_graph_by_universe_()

    def get_stage_model(self):
        return self._qt_widget._track_stage._stage_model

    def get_current_frame(self):
        return self._qt_widget._track_timeline._get_current_frame_()

    def create_test(self):
        post_cycles = range(1, 5)

        args = [
            ('sam_walk_macho_forward', 24),
            ('sam_run_turn_left', 24),
            ('sam_walk_forward', 24),
            ('sam_walk_sneak_turn_right', 24),
            ('sam_run_forward', 24),
            ('sam_walk_sneak_forward', 24)
        ]

        random.seed(1)

        clip_start = 1
        for i_index in range(10):
            i_name, i_source_count = random.choice(args)
            i_post_cycle = random.choice(post_cycles)

            i_clip_end = bsc_model.TrackModel.compute_end(
                clip_start, 1, i_source_count-1, i_post_cycle
            )

            self.register_track_to_universe(
                key='{}_{}'.format(i_name, i_index),
                clip_start=clip_start, clip_end=i_clip_end,
                start=clip_start, speed=1.0,
                source_start=1, source_end=i_source_count-1,
                pre_cycle=0, post_cycle=i_post_cycle,
                layer_index=i_index
            )

            clip_start = i_clip_end+1

        self.setup_graph_by_universe()

