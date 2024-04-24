# coding:utf-8
import lxbasic.core as bsc_core

if __name__ == '__main__':
    print bsc_core.ScanGlob.glob('X:/QSM_TST/Assets/*/sam/Rig/Final')
    print bsc_core.PtnBaseMtd.glob_fnc('X:/QSM_TST/Assets/*/*/Rig/Final')
