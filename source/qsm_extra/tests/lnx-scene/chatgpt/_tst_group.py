# coding:utf-8
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QGraphicsItemGroup
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QEvent
import sys

class ResizableGroup(QGraphicsItemGroup):
    """ 可手动调整大小的 Group """
    def __init__(self):
        super(ResizableGroup, self).__init__()
        self.border = QGraphicsRectItem(self)  # 作为边界框
        self.border.setPen(QPen(Qt.DashLine))  # 设置虚线框
        # self.border.setBrush(Qt.NoBrush)  # 无填充
        self.border.setZValue(-1)  # 让边界框在底层

        self.setFlag(QGraphicsItem.ItemIsMovable)  # 允许整个组移动
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)  # 允许发送几何变化事件

    def addToGroup(self, item):
        """ 添加子项并更新边界 """
        super(ResizableGroup, self).addToGroup(item)
        item.setParentItem(self)  # 让子项归属于 Group
        self.updateBoundingBox()

    def removeFromGroup(self, item):
        """ 移除子项并更新边界 """
        super(ResizableGroup, self).removeFromGroup(item)
        self.updateBoundingBox()

    def updateBoundingBox(self):
        """ 计算所有子项的整体边界，并更新边界框 """
        if self.childItems():
            rect = self.childrenBoundingRect().adjusted(-5, -5, 5, 5)  # 适当扩展边界
            self.border.setRect(rect)  # 更新边界框大小
        else:
            self.border.setRect(QRectF())  # 没有子项时清空边界

    def itemChange(self, change, value):
        """ 重载 itemChange，控制物体的移动行为 """
        if change == QGraphicsItem.ItemPositionChange:
            new_pos = value
            group_rect = self.border.rect()  # 获取组的边界矩形

            # 如果子物体在组内的范围内，允许移动
            if group_rect.contains(new_pos):
                return new_pos
            else:
                return self.pos()  # 不在组内则不移动
        return super(ResizableGroup, self).itemChange(change, value)


class MovableRect(QGraphicsRectItem):
    """ 可移动的矩形节点 """
    def __init__(self, x, y, color):
        super(MovableRect, self).__init__(0, 0, 60, 40)  # 让原点在 (0,0)
        self.setBrush(QBrush(QColor(color)))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)  # 设置初始位置


class GraphicsTest(QGraphicsView):
    def __init__(self):
        super(GraphicsTest, self).__init__()

        # 创建场景
        self.scene = QGraphicsScene(0, 0, 500, 500)
        self.setScene(self.scene)

        # 创建可调整大小的 Group
        self.group = ResizableGroup()
        self.scene.addItem(self.group)

        # 创建子节点
        self.create_nodes()

        # 允许抗锯齿渲染
        # self.setRenderHint(self.renderHints() | self.renderHints().Antialiasing)

    def create_nodes(self):
        """ 创建几个节点并添加到 Group """
        colors = ["red", "blue", "green", "yellow"]
        positions = [(0, 0), (100, 50), (50, 150), (150, 100)]

        for i, (x, y) in enumerate(positions):

            rect = MovableRect(x, y, colors[i])
            if i%2:
                self.group.addToGroup(rect)  # 添加到 Group
            # else:
            #     self.scene.addItem(rect)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphicsTest()
    window.show()
    sys.exit(app.exec_())
