# coding:utf-8
from PySide2 import QtCore, QtWidgets, QtUiTools


class W(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setFixedSize(800, 600)
        self.ui = QtUiTools.QUiLoader().load('/home/dongchangbao/packages/lxdcc_lib/0.0.99/bin/linux-x64-python-2.7.18/lib/python2.7/site-packages/PySide2/examples/webchannel/standalone/dialog.ui', self)
        # print dir(self.ui)

        print self.ui.output


if __name__ == '__main__':
    import sys
    #
    app = QtWidgets.QApplication(sys.argv)
    w = W()
    #
    w.ui.show()
    #
    sys.exit(app.exec_())
