# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects

import lxarnold.core as and_core


f = '/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/render/output/default.profile.0001.json'

o = and_core.ProfileFileOpt(
    gnl_dcc_objects.StgFile(f)
)

o._test_()
