# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

from ...screw import core as _scr_core


class AudioRegister(object):
    def __init__(self, scr_stage, file_path):
        assert isinstance(scr_stage, _scr_core.Stage)
        self._scr_stage = scr_stage
        self._file_path = file_path

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        file_opt = bsc_storage.StgFileOpt(self._file_path)
        uuid = file_opt.to_hash_uuid()
        scr_node_path = '/{}'.format(uuid)

        if self._scr_stage.check_node_exists(scr_node_path) is False:
            self._scr_stage.create_node(
                scr_node_path,
                ctime=file_opt.get_ctime(),
                mtime=file_opt.get_mtime(),
                user=bsc_core.BscSystem.get_user_name(),
                gui_name=file_opt.name,
                gui_name_chs=file_opt.name,
            )

            if scr_type_paths:
                [self._scr_stage.create_node_type_assign(scr_node_path, x) for x in scr_type_paths]

            if scr_tag_paths:
                [self._scr_stage.create_node_tag_assign(scr_node_path, x) for x in scr_tag_paths]

            self._scr_stage.upload_node_audio(
                scr_node_path, self._file_path
            )


class AudioBatchRegister(object):
    def __init__(self, scr_stage_key, file_paths):
        self._scr_stage = _scr_core.Stage(scr_stage_key)
        self._file_paths = file_paths

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        with bsc_log.LogProcessContext.create(maximum=len(self._file_paths)) as l_p:
            for i_file_path in self._file_paths:
                AudioRegister(self._scr_stage, i_file_path).execute(scr_type_paths, scr_tag_paths)

                l_p.do_update()
