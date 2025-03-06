# coding:utf-8
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication
from PyQt5.QtGui import QPainterPath, QBrush, QPen, QPainter, QCursor
from PyQt5.QtCore import Qt, QPointF


class Port(QGraphicsEllipseItem):
    """ 端口类 (用于连接的接口) """
    def __init__(self, parent, x_offset, y_offset, is_output=False):
        super(Port, self).__init__(-5, -5, 10, 10, parent)
        self.setBrush(QBrush(Qt.blue if is_output else Qt.red))
        self.setPen(QPen(Qt.black, 1))
        self.setZValue(2)  # 让端口显示在前面
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        # 记录端口类型 (输入 / 输出)
        self.is_output = is_output
        self.edges = []  # 存储连接的边

        # 设置端口位置 (相对父节点)
        self.setPos(x_offset, y_offset)

    def itemChange(self, change, value):
        """ 当端口移动时，更新连接的边 """
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            for edge in self.edges:
                edge.update_path()
        return super(Port, self).itemChange(change, value)


class Edge(QGraphicsPathItem):
    """ 连接线 (贝塞尔曲线) """
    def __init__(self, start_port, end_port=None):
        super(Edge, self).__init__()
        self.setZValue(1)  # 显示在节点后面
        self.setPen(QPen(Qt.black, 2))

        self.start_port = start_port
        self.end_port = end_port
        start_port.edges.append(self)
        if end_port:
            end_port.edges.append(self)

        self.update_path()

    def update_path(self):
        """ 更新曲线路径 """
        start = self.start_port.scenePos()
        if self.end_port:
            end = self.end_port.scenePos()
        else:
            end = self.mapToParent(QCursor.pos())

        path = QPainterPath()
        path.moveTo(start)

        # 使用贝塞尔曲线，控制点在中间位置
        dx = (end.x() - start.x()) * 0.5
        path.cubicTo(start.x() + dx, start.y(), end.x() - dx, end.y(), end.x(), end.y())

        self.setPath(path)

    def set_end_port(self, end_port):
        """ 绑定终点端口 """
        self.end_port = end_port
        end_port.edges.append(self)
        self.update_path()


class Node(QGraphicsRectItem):
    """ 节点类 (包含多个端口) """
    def __init__(self, x, y, width=100, height=60):
        super(Node, self).__init__(0, 0, width, height)
        self.setBrush(QBrush(Qt.lightGray))
        self.setPen(QPen(Qt.black, 2))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        self.setPos(x, y)

        # 创建端口 (输入 / 输出)
        self.inputs = [Port(self, -5, height // 2, is_output=False)]
        self.outputs = [Port(self, width + 5, height // 2, is_output=True)]


class NodeGraphView(QGraphicsView):
    """ 节点图视图 (支持连接) """
    def __init__(self):
        super(NodeGraphView, self).__init__()
        self.setRenderHint(QPainter.Antialiasing)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 记录当前连接状态
        self.dragging_edge = None
        self.start_port = None

    def mousePressEvent(self, event):
        """ 鼠标按下事件 (创建连接) """
        item = self.itemAt(event.pos())
        if isinstance(item, Port):
            self.start_port = item
            self.dragging_edge = Edge(self.start_port)
            self.scene.addItem(self.dragging_edge)
        else:
            super(NodeGraphView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ 鼠标拖拽事件 (更新连接线) """
        if self.dragging_edge:
            self.dragging_edge.update_path()
        else:
            super(NodeGraphView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """ 鼠标释放事件 (完成连接) """
        if self.dragging_edge:
            item = self.itemAt(event.pos())
            if isinstance(item, Port) and item.is_output != self.start_port.is_output:
                self.dragging_edge.set_end_port(item)
            else:
                self.scene.removeItem(self.dragging_edge)
            self.dragging_edge = None
            self.start_port = None
        else:
            super(NodeGraphView, self).mouseReleaseEvent(event)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    view = NodeGraphView()
    view.setSceneRect(-200, -200, 600, 400)

    # 添加节点
    node1 = Node(0, 0)
    node2 = Node(200, 50)
    view.scene.addItem(node1)
    view.scene.addItem(node2)

    view.show()
    sys.exit(app.exec_())
