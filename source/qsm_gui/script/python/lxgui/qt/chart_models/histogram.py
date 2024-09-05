# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

from ... import core as _gui_core

from ..core.wrap import *

from .. import core as _core

from . import base as _base


class ChartModelForHistogram(object):
    def __init__(self):
        self._count = 0
        self._branches = []

        self._leaf_w = 40
        self._leaf_name_minimum = 40
        self._leaf_name_maximum = 240

        self._branch_width_maximum = 480
        self._branch_width_minimum = 40

        self._leaf_value_width = 40

        self._font = _core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

    def set_data(self, data):
        self._branches = []
        keys = data.keys()
        if keys:
            keys.sort(key=lambda _x: bsc_pinyin.Text.split_any_to_letters(_x))
            for i_k in keys:
                i_v = data[i_k]
                if not i_v:
                    continue

                i_leaf_data = self._to_leaf_data(i_v)
                i_value_total = sum([x[1] for x in i_leaf_data])
                i_value_total_text = bsc_core.BscInteger.to_prettify(i_value_total, i_value_total)
                i_branch = _base._Data(
                    name=i_k,
                    rect=QtCore.QRect(),
                    name_rect=QtCore.QRect(),
                    color=QtGui.QColor(47, 47, 47),
                    value=i_value_total,
                    value_rect=QtCore.QRect(),
                    value_text=i_value_total_text,
                    leafs=[],
                )
                i_percent = 0
                for j_idx, (j_k, j_v) in enumerate(i_leaf_data):
                    j_percent = j_v/float(i_value_total)
                    j_percent_text = '{}%'.format(bsc_core.RawValueMtd.to_percent_prettify(j_v, i_value_total))
                    i_r, i_g, i_b = bsc_core.BscColor.hsv2rgb(
                        360-360*i_percent, .55, .75
                    )
                    j_leaf = _base._Data(
                        index=j_idx,
                        index_text=str(j_idx+1),
                        index_rect=QtCore.QRect(),
                        name=j_k,
                        name_rect=QtCore.QRect(),
                        value=j_v,
                        value_rect=QtCore.QRect(),
                        value_text=bsc_core.BscInteger.to_prettify(
                            j_v, language=_gui_core.GuiUtil.get_language()
                        ),
                        percent=j_percent,
                        percent_rect=QtCore.QRect(),
                        percent_text=j_percent_text,
                        color=QtGui.QColor(i_r, i_g, i_b)
                    )
                    i_branch.leafs.append(j_leaf)

                    i_percent += j_percent

                self._branches.append(i_branch)

    @classmethod
    def _to_leaf_data(cls, data):
        ss = [(k, v) for k, v in data.items()]
        ss.sort(key=lambda x: x[1], reverse=True)
        return ss

    def update(self, x, y, w, h):
        c_x, c_y = x+0, y
        leaf_h = 20
        spc = 2
        for i_branch in self._branches:
            i_branch_w = self.compute_branch_width_for(i_branch)
            i_branch.rect.setRect(
                c_x, c_y, i_branch_w, h
            )
            i_branch.name_rect.setRect(
                c_x, c_y, i_branch_w-self._leaf_value_width, leaf_h
            )
            i_branch.value_rect.setRect(
                c_x+i_branch_w-self._leaf_value_width, c_y, self._leaf_value_width, leaf_h
            )
            i_leaf_index_w = self.compute_leaf_index_width_for(i_branch)
            i_leaf_name_w = self.compute_leaf_name_width_for(i_branch)
            i_leaf_percent_w = self.compute_leaf_percent_width_for(i_branch)
            i_c_name_y = c_y+leaf_h
            i_c_value_y = c_y+leaf_h
            i_value_h = h-leaf_h
            for j_leaf in i_branch.leafs:
                j_leaf.index_rect.setRect(
                    c_x, i_c_name_y, i_leaf_index_w-4, leaf_h
                )
                j_leaf.name_rect.setRect(
                    c_x+i_leaf_index_w, i_c_name_y,
                    i_leaf_name_w-4, leaf_h
                )
                j_leaf.percent_rect.setRect(
                    c_x+i_leaf_index_w+i_leaf_name_w, i_c_name_y,
                    i_leaf_percent_w-4, leaf_h
                )

                j_leaf_value_h = i_value_h*j_leaf.percent
                j_leaf.value_rect.setRect(
                    c_x+i_leaf_index_w+i_leaf_name_w+i_leaf_percent_w, i_c_value_y,
                    self._leaf_value_width, j_leaf_value_h
                )

                i_c_name_y += leaf_h
                i_c_value_y += j_leaf_value_h

            c_x += i_branch_w+spc

    def _draw_branches(self, painter, branches):
        for i_branch_idx, i_branch in enumerate(branches):
            painter.setPen(QtGui.QColor(0, 0, 0, 0))
            if i_branch_idx % 2:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(55, 55, 55)))
            else:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))

            painter.drawRect(i_branch.rect)

            painter.setFont(self._font)
            self._draw_branch_text_(painter, i_branch.name_rect, i_branch.name)
            self._draw_branch_text_(painter, i_branch.value_rect, i_branch.value_text)
            for j_leaf in i_branch.leafs:
                painter.setFont(self._font)
                self._draw_leaf_index_(painter, j_leaf.index_rect, j_leaf.index_text)
                self._draw_leaf_name_(painter, j_leaf.name_rect, j_leaf.name)
                self._draw_leaf_percent_(painter, j_leaf.percent_rect, j_leaf.percent_text, j_leaf.color)

                self._draw_leaf_value_(painter, j_leaf.value_rect, j_leaf.value_text, j_leaf.color)

    @classmethod
    def _draw_branch_text_(cls, painter, rect, text):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_index_(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(127, 127, 127))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_name_(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)
    
    @classmethod
    def _draw_leaf_percent_(cls, painter, rect, text, color):
        painter.setPen(color)
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_value_(cls, painter, rect, text, color):
        painter.setPen(color)
        painter.setBrush(QtGui.QBrush(color))
        painter.drawRect(rect)

        h = rect.height()
        font_size = max(min(h, 12), 2)
        painter.setFont(_core.QtFont.generate_2(size=font_size))

        painter.setPen(QtGui.QColor(31, 31, 31))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    def generate_pixmap(self, x, y, w, h):
        self.update(x, y, w, h)

        size = QtCore.QSize(w, h)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(63, 63, 63, 255))
        painter = _core.QtPainter(pixmap)
        painter._set_font_(self._font)
        painter._set_antialiasing_(False)
        self._draw_branches(painter, self._branches)
        painter.end()
        return pixmap

    def compute_text_width_by(self, text):
        return self._font_metrics.width(text)+16

    def compute_branch_name_width_for(self, branch):
        return self.compute_text_width_by(branch.name)

    def compute_leaf_index_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            return max([self.compute_text_width_by(x.index_text) for x in branch.leafs])
        return 0

    def compute_leaf_name_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            return max([self.compute_text_width_by(x.name) for x in branch.leafs])
        return 0

    def compute_leaf_percent_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            return max([self.compute_text_width_by(x.percent_text) for x in branch.leafs])
        return 0

    def compute_branch_width_for(self, branch):
        branch_name_width = self.compute_branch_name_width_for(branch)
        leaf_index_width = self.compute_leaf_index_width_for(branch)
        leaf_name_width = self.compute_leaf_name_width_for(branch)
        leaf_percent_width = self.compute_leaf_percent_width_for(branch)
        leaf_width = leaf_index_width+leaf_name_width+leaf_percent_width+self._leaf_value_width
        w = max(branch_name_width, leaf_width)
        return max(min(w, self._branch_width_maximum), self._branch_width_minimum)

    def compute_width_maximum(self):
        return sum([self.compute_branch_width_for(x) for x in self._branches])
