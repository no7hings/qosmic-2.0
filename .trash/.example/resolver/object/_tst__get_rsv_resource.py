# coding:utf-8
import lxbasic.log as bsc_log

import lxresolver.core as rsv_core

bsc_log.Log.RESULT_ENABLE = False

r = rsv_core.RsvBase.generate_root()

for i_project in [
    'cgm',
    'nsa_dev'
]:
    i_rsv_project = r.get_rsv_project(project=i_project)

    print i_rsv_project.get_rsv_resource(
        asset='sunny01_lightrig'
    )
