# coding:utf-8
from __future__ import print_function

from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QBrush

# Python 2.7 兼容的 print 函数



class Node(QGraphicsRectItem):
    def __init__(self, x, y):
        super(Node, self).__init__(x, y, 50, 50)  # 创建一个 50x50 的矩形节点
        self.setBrush(QBrush(QColor(0, 0, 255)))  # 设置为蓝色
        self.setFlag(QGraphicsRectItem.ItemIsMovable)  # 允许移动


class MyGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super(MyGraphicsView, self).__init__(scene)
        # self.setRenderHint(self.Antialiasing)  # 启用抗锯齿
        # self.setRenderHint(self.SmoothPixmapTransform)  # 启用平滑像素变换


def get_nodes_in_rect(view, scene, rect):
    """
    获取指定矩形范围内的所有 Node
    :param view: QGraphicsView，视图对象
    :param scene: QGraphicsScene，场景对象
    :param rect: QRectF，指定的矩形范围（视图坐标系）
    :return: list，包含所有在指定范围内的 Node
    """
    # 将视图坐标系中的矩形转换为场景坐标系中的矩形
    scene_rect = QRectF(view.mapToScene(rect.topLeft().toPoint()), view.mapToScene(rect.bottomRight().toPoint()))

    nodes_in_range = []

    # 使用 QGraphicsScene.items(rect) 获取指定范围内的项
    for item in scene.items(scene_rect):
        if isinstance(item, Node):  # 只筛选 Node 类型的项
            nodes_in_range.append(item)

    return nodes_in_range


if __name__ == "__main__":
    app = QApplication([])

    # 创建场景
    scene = QGraphicsScene()

    # 创建节点
    node1 = Node(100, 100)
    node2 = Node(200, 150)
    node3 = Node(500, 500)
    scene.addItem(node1)
    scene.addItem(node2)
    scene.addItem(node3)

    # 创建视图
    view = MyGraphicsView(scene)
    view.setScene(scene)

    # 获取范围内的节点，视图坐标系中的矩形
    rect = QRectF(50, 50, 300, 200)  # 指定的矩形范围（视图坐标系）
    nodes_in_range = get_nodes_in_rect(view, scene, rect)

    # 输出所有在范围内的节点
    print("Nodes in range:")
    for node in nodes_in_range:
        print("Node at ({}, {})".format(node.x(), node.y()))  # Python 2.7 兼容的字符串格式化

    view.show()
    app.exec_()

