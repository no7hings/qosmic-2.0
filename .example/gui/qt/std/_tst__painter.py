# coding:utf-8
import sys

from lxgui.qt.core.wrap import *


class W(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        contents_y = self.edit.verticalScrollBar().value()
        page_bottom = contents_y + self.edit.viewport().height()
        font_metrics = self.fontMetrics()
        current_block = self.edit.document().findBlock(self.edit.textCursor().position())
        painter = QtGui.QPainter(self)
        line_count = 0
        block = self.edit.document().begin()
        while block.isValid():
            line_count += 1
            position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()
            if position.y() > page_bottom:
                break
            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
                self.current = line_count
            painter.drawText(
                self.width() - font_metrics.width(str(line_count)) - 10,
                round(position.y()) - contents_y + font_metrics.ascent(),
                str(line_count),
            )
            if bold:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)
            block = block.next()
        self.highest_line = line_count
        painter.end()
        # QWidget.paintEvent(self, event)


app = QtWidgets.QApplication(sys.argv)

w = W()

w.setBaseSize(480, 480)
w.show()

sys.exit(app.exec_())
