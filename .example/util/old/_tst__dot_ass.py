# coding:utf-8
import lxbasic.dcc.core as bsc_dcc_core

# r = bsc_dcc_core.DotAssOpt(
#     '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v038/cache/ass/laohu_xiao.ass'
# )
#
# print r.get_file_paths()

o = bsc_dcc_core.DotMaOpt(
    '/production/shows/nsa_dev/assets/chr/nikki/shared/mod/modeling/nikki.mod.modeling.v016/maya/nikki.ma'
)

print o.get_node_paths()

