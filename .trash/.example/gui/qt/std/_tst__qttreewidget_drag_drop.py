# coding:utf-8
from PySide2.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow
from PySide2.QtCore import Qt, QMimeData
from PySide2.QtGui import QDrag


class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.setDragEnabled(True)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.itemPressed.connect(self.handle_item_pressed)
        self.itemChanged.connect(self.handle_item_changed)

    def handle_item_pressed(self, item, column):
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())

    def handle_item_changed(self, item, column):
        if item.parent() is None:
            # top-level item
            return
        parent = item.parent()
        index = parent.indexOfChild(item)
        text = item.text(column)
        new_item = QTreeWidgetItem(parent, [text])
        parent.takeChild(index)
        parent.insertChild(index, new_item)

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return

        item = self.currentItem()
        if not item:
            return

        mime_data = QMimeData()
        mime_data.setText(item.text(0))

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.tree = MyTreeWidget(self)
        self.tree.setColumnCount(1)
        for i in range(3):
            parent = QTreeWidgetItem(self.tree, ['Parent {}'.format(i)])
            for j in range(4):
                child = QTreeWidgetItem(parent, ['Child {}'.format(j)])
        self.setCentralWidget(self.tree)

if __name__ == '__main__':

    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
