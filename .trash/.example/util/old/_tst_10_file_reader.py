# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core


f = gnl_dcc_core.DotMtlxOptOld(
    file_path='/l/prod/shl/publish/assets/chr/nn_gongshifu/srf/surfacing/nn_gongshifu.srf.surfacing.v004/look/mtlx/nn_gongshifu.mtlx'
)


print f.get_geometries_properties()
