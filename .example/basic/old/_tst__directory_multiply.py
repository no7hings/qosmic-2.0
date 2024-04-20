# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


# dic = bsc_storage.StgDirectoryMtdForMultiply.get_all_multiply_file_dict(
#     '/data/f/sequence_chart_test/chr_a/R2', '*.%04d.*'
# )
#
# for k, v in dic.items():
#     print bsc_core.RawIntArrayMtd.merge_to(v)

# print bsc_storage.StgFileMtdForMultiply.get_number_args(
#     'A.1001.1001.exr', '*.<udim>.%04d.*'
# )
# print bsc_storage.StgFileMtdForMultiply.get_number_args(
#     'A.1001.exr', '*.####.*'
# )

print bsc_core.PtnMultiplyFileMtd.to_fnmatch_style(
    '*.$F03.$F04.*'
)
