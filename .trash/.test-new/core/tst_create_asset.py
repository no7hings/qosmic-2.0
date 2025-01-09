# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

d = bsc_storage.StgFileOpt(
    'E:/myworkspace/qosmic-2.0/.test-new/asset_names.json'
).set_read()

# for i in d['chr']:
#
#     for j in ['mod/modeling', 'grm/grooming', 'srf/surfacing', 'rig/rigging']:
#         j_dir = 'Z:/projects/QSM_TST_DFT/work/assets/chr/{}/{}'.format(i.lower(), j)
#         bsc_storage.StgDirectoryOpt(j_dir).set_create()

# for i in d['prp']:
#
#     for j in ['mod/modeling', 'srf/surfacing', 'rig/rigging']:
#         j_dir = 'Z:/projects/QSM_TST_DFT/work/assets/prp/{}/{}'.format(i.lower(), j)
#         bsc_storage.StgDirectoryOpt(j_dir).set_create()

# for i in d['chr']:
#
#     for j in ['Rig/Final']:
#         j_dir = 'X:/QSM_TST/Assets/chr/{}/{}'.format(i.lower(), j)
#         print j_dir
#         bsc_storage.StgDirectoryOpt(j_dir).set_create()

# for i in d['prp']:
#
#     for j in ['Rig/Final']:
#         j_dir = 'X:/QSM_TST/Assets/prp/{}/{}'.format(i.lower(), j)
#         bsc_storage.StgDirectoryOpt(j_dir).set_create()
