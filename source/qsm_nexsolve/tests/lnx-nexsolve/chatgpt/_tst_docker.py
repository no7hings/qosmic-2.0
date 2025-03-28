# coding:utf-8
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("PyQt5 DockWidget 田字格布局")
        self.setGeometry(100, 100, 800, 600)

        # 创建主窗口中央的编辑区
        central_widget = QTextEdit("中央窗口")
        self.setCentralWidget(central_widget)

        # 创建4个 QDockWidget
        self.create_dock("左上", Qt.LeftDockWidgetArea)
        self.create_dock("右上", Qt.RightDockWidgetArea)
        self.create_dock("左下", Qt.LeftDockWidgetArea, below=True)
        self.create_dock("右下", Qt.RightDockWidgetArea, below=True)

    def create_dock(self, title, position, below=False):
        """创建可停靠窗口"""
        dock = QDockWidget(title, self)
        dock.setWidget(QTextEdit(title))  # 内部放置文本框
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)  # 允许拖拽到任何区域

        # 默认停靠
        self.addDockWidget(position, dock)

        # 如果是下方窗口，放置在上方窗口下方
        if below:
            self.splitDockWidget(self.findChildren(QDockWidget)[-2], dock, Qt.Vertical)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



