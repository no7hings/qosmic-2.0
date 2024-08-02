# coding:utf-8
import random
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import lxbasic.log as bsc_log

import qsm_maya.core as qsm_mya_core

import qsm_maya.animation.core as qsm_mya_anm_core

from .. import core as _core


class AdvChrMotionImportOpt(object):
    """
# coding:utf-8
import qsm_maya_adv
reload(qsm_maya_adv)
qsm_maya_adv.do_reload()

import qsm_maya_adv.scripts as s

s.AdvChrMotionImportOpt('sam_Skin').test()
    """
    def __init__(self, namespace):
        self._namespace = namespace
        # self._adv_character = _core.AdvResource(self._namespace)
        self._index = 0

    def setup(self):
        self._adv_resource = _core.AdvResource(
            self._namespace
        )

        self._adv_master_layer = _core.AdcChrMotionMasterLayer.create_for(
            self._namespace+'_master'
        )
        self._adv_master_layer.connect_to_resource(self._adv_resource)

    @classmethod
    def test_(cls):
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        if namespaces:
            results = qsm_mya_anm_core.AdvRig.filter_namespaces(namespaces)
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
                    pre_blend_frame=4, post_blend_frame=4
                )
                l_p.do_update()

        qsm_mya_core.Frame.set_frame_range(
            *self._adv_master_layer.get_frame_range()
        )

    def test(self):
        self.setup()
        with bsc_log.LogProcessContext.create(maximum=2) as l_p:
            for i_key, i_cycle in [
                ('sam_run_forward', 2),
                ('sam_walk_forward', 2),
                ('sam_walk_sneak_turn_right', 1),
                ('sam_run_forward', 3),
                ('sam_walk_sneak_forward', 3)
            ]:
                i_file_path = bsc_resource.ExtendResource.get('motion/{}.json'.format(i_key))

                self._adv_master_layer.append_layer(
                    i_file_path,
                    post_cycle=i_cycle,
                    pre_blend_frame=4,
                    post_blend_frame=4,
                )
                l_p.do_update()

        qsm_mya_core.Frame.set_frame_range(
            *self._adv_master_layer.get_frame_range()
        )

