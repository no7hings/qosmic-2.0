# coding:utf-8
import os.path

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import qsm_maya.core as qsm_mya_core

from ..core import base as _cor_base

from ..mixamo import resource as _mxm_resource

from . import sketch as _sketch


class MasterResource(_cor_base.MotionBase):
    def __init__(self, namespace):
        self._namespace = namespace

        self._sketch_set = _sketch.MasterSketchSet.generate(self._namespace)

    @classmethod
    def create_sketches(cls):
        _sketch.MasterSketchSet.create(
            cls.Namespaces.Master
        )

    def get_root_height(self):
        # is a constant value now
        return 8.48399903945

    def match_height_to_mixamo(self):
        mixamo_resource = _mxm_resource.MixamoResource(self.Namespaces.Mixamo)
        height_0 = mixamo_resource.get_root_height()
        height_1 = self.get_root_height()

        scale = height_0/height_1

        root = self._sketch_set.find_root(self._namespace)

        cmds.setAttr(
            root+'.scale', scale, scale, scale
        )

    def connect_to_mixamo(self):
        # match mixamo first
        self.match_height_to_mixamo()

        mixamo_resource = _mxm_resource.MixamoResource(self.Namespaces.Mixamo)
        mixamo_resource.sketch_set.connect_to_master(self._sketch_set)

    def get_data(self):
        mixamo_resource = _mxm_resource.MixamoResource(self.Namespaces.Mixamo)
        start_frame, end_frame = mixamo_resource.sketch_set.get_frame_range()
        data = self._sketch_set.get_data(start_frame, end_frame)
        data['root_height'] = self.get_root_height()
        data['metadata'] = dict(
            ctime=bsc_core.BscSystem.generate_timestamp(),
            user=bsc_core.BscSystem.get_user_name(),
            host=bsc_core.BscSystem.get_host(),
            start_frame=start_frame,
            end_frame=end_frame,
            fps=qsm_mya_core.Frame.get_fps()
        )
        return data

    def export_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.get_data()
        )

    @classmethod
    def create_from_mixamo_fbx(cls, fbx_path, motion_path):
        qsm_mya_core.SceneFile.new()
        qsm_mya_core.SceneFile.import_fbx(
            fbx_path
        )
        cls.create_sketches()

        master_resource = cls(cls.Namespaces.Master)
        master_resource.connect_to_mixamo()

        master_resource.export_to(motion_path)

    @classmethod
    def batch_create_from_mixamo_fbx(cls, directory_path_src, directory_path_tgt, force=False):
        file_paths = bsc_storage.StgDirectory.get_file_paths(
            directory_path_src, ext_includes=['.fbx']
        )
        for i_fbx_path in file_paths:
            i_keys = bsc_pinyin.Text.split_any_to_words_extra(bsc_storage.StgFile.get_name_base(i_fbx_path))
            i_name = '_'.join(i_keys).lower()
            i_motion_path = '{}/{}.json'.format(directory_path_tgt, i_name)

            if os.path.isfile(i_motion_path) is True and force is False:
                continue

            cls.create_from_mixamo_fbx(
                i_fbx_path, i_motion_path
            )

    @classmethod
    def test(cls):
        cls.batch_create_from_mixamo_fbx(
            'Z:/resources/mixamo',
            'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/mixamo'
        )
        # cls.create_from_mixamo_fbx(
        #     'C:/Users/nothings/Downloads/Jog In Circle.fbx',
        #     'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/mixamo/jog_in_circle.json'
        # )

    @classmethod
    def test_1(cls):
        master_resource = cls(cls.Namespaces.Master)
        print master_resource.get_data()
