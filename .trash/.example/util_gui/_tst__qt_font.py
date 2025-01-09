# coding:utf-8
import sys

from PySide2 import QtWidgets, QtGui

app = QtWidgets.QApplication(sys.argv)
#
print QtGui.QFontDatabase().families()
#
sys.exit(app.exec_())
