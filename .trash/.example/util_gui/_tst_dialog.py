# coding:utf-8
from PySide2 import QtCore, QtWidgets


class W(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        layout = QtWidgets.QVBoxLayout(self)
        self.setFixedSize(640, 320)


if __name__ == '__main__':
    import sys
    #
    app = QtWidgets.QApplication(sys.argv)
    for i in range(100):
        print i
        if i == 10:
            w = W()
            #
            w.exec_()
    #
    sys.exit(app.exec_())
