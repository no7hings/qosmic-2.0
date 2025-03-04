# coding:utf-8
from __future__ import print_function

import os.path

import lxbasic.pinyin as bsc_pinyin

import lxbasic.log as bsc_log

import lxbasic.scan as bsc_scan

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lnx_screw.core as lnx_scr_core


class QuixelAssetRegister(object):

    def __init__(self, scr_stage, file_path):
        assert isinstance(scr_stage, lnx_scr_core.Stage)

        self._scr_stage = scr_stage
        self._file_path = file_path

        self._ignore_exists = True

    def execute(self):
        file_opt = bsc_storage.StgFileOpt(self._file_path)


class QuixelRegisterBatch(object):

    @classmethod
    def get_files_fnc(cls, directory_path, file_pattern, file_formats):
        directory_kwargs = dict(
            directory=directory_path
        )

        file_formats = [str(x).strip() for x in file_formats.split(',')]

        set_ = set()

        for i_format in file_formats:
            i_kwargs = dict(directory_kwargs)
            i_kwargs['format'] = i_format

            i_regex = file_pattern.format(
                **i_kwargs
            )

            i_file_paths = bsc_scan.ScanGlob.glob_files(i_regex)

            if i_file_paths:
                set_.update(set(i_file_paths))

        list_ = list(set_)
        list_.sort()
        return list_

    @classmethod
    def register_fnc(
        cls, database_name, directory_path, scheme
    ):
        json_paths = cls.get_files_fnc(directory_path, file_pattern='{directory}//*.{format}', file_formats='json')

        if json_paths:
            result = gui_core.GuiApplication.exec_message_dialog(
                u'\n'.join(json_paths),
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )
            if result:
                cls(database_name, json_paths, scheme).execute()
        else:
            gui_core.GuiApplication.exec_message_dialog(
                'File is not found.',
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )

    def __init__(
        self,
        database_name, json_paths, scheme
    ):
        self._scr_stage = lnx_scr_core.Stage(database_name)

        self._json_paths = json_paths

        self._scheme = scheme

    def execute(self):
        if self._json_paths:
            with bsc_log.LogProcessContext.create(
                maximum=len(self._json_paths), label='maya scene register batch'
            ) as l_p:
                for i_file_path in self._json_paths:
                    # noinspection PyBroadException
                    try:
                        if self._scheme == 'asset':
                            QuixelAssetRegister(self._scr_stage, i_file_path).execute()
                    except Exception:
                        pass
                    finally:
                        l_p.do_update()
