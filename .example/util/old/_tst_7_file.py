# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects

f = bsc_dcc_objects.StgFileForMultiply(
    '/l/prod/cg7/publish/shots/z88/z88030/efx/efx/z88030.efx.efx.v006/cache/fire/bgeo_sc/fire.$F.bgeo.sc'
)

print f.get_has_elements()
