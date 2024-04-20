# coding:utf-8
import os

import lxbasic.storage as bsc_storage

d = '/h/FTP/dongshi/to_dongshi/production_files/s10090.efx.efx_galaxy_xuanzi.v006/images/s10090.efx.nebula.v012/images/RENDER_nebula_front_dense_deep'

print os.path.exists(d)

f = '/h/FTP/dongshi/to_dongshi/production_files/s10090.efx.efx_galaxy_xuanzi.v006/images/s10090.efx.nebula.v012/images/RENDER_nebula_front_dense_deep/RENDER_nebula_front_dense_deep.1002.exr'

print os.path.exists(f)

print os.access(f, os.R_OK)

print bsc_storage.StgPathMtd.set_map_to_nas(f)

# f = '/l/temp/td/dongchangbao/test_a'
