# coding:utf-8
import lxbasic.scan as bsc_scan

import cProfile


def test():
    print bsc_scan.ScanGlob.glob('X:/QSM_TST/Assets/chr/*/Rig/Final/scenes/*_Skin.ma')
    # print bsc_core.ScanGlob.glob('Z:/projects/QSM_TST_DFT/work/assets/*/*/mod/modeling')


if __name__ == '__main__':
    test()
    # cProfile.run('test()')
