# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

print bsc_storage.StgPathMtd.get_is_writable(
    '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/test/v001'
)


print bsc_core.CameraMtd.get_front_transformation(
    geometry_args=((0, 0, 0), (0, 0, 0), (1, 1, 1)),
    angle=1,
    bottom=True
)
