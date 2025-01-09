# coding:utf-8
from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtGui import QPainter, QColor, QBrush, QPen, QImage, QPixmap
from PySide2.QtSvg import QSvgRenderer


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.color = QColor(255, 0, 0)  # 初始化颜色为红色

        self.renderer = QSvgRenderer('/data/e/myworkspace/td/lynxi/script/python/.resources/icons/arrow_down.svg')  # 加载 SVG 文件
        self.width = self.renderer.defaultSize().width()
        self.height = self.renderer.defaultSize().height()

        self.setFixedSize(self.width, self.height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置画笔和画刷颜色
        painter.setPen(QPen(self.color, 3))
        painter.setBrush(QBrush(self.color))

        # 将 SVG 图像渲染为 QImage 对象
        image = QImage(self.width, self.height, QImage.Format_ARGB32)
        image.fill(0)
        painter = QPainter(image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)  # 设置合成模式
        self.renderer.render(painter)
        painter.end()

        # 将 QImage 对象转换为 QPixmap 对象，并绘制在窗口上
        pixmap = QPixmap.fromImage(image)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, pixmap)

    def setColor(self, color):
        self.color = color
        self.update()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()

    # 改变颜色
    widget.setColor(QColor(0, 255, 0))  # 设置为绿色

    sys.exit(app.exec_())

