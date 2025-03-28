# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from ..core.main import layer as _man_layer

from ..core.adv import resource as _adv_resource

from ..core.transfer import handle as _trs_handle


class AdvChrMotionExportOpt(object):
    @classmethod
    def test(cls):
        # qsm_mya_core.SceneFile.new()
        cls('sam_Skin').execute(
            'Z:/temporaries/premiere_xml_test/motion/test.jsz'
        )

    def __init__(self, rig_namespace):
        if qsm_mya_core.Namespace.is_exists(rig_namespace) is False:
            raise RuntimeError()

        self._rig_namespace = rig_namespace

    def execute(self, json_path, frame_range=None):
        h = _trs_handle.AdvTransferHandle(self._rig_namespace)
        h.setup()
        h.connect()
        h.export_motion_to(json_path, frame_range)


class AdvChrMotionImportOpt(object):
    @classmethod
    def test(cls):
        namespace = qsm_mya_core.SceneFile.reference_file(
            'X:/QSM_TST/Assets/chr/lily/Rig/Final/scenes/lily_Skin.ma', 'lily_Skin'
        )
        cls(namespace).execute(
            'Z:/temporaries/premiere_xml_test/motion/test.jsz',
            start_frame=30
        )

    def __init__(self, rig_namespace):
        if qsm_mya_core.Namespace.is_exists(rig_namespace) is False:
            raise RuntimeError()

        self._rig_namespace = rig_namespace

        self._adv_resource = _adv_resource.AdvResource(self._rig_namespace)

    def build_splice(self):
        self._mtg_master_layer = _man_layer.MtgMasterLayer.generate_fnc(self._rig_namespace)
        self._mtg_master_layer.connect_to_adv_resource(self._adv_resource)

    def execute(self, json_path, start_frame=1):
        self.build_splice()
        data = bsc_storage.StgFileOpt(json_path).set_read()
        scale = data['scale']
        mtg_layer = self._mtg_master_layer.append_layer(json_path, start_frame=start_frame)
        mtg_layer.apply_root_scale(scale)
        # self._mtg_master_layer.do_bake()
