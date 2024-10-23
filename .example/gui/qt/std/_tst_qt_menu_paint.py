# coding:utf-8
import lxgui.qt.core as qt_core

from PyQt5.QtWidgets import QMenu, QStyleOptionMenuItem, QStyle, QApplication, QAction, QMainWindow
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QRect, QSize


class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super(CustomMenu, self).__init__(parent)

        self.setPalette(qt_core.GuiQtDcc.generate_qt_palette())
        self.setAutoFillBackground(True)
        #
        self.setFont(qt_core.QtFonts.NameNormal)

        self.item_height = 22

    def paintEvent(self, event):
        # 创建绘制对象
        painter = QPainter(self)

        # 遍历所有的 menu item 并逐个绘制
        for action in self.actions():
            if action.isVisible():
                opt = QStyleOptionMenuItem()
                # opt.initFrom(self)
                self.initStyleOption(opt, action)
                opt.rect = self.actionGeometry(action)

                self._draw_item_(painter, opt)

    @classmethod
    def _draw_item_(cls, painter, option):
        painter.save()
        # print option.rect
        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()
        frame_rect = QRect(x+1, y+1, w-2, h-2)
        if option.state & QStyle.State_Selected:
            painter.fillRect(frame_rect, Qt.blue)
        # else:
        #     painter.fillRect(frame_rect, Qt.white)

        painter.setPen(Qt.white if option.state & QStyle.State_Selected else Qt.black)
        painter.drawText(frame_rect, Qt.AlignVCenter | Qt.AlignLeft, option.text)
        painter.restore()

    def sizeHint(self):
        width = super(CustomMenu, self).sizeHint().width()
        height = len(self.actions())*self.item_height

        style = self.style()
        panel_margin = style.pixelMetric(QStyle.PM_MenuPanelWidth)
        v_margin = style.pixelMetric(QStyle.PM_MenuVMargin)
        h_margin = style.pixelMetric(QStyle.PM_MenuHMargin)

        total_height = height+2*(v_margin+panel_margin)
        total_width = width+2*(h_margin+panel_margin)

        return QSize(total_width, total_height)

    def actionGeometry(self, action):
        index = self.actions().index(action)
        style = self.style()

        panel_margin = style.pixelMetric(QStyle.PM_MenuPanelWidth)
        v_margin = style.pixelMetric(QStyle.PM_MenuVMargin)
        h_margin = style.pixelMetric(QStyle.PM_MenuHMargin)

        width = self.sizeHint().width()-2*(h_margin+panel_margin)

        return QRect(h_margin+panel_margin, v_margin+panel_margin+index*self.item_height, width, self.item_height)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        menu = CustomMenu(self)
        menu.setTitle('test')
        self.menuBar().addMenu(menu)
        # create icons
        data = [
            ("Absolute", "Ctrl+Alt+C"),
            ("Relative", "Ctrl+Shift+C"),
            ("Copy", "Ctrl+C"),
            ("Absolute", "Ctrl+Alt+C"),
            ("Relative", "Ctrl+Shift+C"),
            ("Copy", "Ctrl+C")
        ]
        for text, shortcut in data:
            action = QAction(self)
            action.setText(text)
            action.setShortcut(shortcut)
            menu.addAction(action)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    _w = MainWindow()
    _w.resize(640, 480)
    _w.show()
    sys.exit(app.exec_())
