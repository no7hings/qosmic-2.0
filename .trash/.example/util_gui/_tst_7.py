# coding:utf-8

if __name__ == '__main__':
    from PySide2 import QtCore, QtGui, QtWidgets
    #
    import sys
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    print QtWidgets.QApplication.translate(
        "Splash", "Dialog", None, -1
    )
    #
    sys.exit(app.exec_())
