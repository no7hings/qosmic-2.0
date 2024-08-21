# coding:utf-8
from qsm_lazy_tool.montage.gui import abstracts as _gui_abstracts

import qsm_maya.core as qsm_mya_core

import qsm_maya.animation.core as qsm_mya_anm_core

import qsm_maya_lazy.montage.core as qsm_mya_lzy_mtg_core

import qsm_maya_lazy.montage.scripts as qsm_mya_lzy_mtg_scripts


class PrxPageForSplicing(_gui_abstracts.AbsPrxPageForSplicing):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForSplicing, self).__init__(window, session, *args, **kwargs)

    def gui_refresh_stage(self, force=False):
        if force is True:
            self._motion_prx_track_view.restore()

        data = qsm_mya_lzy_mtg_core.AdvMotionStage().generate_track_data()
        if data:
            for i_kwargs in data:
                self._motion_prx_track_view.create_node(**i_kwargs)
            #     self._motion_prx_track_view.register_track_to_universe(
            #         **i_kwargs
            #     )
            # self._motion_prx_track_view.setup_graph_by_universe()

    def get_dcc_character_args(self):
        results = []

        master_layer = qsm_mya_lzy_mtg_scripts.AdvChrMotionImportOpt.find_master_layer()
        if master_layer:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.exists_master_layer'.format(self.PAGE_KEY))
                ),
                status='warning'
            )
            return

        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        if namespaces:
            results = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_character'.format(self.PAGE_KEY))
                ),
                status='warning'
            )
            return
        return results

    def _create_master_layer(self):
        results = self.get_dcc_character_args()
        if results:
            qsm_mya_lzy_mtg_scripts.AdvChrMotionImportOpt.setup_for(results[0])

    def do_dcc_motion_update(self):
        stage = self._motion_prx_track_view.get_stage_model()
        start_frame, end_frame = stage.track_start, stage.track_end
        current_frame = self._motion_prx_track_view.get_current_frame()

        qsm_mya_core.Frame.update_frame(start_frame, end_frame, current_frame)

        tvl = stage.generate_valid_frame_range_travel()

        while tvl.is_valid():
            frame_range, track_model = tvl.current_data()

            is_start, is_end = tvl.is_start(), tvl.is_end()

            if track_model is not None:
                frame_range_index = track_model.get_frame_range_index(frame_range)
                key = track_model.key
                location = '|{}:LAYER'.format(key)
                layer_opt = qsm_mya_lzy_mtg_core.AdvChrMotionLayer(location)
                #
                layer_opt.set('clip_start', track_model.clip_start)
                layer_opt.set('clip_end', track_model.clip_end)
                #
                layer_opt.set('start', track_model.start)
                layer_opt.set('speed', track_model.speed)
                layer_opt.set('count', track_model.count)
                #
                layer_opt.set('source_start', track_model.source_start)
                layer_opt.set('source_end', track_model.source_end)
                layer_opt.set('pre_cycle', track_model.pre_cycle)
                layer_opt.set('post_cycle', track_model.post_cycle)
                #
                layer_opt.set('scale_start', track_model.scale_start)
                layer_opt.set('scale_end', track_model.scale_end)
                #
                layer_opt.set('pre_blend', track_model.pre_blend)
                layer_opt.set('post_blend', track_model.post_blend)
                #
                layer_opt.set('valid_start', track_model.get_valid_start())
                layer_opt.set('valid_end', track_model.get_valid_end())
                layer_opt.set('output_end', frame_range[-1])

                if frame_range_index == 0:
                    layer_opt.clear_main_weight_keys()

                if tvl.next_is_valid() is False:
                    data_next = tvl.next_data()
                    if data_next is not None:
                        frame_range_next, track_model_next = data_next
                        frame_range = (frame_range[0], frame_range_next[-1])

                layer_opt.update_main_weight(frame_range, is_start, is_end)

                data_last = tvl.last_data()
                if data_last:
                    frame_range_last, track_model_last = data_last
                    if track_model_last is not None:
                        key_last = track_model_last.key
                        location_last = '|{}:LAYER'.format(key_last)
                        layer_opt_last = qsm_mya_lzy_mtg_core.AdvChrMotionLayer(location_last)
                        layer_opt.update_root_start_opt(layer_opt, layer_opt_last, frame_range[0])
                else:
                    layer_opt.update_root_start_self(layer_opt)

            tvl.next()

    def do_dcc_update_current_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)
