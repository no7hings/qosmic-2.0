# coding:utf-8
from __future__ import print_function

import os.path

import lxbasic.pinyin as bsc_pinyin

import lxbasic.log as bsc_log

import lxbasic.scan as bsc_scan

import lxbasic.storage as bsc_storage

import lnx_screw.core as lnx_scr_core


class FbxCacheRegister(object):
    def __init__(
        self,
        scr_stage, file_path,
        with_preview=True, preview_pattern='{file_directory}/{file_name}.png',
        with_file_reference=True, file_reference_pattern='{file_directory}//*'
    ):
        assert isinstance(scr_stage, lnx_scr_core.Stage)

        self._scr_stage = scr_stage
        self._file_path = file_path

        self._with_preview = with_preview
        self._preview_pattern = preview_pattern

        self._with_file_reference = with_file_reference
        self._file_reference_pattern = file_reference_pattern

        self._ignore_exists = True

    def execute(self):
        file_opt = bsc_storage.StgFileOpt(self._file_path)

        file_kwargs = dict(
            file_directory=file_opt.directory_path,
            file_name=file_opt.name_base
        )

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
        source_dir_path = self._scr_stage.generate_node_source_dir_path(scr_node_path)
        file_path_tgt = file_opt.copy_to_directory(source_dir_path)
        self._scr_stage.create_or_update_node_parameter(scr_node_path, 'source', file_path_tgt)

        # preview
        if self._with_preview is True:
            preview_path = self._preview_pattern.format(**file_kwargs)
            if bsc_storage.StgPath.get_is_exists(preview_path):
                self._scr_stage.upload_node_preview(scr_node_path, preview_path)

        # file reference
        if self._with_file_reference is True:
            file_reference_ptn = self._file_reference_pattern.format(**file_kwargs)

            directory_root_path = os.path.dirname(file_reference_ptn)
            all_files = bsc_scan.ScanGlob.glob_files(file_reference_ptn)
            for i_file_path in all_files:
                i_file_name_tgt = i_file_path[len(directory_root_path)+1:]
                i_file_path_tgt = u'{}/{}'.format(source_dir_path, i_file_name_tgt)
                i_file_opt = bsc_storage.StgFileOpt(i_file_path)
                i_file_opt.copy_to_file(i_file_path_tgt)


class FbxCacheRegisterBatch(object):
    def __init__(
        self,
        database_name, file_paths,
        with_preview=True, preview_pattern='{file_directory}/{file_name}.png',
        with_file_reference=True, file_reference_pattern='{file_directory}//*'
    ):
        self._scr_stage = lnx_scr_core.Stage(database_name)

        self._file_paths = file_paths

        self._with_preview = with_preview
        self._preview_pattern = preview_pattern

        self._with_file_reference = with_file_reference
        self._file_reference_pattern = file_reference_pattern

    def execute(self):
        if self._file_paths:
            with bsc_log.LogProcessContext.create(
                maximum=len(self._file_paths), label='maya scene register batch'
            ) as l_p:
                for i_file_path in self._file_paths:
                    # noinspection PyBroadException
                    try:
                        FbxCacheRegister(
                            self._scr_stage,
                            i_file_path,
                            with_preview=self._with_preview,
                            preview_pattern=self._preview_pattern,
                            with_file_reference=self._with_file_reference,
                            file_reference_pattern=self._file_reference_pattern
                        ).execute()
                    except Exception:
                        pass
                    finally:
                        l_p.do_update()
