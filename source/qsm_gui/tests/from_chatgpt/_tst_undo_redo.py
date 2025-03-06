# coding:utf-8
from PyQt5 import QtWidgets, QtCore, QtGui

# 定义一个复合的 UndoCommand，用来保存多个节点的移动操作
class MoveNodesCommand(QtWidgets.QUndoCommand):
    def __init__(self, items, old_positions, new_positions):
        super(MoveNodesCommand, self).__init__()
        self.items = items  # 需要移动的节点列表
        self.old_positions = old_positions  # 节点的旧位置
        self.new_positions = new_positions  # 节点的新位置

    def undo(self):
        """撤销操作，将所有节点位置恢复到旧位置"""
        for item, old_pos in zip(self.items, self.old_positions):
            item.setPos(old_pos)

    def redo(self):
        """重做操作，将所有节点移动到新位置"""
        for item, new_pos in zip(self.items, self.new_positions):
            item.setPos(new_pos)


class NodeItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, width, height, undo_stack):
        super(NodeItem, self).__init__(x, y, width, height)
        self.setBrush(QtGui.QColor(100, 100, 250))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)  # 使节点可以拖动
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)  # 使节点可以选中
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)  # 发送几何变化

        # 关联 UndoStack
        self.undo_stack = undo_stack

    def mouseMoveEvent(self, event):
        """重载鼠标移动事件，保存 Undo/Redo 操作"""
        # 获取当前节点的位置
        old_pos = self.pos()

        # 让父类处理移动
        super(NodeItem, self).mouseMoveEvent(event)

        # 获取新的节点位置
        new_pos = self.pos()

        # 如果位置发生变化，创建一个移动操作并将其加入到 Undo Stack
        if old_pos != new_pos:
            command = MoveNodesCommand([self], [old_pos], [new_pos])  # 传入当前节点的移动操作
            self.undo_stack.push(command)

    def get_pos(self):
        return self.pos()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Undo/Redo Multiple Node Movement Example")
        self.setGeometry(100, 100, 800, 600)

        # 初始化 Undo Stack
        self.undo_stack = QtWidgets.QUndoStack()

        # 创建图形场景和视图
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setGeometry(50, 50, 700, 500)

        # 创建多个节点并添加到场景
        self.node1 = NodeItem(100, 100, 100, 60, self.undo_stack)
        self.node2 = NodeItem(300, 100, 100, 60, self.undo_stack)
        self.node3 = NodeItem(500, 100, 100, 60, self.undo_stack)

        self.scene.addItem(self.node1)
        self.scene.addItem(self.node2)
        self.scene.addItem(self.node3)

        # 创建 Undo/Redo 按钮
        undo_button = QtWidgets.QPushButton("Undo", self)
        redo_button = QtWidgets.QPushButton("Redo", self)
        undo_button.clicked.connect(self.undo_stack.undo)
        redo_button.clicked.connect(self.undo_stack.redo)

        undo_button.setGeometry(50, 550, 80, 30)
        redo_button.setGeometry(150, 550, 80, 30)

        # 添加布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(undo_button)
        layout.addWidget(redo_button)
        self.setLayout(layout)

    def move_selected_nodes(self):
        """批量移动选中的节点，并将操作添加到 Undo Stack"""
        selected_items = self.scene.selectedItems()
        if len(selected_items) > 0:
            old_positions = [item.get_pos() for item in selected_items]
            new_positions = [item.get_pos() + QtCore.QPointF(50, 0) for item in selected_items]  # 移动50单位
            command = MoveNodesCommand(selected_items, old_positions, new_positions)
            self.undo_stack.push(command)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # 创建主窗口并显示
    window = MainWindow()
    window.show()

    # 批量移动选中的节点
    window.move_selected_nodes()

    app.exec_()
