# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core

# r = gnl_dcc_core.DotAssOpt(
#     '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v038/cache/ass/laohu_xiao.ass'
# )
#
# print r.get_file_paths()

o = gnl_dcc_core.DotMaOpt(
    '/production/shows/nsa_dev/assets/chr/nikki/shared/mod/modeling/nikki.mod.modeling.v016/maya/nikki.ma'
)

print o.get_node_paths()

