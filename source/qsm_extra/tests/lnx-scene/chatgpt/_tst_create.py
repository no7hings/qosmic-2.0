# coding:utf-8
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor
import sys


class CheckableItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super(CheckableItem, self).__init__(x, y, width, height)

        self.checked = False
        self.setBrush(QBrush(QColor(200, 200, 200)))  # 默认颜色
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)  # 允许选择

    def mousePressEvent(self, event):
        self.toggleChecked()
        super(CheckableItem, self).mousePressEvent(event)

    def toggleChecked(self):
        if self.checked:
            self.checked = False
            self.setBrush(QBrush(QColor(200, 200, 200)))  # 未选中
            self.setZValue(0)  # 还原 Z 轴优先级
        else:
            self.scene().clearSelection()  # 取消其他 Item 选择
            for item in self.scene().items():
                if isinstance(item, CheckableItem):
                    item.checked = False
                    item.setBrush(QBrush(QColor(200, 200, 200)))
                    item.setZValue(0)  # 还原 Z 轴

            self.checked = True
            self.setBrush(QBrush(QColor(100, 200, 100)))  # 选中颜色
            self.setZValue(1)  # 设置最高优先级


class GraphicsView(QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # 创建多个 CheckableItem
        for i in range(3):
            item = CheckableItem(i*60, 0, 50, 50)
            self.scene.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = GraphicsView()
    view.show()
    sys.exit(app.exec_())

