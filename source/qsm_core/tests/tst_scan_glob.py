# coding:utf-8
import cProfile

import lxbasic.scan as bsc_scan


def test_0():
    print bsc_scan.ScanGlob.glob(
        'X:/QSM_TST/Assets/*/*/Rig/Final/scenes/*_Skin.ma'
    )


def test_1():
    def fnc_(path_):
        print path_

    bsc_scan.ScanGlob.generate_glob_executor(
        'X:/QSM_TST/Assets/*/*/Rig/Final/scenes/*_Skin.ma', fnc_
    )


# cProfile.run('test_1()')

# test_1()

# test_0()

# print bsc_scan.ScanGlob.filter_all_files_from(
#     'X:/QSM_TST/Assets', '*_Skin.ma'
# )

print bsc_scan.ScanGlob.glob_all_files('X:/QSM_TST/Assets/*//*_Skin.ma')

print bsc_scan.ScanGlob.glob_all_files('X:/QSM_TST/Assets/*/*/Rig/Final/scenes/*_Skin.ma')
