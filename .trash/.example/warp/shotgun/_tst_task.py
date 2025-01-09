# coding:utf-8
import lxresolver.core as rsv_core

import lxbasic.shotgun as bsc_shotgun

r = rsv_core.RsvBase.generate_root()

branch = 'asset'

rsv_project = r.get_rsv_project(project='lib')

stg_connector = bsc_shotgun.StgConnector()

print stg_connector.get_stg_task(
    project='lib', asset='yellow_fabric', step='srf', task='surfacing'
)

