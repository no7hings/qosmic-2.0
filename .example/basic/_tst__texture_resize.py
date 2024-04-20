# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

f_src = '/l/prod/cgm/work/shots/z95/z95141/srf/surfacing/texture/small_disp_tx/oceanevaluate_small.disp.<udim>.####.tx'

fs = bsc_storage.StgFileMtdForMultiply.get_exists_unit_paths(
    f_src
)

print fs

for i in fs:
    i_f = bsc_storage.StgFileOpt(i)
    i_f_p_tgt = '{}/output_8192/{}'.format(
        bsc_storage.StgDirectoryOpt(i_f.get_directory_path()).get_parent_path(), i_f.get_name()
    )
    if bsc_storage.StgFileOpt(i_f_p_tgt).get_is_file() is False:
        print i_f_p_tgt
        bsc_storage.ImgOiioMtd.fit_to(
            i,
            i_f_p_tgt,
            (8192, 8192)
        )
