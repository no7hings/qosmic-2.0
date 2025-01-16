# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ..mocap import resource as _mcp_resource

from ..adv import resource as _adv_resource

from . import resource as _resource


class MocapTransferHandle(object):
    def __init__(self, mocap_namespace):
        self._mocap_namespace = mocap_namespace

    def setup(self):
        _resource.TransferResource.create_sketches()
        self._transfer_resource = _resource.TransferResource(
            _resource.TransferResource.Namespaces.Transfer
        )
        self._mocap_resource = _mcp_resource.MocapResource(namespace=self._mocap_namespace)

    def connect_to_mocap(self):
        self._transfer_resource.connect_from_mocap(self._mocap_resource)

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
            fps=qsm_mya_core.Frame.get_fps(),
            api_version='1.0.1'
        )
        return data

    def bake_sketches_keyframes(self):
        start_frame, end_frame = self._mocap_resource.get_frame_range()
        self._transfer_resource.bake_sketches_keyframes(start_frame, end_frame)

    @classmethod
    def test(cls):
        pass

    def export_mocap_to(self, file_path):
        # bake first
        self.bake_sketches_keyframes()
        #
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
            # bake key frame first
            handle.bake_sketches_keyframes()
            # handle.export_mocap_to(
            #     'Z:/resources/motion_json_new/idle.json'
            # )


class MocapToAdvHandle(object):
    def __init__(self, adv_namespace, mocap_namespace=None, mocap_location=None):
        self._adv_namespace = adv_namespace
        self._mocap_namespace = mocap_namespace
        self._mocap_location = mocap_location

    def setup(self):
        _resource.TransferResource.create_sketches()
        self._transfer_resource = _resource.TransferResource(
            _resource.TransferResource.Namespaces.Transfer
        )

        self._mocap_resource = _mcp_resource.MocapResource(
            namespace=self._mocap_namespace, location=self._mocap_location
        )
        self._adv_resource = _adv_resource.AdvResource(self._adv_namespace)

    def create_mocap_resource_connection(self):
        self._transfer_resource.connect_from_mocap(self._mocap_resource)

    def create_adv_connection(self):
        self._adv_resource.connect_from_transfer_resource(self._transfer_resource)

    def bake_adv_controls_keyframes(self):
        frame_range = self._mocap_resource.get_frame_range()
        self._adv_resource.bake_controls_keyframes(*frame_range)

    def delete_transfer_resource(self):
        self._transfer_resource.do_delete()

    @classmethod
    def test(cls):
        h = cls('sam_Skin', mocap_location='|Hips')
        h.setup()
        h.create_mocap_resource_connection()
        h.create_adv_connection()
        h.bake_adv_controls_keyframes()
        h.delete_transfer_resource()
