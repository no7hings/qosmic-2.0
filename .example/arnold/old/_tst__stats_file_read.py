# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects

import lxarnold.core as and_core


f = '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v038/render/output/default.stats.0001.json'

o = and_core.StatsFileOpt(
    gnl_dcc_objects.StgFile(f)
)

o._test_()
