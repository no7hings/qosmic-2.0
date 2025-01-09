# coding:utf-8
from PySide2 import QtWidgets, QtGui, QtCore


class MenuProxyStyle(QtWidgets.QProxyStyle):

    def drawControl(self, element, option, painter, widget=None):
        if element == QtWidgets.QStyle.CE_MenuItem:
            opt = QtWidgets.QStyleOptionMenuItem()
            opt.init(widget)
            # widget.initStyleOption(option)
            # opt.state |= QtWidgets.QStyle.State_Active
            print opt.rect
            painter.fillRect(opt.rect, QtGui.QColor(255, 0, 0, 255))

            print opt.menuRect
            print opt.text
            text_rect = self.subElementRect(QtWidgets.QStyle.SE_ItemViewItemText, opt, widget)
            painter.drawText(text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, opt.text)
        else:
            super(MenuProxyStyle, self).drawControl(element, option, painter, widget)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        menu = QtWidgets.QMenu("File", self)
        menu.setTitle('test')
        self.menuBar().addMenu(menu)

        # create icons
        data = [("Absolute", "Ctrl+Alt+C"),
                 ("Relative", "Ctrl+Shift+C"),
                 ("Copy", "Ctrl+C")]

        for text, shortcut in data:
            action = QtWidgets.QAction(self)
            action.setText(text+"\t"+shortcut)
            menu.addAction(action)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(MenuProxyStyle())
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
