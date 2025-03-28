# coding:utf-8
import tempfile
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from ..mocap import resource as _mcp_resource

from ..adv import resource as _adv_resource

from . import resource as _resource


class MocapTransferHandle(object):

    @classmethod
    def test(cls):
        pass

    def __init__(self, mocap_namespace=None, mocap_location=None):
        self._mocap_namespace = mocap_namespace
        self._mocap_location = mocap_location

        self._transfer_namespace = '{}_transfer'.format(self._mocap_namespace)

    def setup(self):
        _resource.TransferResource.create_sketches(self._transfer_namespace)
        self._transfer_resource = _resource.TransferResource(
            self._transfer_namespace
        )
        self._mocap_resource = _mcp_resource.MocapResource(
            namespace=self._mocap_namespace, location=self._mocap_location
        )

    def connect(self):
        self._transfer_resource.connect_from_mocap(self._mocap_resource)

    def export_motion_to(self, json_path, frame_range=None):
        if frame_range is not None:
            start_frame, end_frame = frame_range
        else:
            start_frame, end_frame = self._mocap_resource.get_frame_range()

        self._transfer_resource.export_motion_to(
            start_frame, end_frame, json_path
        )


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

    @qsm_mya_core.Undo.execute
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


class AdvTransferHandle(object):
    @classmethod
    def test(cls):
        h = cls('sam_Skin')
        h.setup()
        h.connect()
        # h.export_motion_to(
        #     'Z:/temporaries/premiere_xml_test/motion/test.jsz', qsm_mya_core.Frame.get_frame_range()
        # )

    def __init__(self, adv_namespace):
        self._adv_namespace = adv_namespace
        self._transfer_namespace = '{}_transfer'.format(self._adv_namespace)

    def setup(self):
        _resource.TransferResource.create_sketches(self._transfer_namespace)
        self._transfer_resource = _resource.TransferResource(
            self._transfer_namespace
        )
        self._adv_resource = _adv_resource.AdvResource(
            self._adv_namespace
        )

    def connect(self):
        self._transfer_resource.connect_from_adv(self._adv_resource)

    def export_motion_to(self, json_path, frame_range=None):
        if frame_range is not None:
            start_frame, end_frame = frame_range
        else:
            start_frame, end_frame = self._adv_resource.get_frame_range()

        self._transfer_resource.export_motion_to(
            start_frame, end_frame, json_path
        )
        self._transfer_resource.do_delete()
