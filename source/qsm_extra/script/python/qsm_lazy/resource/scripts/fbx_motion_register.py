# coding:utf-8
import os

import six

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.content as bsc_content

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import qsm_general.core as qsm_gnl_core

import qsm_screw.core as qsm_scr_core


class FbxMotionRegister(object):
    LOG_KEY = 'motion fbx register'

    TYPE_PATH_MAP = {
        '/characters/basics/idle': ['idle'],
        '/characters/basics/walking': ['walk', 'walking'],
        '/characters/basics/jogging': ['jog', 'jogging'],
        '/characters/basics/running': ['run', 'running'],
        '/characters/basics/jumping': ['jump', 'jumping'],
        '/characters/basics/crouching': ['crouch', 'crouching'],
        '/characters/basics/turning': ['turn', 'turning'],
        '/characters/basics/flipping': ['flip', 'flipping'],
        '/characters/basics/rolling': ['roll', 'rolling'],
        '/characters/basics/spinning': ['spin', 'spinning'],
        '/characters/basics/strafing': ['strafe', 'strafing'],
        '/characters/basics/standing_up': ['stand', 'standing'],
        '/characters/basics/dying': ['die', 'dying'],
        '/characters/basics/laying': ['lay', 'laying'],
        '/characters/basics/pose': ['pose'],

        '/characters/dances/capoeira': ['capoeira'],
        '/characters/dances/samba': ['samba'],
        '/characters/dances/northern_soul': ['northern', 'soul']
    }

    def __init__(self, scr_stage, dir_path, fbx_path, source):
        self._scr_stage = scr_stage
        assert isinstance(self._scr_stage, qsm_scr_core.Stage)
        self._dir_path = dir_path
        self._fbx_path = fbx_path
        self._source = source

        self._type_path_map = {i: k for k, v in self.TYPE_PATH_MAP.items() for i in v}

    def execute(self):
        file_opt = bsc_storage.StgFileOpt(self._fbx_path)

        key_str = self._fbx_path[len(self._dir_path):]
        key_str = os.path.splitext(key_str)[0]

        keys = [x.lower() for x in bsc_pinyin.Text.split_any_to_words_extra(key_str)]

        node_name = '_'.join(keys)
        node_path = '/{}'.format(node_name)
        if self._scr_stage.node_is_exists(node_path) is True:
            return

        gui_name = file_opt.name_base

        user = file_opt.get_user()
        ctime = file_opt.get_ctime()

        source_dir_path = self._scr_stage.generate_node_source_dir_path(node_path)

        # create node
        self._scr_stage.create_node(
            node_path, gui_name=gui_name, gui_name_chs=gui_name, user=user, ctime=float(ctime)
        )

        # assign type
        for i in keys:
            if i in self._type_path_map:
                i_type_path = self._type_path_map[i]
                self._scr_stage.create_node_type_assign(
                    node_path, i_type_path
                )

        # assign tag
        motion_json_path = self._scr_stage.generate_node_motion_json_path(node_path, 'motion')
        if bsc_storage.StgPath.get_is_file(motion_json_path) is False:
            self._scr_stage.create_node_tag_assign(
                node_path, '/mark/unprocessed'
            )

        self._scr_stage.create_node_tag_assign(
            node_path, '/source/{}'.format(self._source)
        )

        file_path_tgt = file_opt.copy_to_directory(source_dir_path)

        self._scr_stage.create_or_update_parameters(
            node_path, 'fbx_source', file_path_tgt
        )

        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'successful for: {}'.format(self._fbx_path)
        )


class FbxMotionRegisterBatch(object):
    def __init__(self, directory_path, source='mixamo'):
        self._directory_path = directory_path
        self._source = source

        self._scr_stage = qsm_scr_core.Stage('motion_splice')

    def execute(self):
        fbx_paths = bsc_storage.StgDirectoryOpt(self._directory_path).get_all_file_paths(ext_includes=['.fbx'])

        for i_fbx_path in fbx_paths:
            FbxMotionRegister(self._scr_stage, self._directory_path, i_fbx_path, self._source).execute()
