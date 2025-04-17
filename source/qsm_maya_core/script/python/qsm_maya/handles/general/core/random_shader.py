# coding:utf-8
import random
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import qsm_maya.core as qsm_mya_core


class RandomShader:
    @classmethod
    @qsm_mya_core.Undo.execute
    def assign_all(cls, shape_paths, seed=0):
        random.seed(seed)
        d = 8

        cs = [x-1 for x in range(1, 256+1) if not x%d]

        for i in shape_paths:
            i_r, i_g, i_b = random.choice(cs), random.choice(cs), random.choice(cs)

            i_material_name = 'random_{}_MTL'.format(bsc_core.BscColor.rgb2hex(i_r, i_g, i_b))
            if qsm_mya_core.Node.is_exists(i_material_name) is False:
                qsm_mya_core.Material.create_as_lambert(
                    i_material_name,
                    # to linear
                    (
                        bsc_core.BscColor.srgb_to_linear(i_r/255.0),
                        bsc_core.BscColor.srgb_to_linear(i_g/255.0),
                        bsc_core.BscColor.srgb_to_linear(i_b/255.0)
                    )
                )
            qsm_mya_core.Material.assign_to(i_material_name, i)
