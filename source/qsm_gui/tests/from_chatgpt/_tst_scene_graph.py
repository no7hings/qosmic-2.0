# coding:utf-8
import sys

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor, QPainter


class NodeItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height, name):
        super(NodeItem, self).__init__(x, y, width, height)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setBrush(QColor(100, 100, 255))
        self.name = name

    def paint(self, painter, option, widget=None):
        super(NodeItem, self).paint(painter, option, widget)
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(self.rect(), Qt.AlignCenter, self.name)


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super(ConnectionLine, self).__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.update_position()

    def update_position(self):
        start_pos = self.start_item.scenePos() + self.start_item.rect().center()
        end_pos = self.end_item.scenePos() + self.end_item.rect().center()
        self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())

    def paint(self, painter, option, widget=None):
        super(ConnectionLine, self).paint(painter, option, widget)
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawLine(self.line())


class NodeGraphView(QGraphicsView):
    def __init__(self, scene):
        super(NodeGraphView, self).__init__(scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setScene(scene)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Node Graph")
        self.setGeometry(100, 100, 800, 600)

        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 800, 600)

        # Create nodes
        node1 = NodeItem(50, 50, 100, 50, "Node 1")
        node2 = NodeItem(300, 150, 100, 50, "Node 2")
        node3 = NodeItem(550, 50, 100, 50, "Node 3")

        # Add nodes to the scene
        scene.addItem(node1)
        scene.addItem(node2)
        scene.addItem(node3)

        # Create connections (lines)
        connection1 = ConnectionLine(node1, node2)
        connection2 = ConnectionLine(node2, node3)

        scene.addItem(connection1)
        scene.addItem(connection2)

        # Create the view
        view = NodeGraphView(scene)
        self.setCentralWidget(view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
