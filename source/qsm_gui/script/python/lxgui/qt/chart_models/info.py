# coding:utf-8
from ..core.wrap import *

from .. import core as _qt_core

from . import base as _base


class ChartModelForInfo(object):
    def __init__(self):
        self._count = 0
        self._branches = []

        self._rect = qt_rect()

        self._font = _qt_core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

        self._leaf_h = 20

    def set_data(self, data):
        self._branches = []
        for k, v in data.items():
            if not v:
                continue
            i_branch = _base._Data(
                text=k,
                rect=qt_rect(),
                text_rect=qt_rect(),
                leafs=[]
            )
            if isinstance(v, (tuple, list)):
                i_texts = v
            else:
                i_texts = [v]

            for j_text in i_texts:
                j_leaf = _base._Data(
                    text=j_text,
                    text_rect=qt_rect()
                )
                i_branch.leafs.append(j_leaf)

            self._branches.append(i_branch)

    def update(self, x, y, w, h):
        key_w = self.compute_key_width()
        value_w = self.compute_value_width()
        mrg = 2
        spc = 2
        d_h = self._leaf_h
        c_w, c_h = key_w+value_w, self.compute_height()
        c_x, c_y = x+w-c_w-mrg, y+h-c_h-mrg
        self._rect.setRect(
            c_x, c_y, c_w, c_h
        )
        for i_branch in self._branches:
            i_branch.rect.setRect(
                c_x, c_y, c_w, d_h
            )
            i_branch.text_rect.setRect(
                c_x, c_y, key_w-spc/2, d_h
            )
            for j_leaf in i_branch.leafs:
                j_leaf.text_rect.setRect(
                    c_x+key_w+spc, c_y, value_w-spc/2, d_h
                )
                c_y += d_h

    def draw(self, painter):
        painter.setFont(
            self._font
        )
        painter.setPen(
            QtGui.QColor(15, 15, 15, 127)
        )
        painter.setBrush(
            QtGui.QBrush(QtGui.QColor(15, 15, 15, 127))
        )
        painter.drawRoundedRect(
            self._rect, 2, 2, QtCore.Qt.AbsoluteSize
        )
        for i_branch in self._branches:
            painter.setPen(
                QtGui.QColor(223, 223, 223)
            )
            painter.drawText(
                i_branch.text_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, '{}:'.format(i_branch.text)
            )
            for j_leaf in i_branch.leafs:
                painter.drawText(
                    j_leaf.text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, j_leaf.text
                )

    def compute_text_width_by(self, text):
        return self._font_metrics.width(text)+16

    def compute_key_width(self):
        return max(
            self.compute_text_width_by(x.text) for x in self._branches
        )

    def compute_height(self):
        count = len([y for x in self._branches for y in x.leafs])
        return count*self._leaf_h

    def compute_value_width(self):
        return max(
            self.compute_text_width_by(y.text) for x in self._branches for y in x.leafs
        )


