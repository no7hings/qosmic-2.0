# coding:utf-8
import tempfile
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
        _resource.TransferResource.create_sketches(_resource.TransferResource.Namespaces.Transfer)
        self._transfer_resource = _resource.TransferResource(
            _resource.TransferResource.Namespaces.Transfer
        )
        self._mocap_resource = _mcp_resource.MocapResource(namespace=self._mocap_namespace)

    def connect_to_mocap(self):
        self._transfer_resource.connect_from_mocap(self._mocap_resource)

    @classmethod
    def test(cls):
        pass

    def export_motion_to(self, motion_json_file):
        start_frame, end_frame = self._mocap_resource.get_frame_range()
        self._transfer_resource.export_motion_to(
            start_frame, end_frame, motion_json_file
        )

    @classmethod
    def mocap_test(cls):
        namespaces = _resource.TransferResource.find_mocap_namespaces()
        if namespaces:
            handle = cls(namespaces[0])
            handle.setup()
            handle.connect_to_mocap()
            # bake key frame first
            motion_json_file = tempfile.mktemp(suffix='.motion.json')
            handle.export_motion_to(motion_json_file)
            print motion_json_file


class MocapToAdvHandle(object):
    def __init__(self, adv_namespace, mocap_namespace=None, mocap_location=None):
        self._adv_namespace = adv_namespace
        self._mocap_namespace = mocap_namespace

        self._transfer_namespace = '{}_transfer'.format(self._adv_namespace)
        self._mocap_location = mocap_location

    def setup(self):
        _resource.TransferResource.create_sketches(self._transfer_namespace)
        self._transfer_resource = _resource.TransferResource(self._transfer_namespace)

        self._mocap_resource = _mcp_resource.MocapResource(
            namespace=self._mocap_namespace, location=self._mocap_location
        )
        self._adv_resource = _adv_resource.AdvResource(self._adv_namespace)

    def create_mocap_resource_connection(self):
        self._transfer_resource.connect_from_mocap(self._mocap_resource)

    def bake_transfer_resource_sketches_keyframes(self):
        start_frame, end_frame = self._mocap_resource.get_frame_range()
        self._transfer_resource.bake_sketches_keyframes(start_frame, end_frame)

    def create_adv_resource_connection(self):
        self._adv_resource.connect_from_transfer_resource(self._transfer_resource)

    def bake_adv_controls_keyframes(self):
        frame_range = self._mocap_resource.get_frame_range()
        self._adv_resource.bake_controls_keyframes(*frame_range)

    def delete_transfer_resource(self):
        self._transfer_resource.do_delete()

    def execute(self):
        self.setup()

        self.create_mocap_resource_connection()
        self.create_adv_resource_connection()

        self.bake_adv_controls_keyframes()
        self.delete_transfer_resource()

    @classmethod
    def mocap_test(cls):
        self = cls('sam_Skin', mocap_location='mixamorig:Hips')
        self.setup()

        self.create_mocap_resource_connection()
        self.create_adv_resource_connection()

        self.bake_adv_controls_keyframes()
        self.delete_transfer_resource()
