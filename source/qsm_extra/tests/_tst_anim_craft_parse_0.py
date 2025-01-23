# coding:utf-8
import lxbasic.content as bsc_content

import lxbasic.storage as bsc_storage

import qsm_general.dotfile.anim_craft as c

print c._Matrix.rotation_matrix_to_euler_angles(
    [
        [
            -0.8921042680740356,
            -0.02059752680361271,
            0.4513603150844574
        ],
        [
            -0.04932306334376335,
            0.9974299073219299,
            -0.05196893587708473
        ],
        [
            -0.4491298794746399,
            -0.06862417608499527,
            -0.8908274173736572
        ]
    ]
)