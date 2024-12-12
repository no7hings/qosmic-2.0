# coding:utf-8
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QLineEdit

from PyQt5.QtCore import Qt


class EditableTreeWidget(QTreeWidget):
    def __init__(self):
        super(EditableTreeWidget, self).__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(['Editable Items'])
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.current_edit = None  # 用于存储当前的编辑器

    def add_item(self, text):
        item = QTreeWidgetItem([text])
        self.addTopLevelItem(item)

    def on_item_double_clicked(self, item, column):
        if not self.current_edit:  # 如果没有处于编辑状态
            line_edit = QLineEdit(self)
            line_edit.setText(item.text(column))
            line_edit.setFocus()
            line_edit.returnPressed.connect(lambda: self.finish_edit(line_edit, item, column))
            line_edit.editingFinished.connect(lambda: self.finish_edit(line_edit, item, column))
            self.setItemWidget(item, column, line_edit)
            self.current_edit = line_edit

    def finish_edit(self, line_edit, item, column):
        if self.current_edit == line_edit:
            new_text = line_edit.text()
            item.setText(column, new_text)  # 更新 item 的文本
            self.removeItemWidget(item, column)  # 移除编辑器
            self.current_edit = None  # 退出编辑状态

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    tree = EditableTreeWidget()
    tree.add_item('Double-click to edit me')
    tree.add_item('Another item')
    tree.show()
    sys.exit(app.exec_())
