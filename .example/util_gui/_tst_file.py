# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects

p = '/data/f/texture-tx-test/v002/cloth_09.normal.1001.exr'

f = gnl_dcc_objects.StgTexture(p)

print f._get_unit_is_exists_as_ext_tgt_(p, ext_tgt='.jpg')
