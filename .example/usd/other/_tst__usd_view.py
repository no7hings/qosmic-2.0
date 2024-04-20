# coding:utf-8
from lxgui.qt_for_usd.core.wrap import *

import argparse

import sys
#
from PySide2 import QtWidgets

p = argparse.ArgumentParser(
    description='View a usd file'
)

p_o = p.parse_args()
#
app = QtWidgets.QApplication(sys.argv)

s = Usdviewq.settings2.Settings('1')
#
d_m = Usdviewq.appController.UsdviewDataModel(False, s)
d_m.stage = Usd.Stage.Open('/production/library/resource/all/3d_asset/metal_pot_vfyqcj2ga/v0001/geometry/usd/metal_pot_vfyqcj2ga.usd', Usd.Stage.LoadAll)
w = QtWidgets.QMainWindow()
s = Usdviewq.stageView.StageView(parent=w, dataModel=d_m)
w.setCentralWidget(s)
w.show()
#
sys.exit(app.exec_())


