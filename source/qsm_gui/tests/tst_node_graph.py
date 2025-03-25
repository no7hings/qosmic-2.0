# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush, QColor, QPainter


class Node(QGraphicsEllipseItem):
    def __init__(self, x, y, diameter):
        super(Node, self).__init__(0, 0, diameter, diameter)
        self.setBrush(QBrush(QColor(100, 200, 150)))
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.diameter = diameter


class NodeGraphScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(NodeGraphScene, self).__init__(parent)

    def mouseMoveEvent(self, event):
        super(NodeGraphScene, self).mouseMoveEvent(event)
        for item in self.selectedItems():
            print(item)
            if isinstance(item, Node):
                colliding_items = item.collidingItems()
                for colliding_item in colliding_items:
                    if isinstance(colliding_item, Node):
                        # Calculate displacement to avoid collision
                        item_center = item.sceneBoundingRect().center()
                        colliding_center = colliding_item.sceneBoundingRect().center()
                        direction = item_center-colliding_center
                        distance = (direction.x()**2+direction.y()**2)**0.5

                        # If distance is less than the sum of the radii, adjust position
                        if distance < (item.diameter/2+colliding_item.diameter/2):
                            overlap = (item.diameter/2+colliding_item.diameter/2)-distance
                            adjustment = direction/distance*overlap
                            newPos = item.pos()+adjustment
                            item.setPos(newPos)


class NodeGraph(QGraphicsView):
    def __init__(self):
        super(NodeGraph, self).__init__()
        self.scene = NodeGraphScene(self)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 800, 600)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        # Add some nodes to the scene
        node1 = Node(100, 100, 50)
        node2 = Node(200, 200, 50)
        self.scene.addItem(node1)
        self.scene.addItem(node2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NodeGraph()
    window.setWindowTitle('Node Graph with Collision Detection and Avoidance')
    window.show()
    sys.exit(app.exec_())



