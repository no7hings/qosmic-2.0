# coding:utf-8
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QTransform


class CustomGraphicsView(QGraphicsView):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            self.frameSelect()
        else:
            super(CustomGraphicsView, self).keyPressEvent(event)

    def frameSelect(self):
        scene = self.scene()
        if not scene:
            return

        # 获取所有被选中的 item
        selected_items = scene.selectedItems()
        if not selected_items:
            return

        self.frame_select(selected_items)

    def frame_select(self, items):
        """ 选中 items 并自动调整视图 """
        if not items:
            return

        # 计算选中区域的 sceneRect
        selected_rect = self.calculate_bounding_rect(items)
        print(selected_rect)

        # 计算合适的缩放比例
        scale_factor = self.calculate_scale(selected_rect)

        # 应用缩放
        transform = QTransform()
        transform.scale(scale_factor, scale_factor)
        self.setTransform(transform)

        selected_rect = self.calculate_bounding_rect(items)
        print(selected_rect)
        # 计算平移量（先缩放后计算位移）
        dx, dy = self.calculate_translate(selected_rect, scale_factor)
        self.translate(dx, dy)

    def calculate_bounding_rect(self, items):
        """ 计算多个 item 的包围盒 """
        if not items:
            return QRectF()

        bounding_rect = items[0].sceneBoundingRect()
        for item in items[1:]:
            bounding_rect = bounding_rect.united(item.sceneBoundingRect())  # 合并区域

        return bounding_rect

    def calculate_scale(self, scene_rect):
        """ 计算适合的缩放比例 """
        view_rect = self.viewport().rect()  # 获取视图窗口大小

        # 防止零除错误
        if scene_rect.width() == 0 or scene_rect.height() == 0:
            return 1.0

        # 计算 X 和 Y 方向的缩放比例
        scale_x = view_rect.width()/scene_rect.width()
        scale_y = view_rect.height()/scene_rect.height()

        return min(scale_x, scale_y)*0.9  # 预留 10% 边距

    def calculate_translate(self, scene_rect, scale_factor):
        """ 计算适合的平移量，让目标区域居中 """
        view_rect = self.viewport().rect()

        # 计算缩放后的目标区域尺寸
        scaled_width = scene_rect.width()*scale_factor
        scaled_height = scene_rect.height()*scale_factor

        # 计算平移量（确保缩放后仍然居中）
        dx = (view_rect.width()-scaled_width)/2-scene_rect.left()*scale_factor
        dy = (view_rect.height()-scaled_height)/2-scene_rect.top()*scale_factor

        return dx/scale_factor, dy/scale_factor  # 需要缩放后除以 scale_factor


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    # 创建测试矩形
    rect1 = QGraphicsRectItem(0, 0, 100, 100)
    rect1.setBrush(Qt.red)
    rect1.setFlag(QGraphicsRectItem.ItemIsSelectable)

    rect2 = QGraphicsRectItem(200, 200, 100, 100)
    rect2.setBrush(Qt.blue)
    rect2.setFlag(QGraphicsRectItem.ItemIsSelectable)

    scene.addItem(rect1)
    scene.addItem(rect2)

    view = CustomGraphicsView(scene)
    view.setScene(scene)
    view.resize(600, 400)
    view.show()

    sys.exit(app.exec_())
