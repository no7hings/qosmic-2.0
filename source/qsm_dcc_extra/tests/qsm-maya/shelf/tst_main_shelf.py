# coding:utf-8
import lxbasic.core as bsc_core

import lxgui

lxgui.do_reload()

bsc_core.PyReloader2(
    ['lxbasic', 'qsm_general', 'qsm_maya', 'qsm_maya_lazy_tool']
).do_reload()

import qsm_maya.gui as qsm_mya_gui

qsm_mya_gui.MainShelf().create()