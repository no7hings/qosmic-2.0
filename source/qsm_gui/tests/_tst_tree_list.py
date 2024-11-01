# coding:utf-8
from PyQt5 import QtCore, QtGui, QtWidgets


class _QtListItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QtWidgets.QStyledItemDelegate.__init__(self, *args, **kwargs)

    def paint(self, painter, option, index):
        # super(_QtListItemDelegate, self).paint(painter, option, index)
        item = self.parent().itemFromIndex(index)
        item.paint(painter, option, index)

    def sizeHint(self, option, index):
        item = self.parent().itemFromIndex(index)
        return item.sizeHint()


class GroupItem(QtWidgets.QListWidgetItem):
    HEIGHT = 20

    def __init__(self, *args):
        super(GroupItem, self).__init__(*args)

    def sizeHint(self):
        width = self.listWidget().viewport().width()
        return QtCore.QSize(width, self.HEIGHT)

    def paint(self, painter, option, index):
        painter.save()

        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()

        rect = QtCore.QRect(x+1, y+1, w-2, h-2)

        text = self.text()

        if bool(option.state & QtWidgets.QStyle.State_Selected) is True:
            painter.setBrush(QtGui.QColor(63, 127, 255))
            painter.drawRect(
                rect
            )

        painter.drawText(
            rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text
        )

        painter.restore()


class Item(QtWidgets.QListWidgetItem):
    def __init__(self, *args):
        super(Item, self).__init__(*args)

    def paint(self, painter, option, index):
        painter.save()

        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()

        rect = QtCore.QRect(x+1, y+1, w-2, h-2)

        text = self.text()

        if bool(option.state & QtWidgets.QStyle.State_Selected) is True:
            painter.setBrush(QtGui.QColor(63, 127, 255))
            painter.drawRect(rect)
        else:
            painter.setBrush(QtGui.QColor(127, 127, 127))
            painter.drawRect(rect)

        painter.drawText(
            rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text
        )

        painter.restore()


class ListWidget(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super(ListWidget, self).__init__(*args, **kwargs)

        self.setViewMode(self.IconMode)

        self.setGridSize(QtCore.QSize(-1, -1))

        self.setResizeMode(QtWidgets.QListWidget.Adjust)

        self.setSortingEnabled(True)

        self.setItemDelegate(
            _QtListItemDelegate(self)
        )


class TreeListView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TreeListView, self).__init__(*args, **kwargs)

        self._listWidget = ListWidget(self)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._listWidget)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("TEST")

        self._widget = TreeListView()
        self.setCentralWidget(self._widget)

        group_item = GroupItem('/Group-0', self._widget._listWidget)
        group_item.setSizeHint(QtCore.QSize(400, 20))
        self._widget._listWidget.addItem(
            group_item
        )

        for i in range(5):
            item = Item('/Group-0/Item-{}'.format(i), self._widget._listWidget)
            item.setSizeHint(QtCore.QSize(120+i*10, 120))
            self._widget._listWidget.addItem(item)

        group_item = GroupItem('/Group-1', self._widget._listWidget)
        group_item.setSizeHint(QtCore.QSize(400, 20))
        self._widget._listWidget.addItem(
            group_item
        )

        for i in range(5):
            item = Item('/Group-1/Item-{}'.format(i), self._widget._listWidget)
            item.setSizeHint(QtCore.QSize(120+i*10, 120))
            self._widget._listWidget.addItem(item)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setGeometry(200, 200, 480, 480)
    main_window.show()
    sys.exit(app.exec_())
