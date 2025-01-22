# coding:utf-8
import lxbasic.content as bsc_content

import lxbasic.storage as bsc_storage

import qsm_general.dotfile.anim_craft as c

data = c.DotAcd(
    'Z:/resources/anim_craft/Bow_Crouch_2_Idle_Aim.acd'
).get_dict()


bsc_storage.StgFileOpt(
    'Z:/resources/anim_craft/Bow_Crouch_2_Idle_Aim.json'
).set_write(
    data
)
