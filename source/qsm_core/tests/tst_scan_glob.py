# coding:utf-8
import cProfile

import lxbasic.scan as bsc_scan


def test_1():
    print bsc_scan.ScanGlob.glob(
        'X:/QSM_TST/Assets/chr/*/Rig/Final/scenes/*_Skin.ma'
    )

# cProfile.run('test_1()')

