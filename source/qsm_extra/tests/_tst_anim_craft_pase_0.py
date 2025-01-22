# coding:utf-8
import lxbasic.content as bsc_content

import qsm_general.dotfile as c

print bsc_content.ToString(
    c.DotAcd(
        'Z:/resources/anim_craft/Bow_Crouch_2_Idle_Aim.acd'
    ).get_dict()
).generate()
