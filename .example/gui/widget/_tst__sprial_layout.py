# coding:utf-8
import time

import random

from lxgui.qt.core.wrap import *

import lxgui.qt.widgets as qt_widgets

import lxbasic.core as bsc_core


class W(qt_widgets.QtMainWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        wgt = qt_widgets.QtTranslucentWidget()
        self.setCentralWidget(wgt)
        lot = qt_widgets.QtVBoxLayout(wgt)
        # lot._set_align_as_top_()

        button = qt_widgets.QtPressButton()
        lot.addWidget(button)
        button._set_name_text_('Test')
        button.press_clicked.connect(self.refresh)

        self.__seed = 0

        self.test()

    def refresh(self):
        self.__seed += 1
        print self.__seed
        self.test()

    def test(self):
        # self._o = bsc_core.RectLayoutOpt(
        #     [(0, 0, choice(range(25, 100)), choice(range(25, 100))) for i in range(100)]
        # )
        random.seed(self.__seed)
        sizes = range(5, 200)
        a = [(0, 0, random.choice(sizes), random.choice(sizes)) for i in range(25)]

        # a = [
        #     (0, 0, 67.52923583984375, 58.419891357421875),
        #     (0, 0, 53.3314208984375, 64.176513671875),
        #     (0, 0, 78.4378662109375, 75.01416015625),
        #     (0, 0, 72.9327392578125, 73.950927734375),
        #     (0, 0, 24.1031494140625, 23.918701171875),
        #     (0, 0, 20.067276000976562, 19.309814453125)
        # ]

        # a = [
        #     (4, 4, 149, 149),
        #     (4, 153, 15, 148),
        #     (19, 153, 46, 132),
        #     (19, 285, 45, 11),
        #     (19, 296, 24, 3),
        #     (43, 153, 66, 126)
        # ]

        # a = [
        #     (0, 0, 200, 201),
        #     (0, 0, 201, 100),
        #     (0, 0, 50, 50),
        #     (0, 0, 25, 25),
        #     (0, 0, 30, 30),
        # ]

        # a = [
        #     (0, 0, 200, 100),
        #     (0, 0, 100, 100),
        #     (0, 0, 50, 100),
        #     (0, 0, 50, 50),
        #     (0, 0, 25, 12.5),
        #     (0, 0, 12.5, 12.5),
        #     (0, 0, 12.5, 12.5),
        #     (0, 0, 12.5, 12.5),
        #     (0, 0, 12.5, 12.5),
        # ]

        # a = [
        #     (0, 0, 200, 200),
        #     (0, 0, 100, 100),
        #     (0, 0, 100, 100),
        #     (0, 0, 25, 25),
        #     (0, 0, 25, 25),
        # ]

        # a = [
        #     (0, 0, 200, 200),
        #     (0, 0, 100, 100),
        #     (0, 0, 50, 50),
        #     (0, 0, 50, 50),
        #     (0, 0, 30, 30),
        #     (0, 0, 20, 25),
        #     (0, 0, 40, 25),
        #     (0, 0, 30, 30),
        #     (0, 0, 30, 30),
        #     (0, 0, 30, 25),
        #     (0, 0, 25, 25),
        #     # (0, 0, 12.5, 12.5),
        #     # (0, 0, 25, 25),
        #     # (0, 0, 25, 25),
        # ]

        # a = [
        #     (0, 0, 150, 200),
        #     (0, 0, 100, 100),
        #     (0, 0, 100, 50),
        #     (0, 0, 50, 50),
        #     # (0, 0, 50, 50),
        #     # (0, 0, 25, 25),
        #     # (0, 0, 25, 25),
        #     # (0, 0, 30, 30),
        #     # (0, 0, 12.5, 12.5),
        #     # (0, 0, 25, 25),
        #     # (0, 0, 30, 30),
        #     # (0, 0, 30, 30),
        # ]

        # a = [
        #     (0, 0, 200, 200),
        #     (0, 0, 200, 100),
        #     (0, 0, 100, 200),
        # ]

        # a = [
        #     (0, 0, 200, 300),
        #     (0, 0, 200, 100),
        #     (0, 0, 100, 200),
        # ]
        self._o = bsc_core.RectLayoutOpt(
            a, spacing=8
        )
        # self._o.center = 4, 4

        self._rects = self._o.generate()

        self.update()

    def paintEvent(self, event):
        painter = qt_widgets.QtGui.QPainter(self)

        c_o = bsc_core.RawColorChoiceOpt()

        rects = self._rects
        print 'draw {} rects'.format(len(rects))
        rect_cur = None
        for i_idx, i_rect in enumerate(rects):
            # print i_rect.args

            i_s = min(i_rect.w, i_rect.h)
            i_rect_ = i_rect.exact_rect
            i_q_rect = QtCore.QRect(i_rect_.x+1, i_rect_.y+1, i_rect_.w-2, i_rect_.h-2)

            i_rgb = c_o.generate()
            i_color = QtGui.QColor(*i_rgb)
            painter.setPen(QtGui.QColor(0, 0, 0, 0))
            painter.setBrush(QtGui.QBrush(i_color))
            painter.drawRect(
                i_q_rect
            )
            painter.setPen(QtGui.QColor(255, 255, 255, 255))
            f = QtGui.QFont()
            f.setPixelSize(max(1, int(i_s/2)))
            painter.setFont(f)
            painter.drawText(
                i_q_rect,
                QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                str(i_rect.index)
            )

            rect_cur = i_rect

            # if i_idx == 5:
            #     break

        if rect_cur is not None:
            space_rect = rect_cur.space
            if space_rect is not None:
                q_space_rect = QtCore.QRect(space_rect.x+1, space_rect.y+1, space_rect.w-2, space_rect.h-2)
                painter.setPen(QtGui.QColor(0, 255, 0, 255))
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
                painter.drawRect(
                    q_space_rect
                )

                piece_parent = space_rect.parent
                if piece_parent is not None:
                    qt_space_rect_parent = QtCore.QRect(*piece_parent.args)
                    painter.setPen(QtGui.QColor(0, 0, 255, 255))
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
                    painter.drawRect(qt_space_rect_parent)

                area_rect = space_rect.area
                if area_rect.get_is_valid() is True:
                    q_area_rect = QtCore.QRect(area_rect.x-1, area_rect.y-1, area_rect.w+2, area_rect.h+2)
                    painter.setPen(QtGui.QColor(0, 0, 0, 255))
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
                    painter.drawRect(q_area_rect)


if __name__ == '__main__':
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    _w = W()
    _w.setFixedSize(1024, 1024)
    _w.show()

    sys.exit(_app.exec_())
