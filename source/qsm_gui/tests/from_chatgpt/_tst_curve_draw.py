# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPainterPath, QPen
from PyQt5.QtCore import Qt

class ComplexPathExample(QMainWindow):
    def __init__(self):
        super(ComplexPathExample, self).__init__()
        self.setWindowTitle("复合路径绘制")
        self.setGeometry(100, 100, 800, 600)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 初始化路径
        path = QPainterPath()

        # 定义路径点
        start_point = (100, 300)  # 起点
        line_end_point = (300, 300)  # 第一段直线的终点
        curve_control_1 = (400, 100)  # 曲线的第一个控制点
        curve_control_2 = (500, 500)  # 曲线的第二个控制点
        curve_end_point = (600, 300)  # 曲线的终点
        final_line_end_point = (700, 300)  # 最后一段直线的终点

        # 绘制第一段直线
        path.moveTo(*start_point)
        path.lineTo(*line_end_point)

        # 绘制第二段曲线（上升的曲线）
        path.cubicTo(curve_control_1[0], curve_control_1[1],
                     curve_control_2[0], curve_control_2[1],
                     curve_end_point[0], curve_end_point[1])

        # 绘制第三段直线
        path.lineTo(final_line_end_point[0], final_line_end_point[1])

        # 绘制路径
        painter.setPen(QPen(Qt.black, 2))
        painter.drawPath(path)

        # 可视化控制点
        painter.setPen(QPen(Qt.red, 3))
        painter.drawEllipse(curve_control_1[0] - 3, curve_control_1[1] - 3, 6, 6)  # 控制点1
        painter.drawEllipse(curve_control_2[0] - 3, curve_control_2[1] - 3, 6, 6)  # 控制点2
        painter.setPen(QPen(Qt.blue, 1, Qt.DashLine))
        painter.drawLine(line_end_point[0], line_end_point[1], curve_control_1[0], curve_control_1[1])  # 起点到控制点1
        painter.drawLine(curve_control_2[0], curve_control_2[1], curve_end_point[0], curve_end_point[1])  # 控制点2到终点

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComplexPathExample()
    window.show()
    sys.exit(app.exec_())
