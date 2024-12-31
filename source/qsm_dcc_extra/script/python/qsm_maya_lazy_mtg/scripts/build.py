# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

from ..core.base import util as _bsc_util

from ..core.mocap import resource as _mcp_resource

from ..core.adv import resource as _adv_resource

from ..core.main import layer as _man_layer

from ..core.main import stage as _man_stage


class MtgBuildScp(object):
    """
    """
    MOTION_JSON_PTN = 'Z:/libraries/lazy-resource/all/motion_splice/{name}/json/{name}.motion.json'

    def __init__(self, namespace):
        self._rig_namespace = namespace
        self._index = 0

    @classmethod
    def to_master_layer_namespace(cls, rig_namespace):
        return _bsc_util.MtgRigNamespace.to_master_layer_namespace(rig_namespace)

    def setup_for_mocap(self, rig_name='alpha'):
        qsm_mya_core.SceneFile.reference_file(
            bsc_resource.ExtendResource.get('rig/{}.ma'.format(rig_name)), self._rig_namespace
        )
        self._mocap_resource = _mcp_resource.MocapResource(self._rig_namespace)
        self._mtg_master_layer = _man_layer.MtgMasterLayer.generate_fnc(self._rig_namespace)
        self._mtg_master_layer.connect_to_mocap(self._mocap_resource)

    def setup_for_adv(self):
        self._adv_resource = _adv_resource.AdvResource(
            self._rig_namespace
        )
        self._mtg_master_layer = _man_layer.MtgMasterLayer.generate_fnc(self._rig_namespace)
        self._mtg_master_layer.connect_to_adv(self._adv_resource)

    def load_template(self, template='walking_running_jumping'):
        track_json_path = 'Z:/resources/montage/{}.jsz'.format(template)

        if os.path.isfile(track_json_path) is True:
            _man_stage.MtgStage(self._rig_namespace).import_track_json(track_json_path)

    def load_template_old(self, template='walking_running_jumping'):
        data = None
        if template == 'walking_running_jumping':
            data = [
                ('a_pose', 1, 4, 4),
                ('jog_backward', 1, 4, 4),
                ('idle_1', 1, 4, 4),
                ('slow_run', 2, 4, 4),
                ('medium_run', 2, 4, 4),
                ('fast_run', 2, 4, 4),
                ('jump', 1, 4, 4),
            ]
        elif template == 'dancing':
            data = [
                ('a_pose', 1, 4, 4),
                ('gangnam_style', 1, 4, 4),
                ('northern_soul_spin', 1, 4, 4),
            ]

        if data:
            with bsc_log.LogProcessContext.create(maximum=len(data)) as l_p:
                for i_name, i_cycle, i_pre_blend, i_post_blend in data:
                    i_file_path = self.MOTION_JSON_PTN.format(name=i_name)
                    if os.path.exists(i_file_path) is False:
                        raise RuntimeError()

                    self._mtg_master_layer.append_layer(
                        i_file_path,
                        post_cycle=i_cycle,
                        pre_blend=i_pre_blend,
                        post_blend=i_post_blend,
                    )
                    l_p.do_update()

            qsm_mya_core.Frame.set_frame_range(
                *self._mtg_master_layer.get_frame_range()
            )

    @classmethod
    def import_motion_json(cls, rig_namespace, motion_json_path):
        master_layer_location = _man_layer.MtgMasterLayer.find_one_master_layer_location(rig_namespace)

        if master_layer_location:
            mtg_master_layer = _man_layer.MtgMasterLayer(master_layer_location)
            mtg_master_layer.append_layer(
                motion_json_path, post_cycle=1, pre_blend=8, post_blend=8,
            )

            start_frame, end_frame = mtg_master_layer.get_frame_range()
            qsm_mya_core.Frame.set_frame_range(
                start_frame, end_frame
            )
            qsm_mya_core.Frame.set_current(end_frame)
        # flush undo
        qsm_mya_core.Undo.flush()

    @classmethod
    def test_mocap(cls, template='walking_running_jumping'):
        qsm_mya_core.SceneFile.new()
        qsm_mya_core.Frame.set_fps_tag('30_fps')
        scp = cls('test')
        scp.setup_for_mocap()
        scp.load_template(template)

    @classmethod
    def test_adv(cls):
        qsm_mya_core.SceneFile.new()
        qsm_mya_core.SceneFile.reference_file(
            'X:/QSM_TST/Assets/chr/sam/Rig/Final/scenes/sam_Skin.ma',
            'sam_Skin'
        )
        scp = cls('sam_Skin')
        scp.setup_for_adv()
        scp.load_template()

    @classmethod
    def test_adv_auto(cls):
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            results = qsm_mya_hdl_anm_core.AdvRigAsset.filter_namespaces(namespaces)
            if results:
                scp = cls(results[0])
                scp.setup_for_adv()
                scp.load_template()

    @classmethod
    def test_import_track_json(cls):
        # qsm_mya_core.SceneFile.new()
        #
        # qsm_mya_core.Frame.set_fps_tag('30_fps')
        # scp = cls('test')
        # scp.setup_for_mocap()

        _man_stage.MtgStage(
            'test'
        ).import_track_json(
            'Z:/resources/montage/dancing.jsz'
        )

    @classmethod
    def test_update_track_json(cls, namespace='test'):
        # qsm_mya_core.SceneFile.new()
        #
        # qsm_mya_core.Frame.set_fps_tag('30_fps')
        # scp = cls('test')
        # scp.setup_for_mocap()

        _man_stage.MtgStage(
            namespace
        ).update_track_json(
            'Z:/resources/montage/dancing.jsz'
        )

