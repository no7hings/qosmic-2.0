# coding:utf-8
import qsm_maya.core as qsm_mya_core

from ..core.main import layer as _man_layer

from ..core.adv import resource as _adv_resource


class AdvChrMotionExportOpt(object):
    def __init__(self, rig_namespace):
        if qsm_mya_core.Namespace.is_exists(rig_namespace) is False:
            raise RuntimeError()

        self._rig_namespace = rig_namespace

        self._adv_resource = _adv_resource.AdvResource(self._rig_namespace)

    def execute(self, json_path):
        self._adv_resource.export_to(json_path)


class AdvChrMotionImportOpt(object):
    @classmethod
    def test(cls):
        qsm_mya_core.SceneFile.new()
        namespace = qsm_mya_core.SceneFile.reference_file(
            'X:/QSM_TST/Assets/chr/lily/Rig/Final/scenes/lily_Skin.ma'
        )
        cls(namespace).execute(
            'Z:/caches/temporary/.shot-cache/replace-reference/E8/7BDBC16B-49E9-3D44-A779-855E68E8C200/sam_Skin.json',
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
        self._mtg_master_layer.append_layer(json_path, start_frame=start_frame)
        self._mtg_master_layer.do_bake()
