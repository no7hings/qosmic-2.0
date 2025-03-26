# coding:utf-8
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 创建一个中央 Dock 作为 "Central Widget"
        self.central_dock = QDockWidget("Central Dock", self)
        self.central_dock.setWidget(QTextEdit("Main Content"))

        # 允许浮动和移动
        self.central_dock.setFeatures(QDockWidget.AllDockWidgetFeatures)

        # 把中央 Dock 加入窗口
        self.addDockWidget(Qt.TopDockWidgetArea, self.central_dock)  # 默认放在顶部

        # 创建两个普通 Dock
        dock1 = self.create_dock("Dock 1")
        dock2 = self.create_dock("Dock 2")

        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)
        self.addDockWidget(Qt.RightDockWidgetArea, dock2)

        # 允许拖拽后形成田字格
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        # **关键点：禁用 `setCentralWidget()`**
        self.setCentralWidget(None)

        self.setWindowTitle("CentralWidget 也是 Dock")
        self.resize(800, 600)

    def create_dock(self, name):
        """ 创建一个 QDockWidget """
        dock = QDockWidget(name, self)
        dock.setWidget(QTextEdit(name))
        dock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        return dock


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())



