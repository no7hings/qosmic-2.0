# coding:utf-8
from __future__ import print_function

import os.path

import lxbasic.pinyin as bsc_pinyin

import lxbasic.log as bsc_log

import lxbasic.scan as bsc_scan

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lnx_screw.core as lnx_scr_core


class AnySceneRegister(object):
    @classmethod
    def get_preview_fnc(cls, file_kwargs, preview_pattern, preview_formats):
        preview_formats = [str(x).strip() for x in preview_formats.split(',')]

        for i_format in preview_formats:
            i_kwargs = dict(file_kwargs)
            i_kwargs['format'] = i_format
            i_regex = preview_pattern.format(**i_kwargs)
            i_file_paths = bsc_scan.ScanGlob.glob_files(i_regex)

            if i_file_paths:
                return i_file_paths[0]

    def __init__(
        self,
        scr_stage, file_path,
        with_preview, preview_pattern, preview_formats,
        with_file_reference, file_reference_pattern
    ):
        assert isinstance(scr_stage, lnx_scr_core.Stage)

        self._scr_stage = scr_stage
        self._file_path = file_path

        self._with_preview = with_preview
        self._preview_pattern = preview_pattern
        self._preview_formats = preview_formats

        self._with_file_reference = with_file_reference
        self._file_reference_pattern = file_reference_pattern

        self._ignore_exists = True

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        file_opt = bsc_storage.StgFileOpt(self._file_path)

        file_kwargs = dict(
            file_directory=file_opt.directory_path,
            file_name=file_opt.name_base,
            file_format=file_opt.format,
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
            preview_path = self.get_preview_fnc(file_kwargs, self._preview_pattern, self._preview_formats)
            if preview_path:
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

        # type and tag
        if scr_type_paths:
            [self._scr_stage.create_node_type_assign(scr_node_path, x) for x in scr_type_paths]

        if scr_tag_paths:
            [self._scr_stage.create_node_tag_assign(scr_node_path, x) for x in scr_tag_paths]


class AnySceneRegisterBatch(object):

    @classmethod
    def get_files_fnc(cls, directory_path, file_pattern, file_formats):
        directory_kwargs = dict(
            directory=directory_path
        )

        file_formats = [str(x).strip() for x in file_formats.split(',')]

        list_ = []

        for i_format in file_formats:
            i_kwargs = dict(directory_kwargs)
            i_kwargs['format'] = i_format

            i_regex = file_pattern.format(
                **i_kwargs
            )

            i_file_paths = bsc_scan.ScanGlob.glob_files(i_regex)

            if i_file_paths:
                list_.extend(i_file_paths)

        return list_

    @classmethod
    def register_fnc(
        cls,
        database_name, directory_path,
        file_pattern='{directory}//*.{format}', file_formats='ma, mb',
        with_preview=True, preview_pattern='{file_directory}/{file_name}.{format}', preview_formats='png, jpg',
        with_file_reference=False, file_reference_pattern='{file_directory}//*',
        scr_type_paths=None, scr_tag_paths=None
    ):
        file_paths = cls.get_files_fnc(directory_path, file_pattern, file_formats)

        if file_paths:
            result = gui_core.GuiApplication.exec_message_dialog(
                u'\n'.join(file_paths),
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )
            if result:
                cls(
                    database_name, file_paths,
                    with_preview=with_preview, preview_pattern=preview_pattern, preview_formats=preview_formats,
                    with_file_reference=with_file_reference, file_reference_pattern=file_reference_pattern,
                ).execute(
                    scr_type_paths, scr_tag_paths
                )
        else:
            gui_core.GuiApplication.exec_message_dialog(
                'File is not found.',
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )

    def __init__(
        self,
        database_name, file_paths,
        with_preview, preview_pattern, preview_formats,
        with_file_reference, file_reference_pattern
    ):
        self._scr_stage = lnx_scr_core.Stage(database_name)

        self._file_paths = file_paths

        self._with_preview = with_preview
        self._preview_pattern = preview_pattern
        self._preview_formats = preview_formats

        self._with_file_reference = with_file_reference
        self._file_reference_pattern = file_reference_pattern

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        if self._file_paths:
            with bsc_log.LogProcessContext.create(
                maximum=len(self._file_paths), label='maya scene register batch'
            ) as l_p:
                for i_file_path in self._file_paths:
                    # noinspection PyBroadException
                    try:
                        AnySceneRegister(
                            self._scr_stage,
                            i_file_path,
                            with_preview=self._with_preview,
                            preview_pattern=self._preview_pattern,
                            preview_formats=self._preview_formats,
                            with_file_reference=self._with_file_reference,
                            file_reference_pattern=self._file_reference_pattern
                        ).execute(
                            scr_type_paths, scr_tag_paths
                        )
                    except Exception:
                        pass
                    finally:
                        l_p.do_update()
