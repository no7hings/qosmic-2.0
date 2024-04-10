# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from .. import objects as bsc_dcc_objects


class ScpDccTextures(object):
    def __init__(self, texture_references, includes=None, force=False):
        self._exts = []
        self._texture_references = texture_references
        if isinstance(includes, (tuple, list)):
            self._objs = includes
        else:
            self._objs = self._texture_references.get_objs()
        #
        self._force = force

    def _repath_by_queue(self, queue, force=False):
        bsc_log.Log.trace_method_result(
            'texture repath',
            'start'
        )
        if queue:
            with bsc_log.LogProcessContext.create(maximum=len(queue), label='texture repath') as g_p:
                for i_port, i_args in queue:
                    g_p.do_update()
                    #
                    if isinstance(i_args, (tuple, list)):
                        check_file_obj, tgt_stg_file = i_args
                    else:
                        check_file_obj = tgt_stg_file = i_args
                    #
                    if check_file_obj.get_exists_units() or force is True:
                        self._repath_fnc(i_port, tgt_stg_file)
                        color_space_input = tgt_stg_file.get_tx_color_space_input()
                        if tgt_stg_file.get_exists_units() is True:
                            i_port.obj.set_color_space(color_space_input)
                    else:
                        bsc_log.Log.trace_method_warning(
                            'texture repath',
                            u'file="{}" is non-exists'.format(tgt_stg_file.path)
                        )

            g_p.set_stop()

            self._repath_post_fnc()

        bsc_log.Log.trace_method_result(
            'texture repath',
            'complete'
        )

    @bsc_core.MdfBaseMtd.run_as_ignore
    def _repath_post_fnc(self):
        if bsc_core.SysApplicationMtd.get_is_maya():
            import lxmaya.scripts as mya_scripts

            mya_scripts.ScpTexture._repair_texture_tiles()

    def _repath_fnc(self, port, stg_texture):
        self._texture_references._set_real_file_value(
            port,
            stg_texture.path
        )
        bsc_log.Log.trace_method_result(
            'texture repath',
            'attribute="{}", file="{}"'.format(port.path, stg_texture.path)
        )

    def auto_search_from(self, directory_paths_tgt, below_enable=False):
        dcc_objs = self._objs

        repath_queue = []

        search_opt = bsc_storage.StgFileSearchOpt(
            ignore_name_case=True,
            ignore_ext_case=True,
            ignore_ext=True
        )
        search_opt.set_search_directories(directory_paths_tgt, below_enable=below_enable)
        if dcc_objs:
            g_p = bsc_log.LogProcessContext(
                maximum=len(dcc_objs)
            )
            for i_dcc_obj in dcc_objs:
                g_p.do_update()
                for j_port_path, j_texture_path_tgt in i_dcc_obj.reference_raw.items():
                    j_texture_src = bsc_dcc_objects.StgTexture(j_texture_path_tgt)
                    j_result = search_opt.get_result(j_texture_src.path)
                    if j_result:
                        j_port = i_dcc_obj.get_port(j_port_path)
                        tgt_texture_tgt = bsc_dcc_objects.StgTexture(j_result)
                        #
                        repath_queue.append(
                            (j_port, tgt_texture_tgt)
                        )
                        bsc_log.Log.trace_method_result(
                            'file-search',
                            'file="{}" >> "{}"'.format(j_texture_src.path, tgt_texture_tgt.path)
                        )
                    else:
                        bsc_log.Log.trace_method_warning(
                            'file-search',
                            'file="{}" target is not found'.format(j_texture_src.path)
                        )

            #
            g_p.set_stop()

            self._repath_by_queue(repath_queue)

    def auto_switch_color_space(self):
        dcc_nodes = self._texture_references.get_objs()
        if dcc_nodes:
            with bsc_log.LogProcessContext.create(maximum=len(dcc_nodes), label='switch color-space auto') as g_p:
                for i_dcc_node in dcc_nodes:
                    g_p.do_update()
                    i_stg_files = i_dcc_node.get_stg_files()
                    if i_stg_files:
                        for j_stg_file in i_stg_files:
                            if j_stg_file.get_is_exists() is True:
                                j_color_space_input = j_stg_file.get_tx_color_space_input()
                                i_dcc_node.set_color_space(j_color_space_input)

    def auto_repath_tx_to_original(self):
        objs = self._objs
        #
        repath_queue = []
        #
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    j_port = i_obj.get_port(j_port_path)
                    stg_texture = bsc_dcc_objects.StgTexture(j_file_path)
                    if stg_texture.get_ext_is_tx():
                        o = stg_texture.get_tx_orig()
                        if o is not None:
                            repath_queue.append(
                                (j_port, o)
                            )
        #
        self._repath_by_queue(repath_queue)

    def auto_repath_ext_tgt_to_original(self, ext_tgt):
        objs = self._objs
        #
        repath_queue = []
        #
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    j_port = i_obj.get_port(j_port_path)
                    i_texture = bsc_dcc_objects.StgTexture(j_file_path)
                    if i_texture.get_ext_is(ext_tgt):
                        o = i_texture.get_orig_as_tgt_ext(ext_tgt)
                        if o is not None:
                            repath_queue.append(
                                (j_port, o)
                            )
        #
        self._repath_by_queue(repath_queue)

    def auto_repath_to_current_platform(self, target_platform=None):
        objs = self._objs
        #
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    stg_texture = bsc_dcc_objects.StgTexture(j_file_path)
                    if target_platform is None:
                        tgt_stg_texture_path = bsc_storage.StgPathMapper.map_to_current(stg_texture.path)
                    elif target_platform == 'windows':
                        tgt_stg_texture_path = bsc_storage.StgPathMapper.map_to_windows(stg_texture.path)
                    elif target_platform == 'linux':
                        tgt_stg_texture_path = bsc_storage.StgPathMapper.map_to_linux(stg_texture.path)
                    else:
                        raise TypeError()
                    #
                    tgt_stg_texture = bsc_dcc_objects.StgTexture(tgt_stg_texture_path)
                    j_port = i_obj.get_port(j_port_path)
                    #
                    self._repath_fnc(j_port, tgt_stg_texture)
