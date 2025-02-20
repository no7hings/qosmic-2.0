# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

import lxbasic.storage as bsc_storage

import lnx_screw.core as lnx_scr_core


class AudioRegister(object):
    def __init__(self, scr_stage, file_path, collect_source=False):
        assert isinstance(scr_stage, lnx_scr_core.Stage)

        self._scr_stage = scr_stage
        self._file_path = file_path

        self._ignore_exists = True

        self._collect_source = collect_source

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        file_opt = bsc_storage.StgFileOpt(self._file_path)

        uuid = file_opt.to_hash_uuid()

        exist_node = self._scr_stage.find_one(
            entity_type=self._scr_stage.EntityTypes.Node,
            filters=[
                ('uuid', 'is', uuid)
            ]
        )
        if exist_node:
            if self._ignore_exists is True:
                return

            scr_node_path = exist_node.path
        else:
            file_name = file_opt.name

            user = file_opt.get_user()
            ctime = file_opt.get_ctime()
            mtime = file_opt.get_mtime()

            dcc_name = bsc_pinyin.Text.to_dcc_name(file_name)
            index_maximum = self._scr_stage.get_entity_index_maximum(self._scr_stage.EntityTypes.Node)
            scr_node_path = '/{}_{}'.format(dcc_name, index_maximum+1)

            scr_node_path_old = '/{}'.format(uuid)
            if self._scr_stage.node_is_exists(scr_node_path_old) is True:
                return

            self._scr_stage.create_node(
                scr_node_path,
                gui_name=file_name,
                gui_name_chs=file_name,
                user=user,
                ctime=float(ctime),
                mtime=float(mtime),
                uuid=uuid
            )

        # source
        self._scr_stage.upload_node_audio(
            scr_node_path, self._file_path, self._collect_source
        )

        # type and tag
        if scr_type_paths:
            [self._scr_stage.create_node_type_assign(scr_node_path, x) for x in scr_type_paths]

        if scr_tag_paths:
            [self._scr_stage.create_node_tag_assign(scr_node_path, x) for x in scr_tag_paths]


class AudioRegisterBatch(object):
    def __init__(self, scr_stage_name, file_paths, collect_source=False):
        self._scr_stage = lnx_scr_core.Stage(scr_stage_name)
        self._file_paths = file_paths
        
        self._collect_source = collect_source

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        with bsc_log.LogProcessContext.create(maximum=len(self._file_paths)) as l_p:
            for i_file_path in self._file_paths:
                AudioRegister(
                    self._scr_stage, i_file_path, self._collect_source
                ).execute(scr_type_paths, scr_tag_paths)

                l_p.do_update()
