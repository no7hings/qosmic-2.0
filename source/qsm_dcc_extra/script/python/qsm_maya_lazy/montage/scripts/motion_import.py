# coding:utf-8
import random
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

from ..core.mixamo import resource as _mxm_resource

from ..core.adv import resource as _adv_resource

from ..core.main import layer as _man_layer


class AdvChrMotionImportOpt(object):
    """
    """
    def __init__(self, namespace):
        self._namespace = namespace
        self._index = 0

    def setup(self):
        self._adv_resource = _adv_resource.AdvResource(
            self._namespace
        )
        self._adv_master_layer = _man_layer.MtgMasterLayer.create_for(
            self._namespace+'_master'
        )
        self._adv_master_layer.connect_to_adv(self._adv_resource)

    def setup_for_mixamo(self):
        qsm_mya_core.SceneFile.reference_file(
            bsc_resource.ExtendResource.get('rig/mixamo_alpha.ma'), self._namespace
        )
        self._mixamo_resource = _mxm_resource.MixamoResource(
            self._namespace
        )
        self._adv_master_layer = _man_layer.MtgMasterLayer.create_for(
            self._namespace+'_master'
        )
        self._adv_master_layer.connect_to_mixamo(self._mixamo_resource)

    @classmethod
    def find_master_layer_path(cls):
        _ = cmds.ls('*:MASTER_LAYER')
        if _:
            return _[0]

    @classmethod
    def setup_for(cls, namespace):
        cls(namespace).setup()
        
    @classmethod
    def append_layer(cls, motion_path):
        master_layer = cls.find_master_layer_path()
        if master_layer:
            opt = _man_layer.MtgMasterLayer(master_layer)
            opt.append_layer(
                motion_path,
                post_cycle=1,
                pre_blend=4,
                post_blend=4,
            )

            start_frame, end_frame = opt.get_frame_range()
            qsm_mya_core.Frame.set_frame_range(
                start_frame, end_frame
            )
            qsm_mya_core.Frame.set_current(end_frame)
        # flush undo
        qsm_mya_core.Undo.flush()

    @classmethod
    def test_(cls):
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            results = qsm_mya_hdl_anm_core.AdvRigAsset.filter_namespaces(namespaces)
            if results:
                cls(results[0]).test()

    def test_random(self):
        self.setup()

        args = [
            ('sam_walk_macho_forward', True),
            ('sam_run_turn_left', False),
            ('sam_walk_forward', True),
            ('sam_walk_sneak_turn_right', False),
            ('sam_run_forward', True),
            ('sam_walk_sneak_forward', True)
        ]

        c = 10
        cycle_times = range(2, 5)
        with bsc_log.LogProcessContext.create(maximum=c) as l_p:
            for i in range(c):
                i_key, i_is_cycle = random.choice(args)
                if i_is_cycle is True:
                    i_cycle = random.choice(cycle_times)
                else:
                    i_cycle = 1

                i_file_path = bsc_resource.ExtendResource.get('motion/{}.json'.format(i_key))

                self._adv_master_layer.append_layer(
                    i_file_path,
                    post_cycle=i_cycle,
                    pre_blend=4, post_blend=4
                )
                l_p.do_update()

        qsm_mya_core.Frame.set_frame_range(
            *self._adv_master_layer.get_frame_range()
        )

    def test(self):
        self.setup()
        data = [
            ('sam_run_forward', 4),
            ('sam_walk_forward', 4),
            # ('sam_walk_sneak_turn_right', 1),
            # ('sam_run_forward', 3),
            # ('sam_walk_sneak_forward', 3)
        ]
        with bsc_log.LogProcessContext.create(maximum=len(data)) as l_p:
            for i_key, i_cycle in data:
                i_file_path = bsc_resource.ExtendResource.get('motion/{}.json'.format(i_key))

                self._adv_master_layer.append_layer(
                    i_file_path,
                    post_cycle=i_cycle,
                    pre_blend=4,
                    post_blend=4,
                )
                l_p.do_update()

        qsm_mya_core.Frame.set_frame_range(
            *self._adv_master_layer.get_frame_range()
        )

    @classmethod
    def test_mixamo_(cls):
        cls('mixamo_test').test_mixamo()

    def test_mixamo(self):
        self.setup_for_mixamo()
        data = [
            ('walking', 2),
            ('slow_run', 2),
            ('medium_run', 2),
            ('fast_run', 2),
            ('jump', 1),
        ]
        with bsc_log.LogProcessContext.create(maximum=len(data)) as l_p:
            for i_key, i_cycle in data:
                i_file_path = bsc_resource.ExtendResource.get('motion/mixamo/{}.json'.format(i_key))

                self._adv_master_layer.append_layer(
                    i_file_path,
                    post_cycle=i_cycle,
                    pre_blend=12,
                    post_blend=12,
                )
                l_p.do_update()

        qsm_mya_core.Frame.set_frame_range(
            *self._adv_master_layer.get_frame_range()
        )

