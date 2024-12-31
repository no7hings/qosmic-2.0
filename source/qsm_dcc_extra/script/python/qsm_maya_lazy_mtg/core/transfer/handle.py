# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ..mocap import resource as _mcp_resource

from . import resource as _resource


class MocapTransferHandle(object):
    def __init__(self, mocap_namespace):
        self._mocap_namespace = mocap_namespace

    def setup(self):
        _resource.TransferResource.create_sketches()
        self._transfer_resource = _resource.TransferResource(
            _resource.TransferResource.Namespaces.Transfer
        )
        self._mocap_resource = _mcp_resource.MocapResource(self._mocap_namespace)

    def match_height_to_mocap(self):
        height_0 = self._mocap_resource.get_root_height()
        height_1 = self._transfer_resource.get_root_height()

        scale = height_0/height_1

        root_location = self._transfer_resource.find_root_location()

        cmds.setAttr(
            root_location+'.scale', scale, scale, scale
        )

    def connect_to_mocap(self):
        self.match_height_to_mocap()
        self._mocap_resource.sketch_set.connect_to_master_sketch(
            self._transfer_resource._sketch_set
        )

    def get_data_from_mocap(self):
        start_frame, end_frame = self._mocap_resource.sketch_set.get_frame_range()
        data = self._transfer_resource._sketch_set.get_data(start_frame, end_frame)
        data['root_height'] = self._transfer_resource.get_root_height()
        data['metadata'] = dict(
            ctime=bsc_core.BscSystem.generate_timestamp(),
            user=bsc_core.BscSystem.get_user_name(),
            host=bsc_core.BscSystem.get_host(),
            start_frame=start_frame,
            end_frame=end_frame,
            fps=qsm_mya_core.Frame.get_fps()
        )
        return data

    def export_mocap_to(self, file_path):
        bsc_storage.StgFileOpt(file_path).set_write(
            self.get_data_from_mocap()
        )

    @classmethod
    def mocap_test(cls):
        namespaces = _resource.TransferResource.find_mocap_namespaces()
        if namespaces:
            handle = cls(namespaces[0])
            handle.setup()
            handle.connect_to_mocap()
            handle.export_mocap_to(
                'Z:/resources/motion_json/mixamo/a_pose.json'
            )
