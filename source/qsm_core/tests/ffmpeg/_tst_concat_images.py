# coding:utf-8
import lxbasic.core as bsc_core

bsc_core.BscFfmpeg.concat_images(
    'X:/QSM_TST/QSM/release/assets/chr/cfx.cfx_rig/lily.cfx.cfx_rig.v001/source/lily.mov',
    [
        'C:/Users/nothings/screenshot/untitled-SMEUX4.png',
        'C:/Users/nothings/screenshot/untitled-SMF3Y7.png'
    ],
    replace=True
)
