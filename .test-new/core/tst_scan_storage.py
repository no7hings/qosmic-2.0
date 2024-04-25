# coding:utf-8
import os

import six

import lxbasic.scan as bsc_scan

import lxbasic.storage as bsc_storage


# for i in bsc_scan.ScanBase.get_all_directory_paths('Z:/projects/QSM_TST/assets/chr/sam/work/user.nothings'):
#     print i
#
#
# for i in bsc_scan.ScanBase.get_all_paths('Z:/libraries/resource/all'):
#     print i


# for i in bsc_scan.ScanBase.get_file_paths('Z:/libraries/resource/all/surface/rocky_ground_wf4mdeen/v0001/quixel/texture'):
#     print i


# for i in bsc_scan.ScanBase.get_all_directory_paths('X:/QSM_TST/Assets'):
#     print i
#     print os.path.exists(i)
#     print isinstance(i, six.text_type)

for i in bsc_storage.StgDirectoryOpt(
    'X:/QSM_TST/Assets'
).get_all():
    print i
