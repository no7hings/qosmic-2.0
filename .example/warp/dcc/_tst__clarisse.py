# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core


cmd = """
# import lxclarisse

# lxclarisse.set_reload()

import lxclarisse.process as crs_core

o = crs_core.StageOpt()

o.reference_file_to(
    '/library/_3d_plant_proxy/grass/lawn_a/aaaaa', '/production/library/resource/all/3d_plant_proxy/shrub_a001_rsc/v0001/geometry/usd/shrub_a001_rsc.usd'
)

"""


gnl_dcc_core.SocketConnectForClarisse(port=55002).run(cmd)
