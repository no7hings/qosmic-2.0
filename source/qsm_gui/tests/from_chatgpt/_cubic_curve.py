# coding:utf-8
import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPainterPath, QPen
from PyQt5.QtCore import Qt, QPointF

class CurveWindow(QMainWindow):
    def __init__(self, coord_list, mode="spline", handle_length=50):
        super(CurveWindow, self).__init__()
        self.coord_list = coord_list
        self.mode = mode  # "spline" 或 "linear"
        self.handle_length = handle_length  # 固定手柄长度
        self.setWindowTitle("PyQt5 绘制曲线")
        self.setGeometry(100, 100, 800, 600)

    def paintEvent(self, event):
        if not self.coord_list:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 获取窗口宽高
        window_width = self.width()
        window_height = self.height()

        # 提取所有坐标点
        x_values = [point["coord"][0] for point in self.coord_list]
        y_values = [point["coord"][1] for point in self.coord_list]

        # 计算坐标范围
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        # 防止除零
        x_range = max(x_max - x_min, 1e-5)
        y_range = max(y_max - y_min, 1e-5)

        # 计算缩放比例
        margin = 20
        x_scale = (window_width - 2 * margin) / x_range
        y_scale = (window_height - 2 * margin) / y_range

        # 缩放并翻转 y 轴
        scaled_points = [
            QPointF(
                margin + (x - x_min) * x_scale,
                window_height - margin - (y - y_min) * y_scale
            )
            for x, y in zip(x_values, y_values)
        ]

        # 绘制曲线
        painter.setPen(QPen(Qt.black, 2))

        if self.mode == "linear":
            self.draw_linear(painter, scaled_points)
        elif self.mode == "spline":
            self.draw_cubic_spline(painter, scaled_points)

    def draw_linear(self, painter, points):
        """绘制线性曲线"""
        path = QPainterPath()
        path.moveTo(points[0])
        for point in points[1:]:
            path.lineTo(point)
        painter.drawPath(path)

    def draw_cubic_spline(self, painter, points):
        """使用 cubicTo 绘制固定手柄长度的三次贝塞尔曲线"""
        if len(points) < 2:
            return

        path = QPainterPath()
        path.moveTo(points[0])

        for i in range(1, len(points) - 1):
            # 当前点
            prev_point = points[i - 1]
            current_point = points[i]
            next_point = points[i + 1]

            # 计算控制点
            control_point1 = self.calculate_control_point(current_point, prev_point, -self.handle_length)
            control_point2 = self.calculate_control_point(current_point, next_point, self.handle_length)

            # 添加贝塞尔曲线
            path.cubicTo(control_point1, control_point2, next_point)

        painter.drawPath(path)

    def calculate_control_point(self, origin, target, length):
        """根据方向计算固定长度的控制点"""
        dx = target.x() - origin.x()
        dy = target.y() - origin.y()
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # 防止零距离
        if distance == 0:
            return origin

        # 归一化并乘以固定长度
        scale = length / distance
        return QPointF(origin.x() + dx * scale, origin.y() + dy * scale)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 坐标列表
    coord_list = [{"coord": (0, 0)}, {"coord": (1, 1)}, {"coord": (2, 0)}, {"coord": (3, 1)}, {"coord": (4, 0)}]

    # 显示窗口（切换模式为 "linear" 或 "spline"）
    mode = "spline"  # 选择 "spline" 或 "linear"
    handle_length = 50  # 手柄固定长度
    window = CurveWindow(coord_list, mode, handle_length)
    window.show()

    sys.exit(app.exec_())
