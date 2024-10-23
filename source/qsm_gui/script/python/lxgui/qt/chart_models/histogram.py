# coding:utf-8
import os

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

from ... import core as _gui_core

from ..core.wrap import *

from .. import core as _qt_core

from . import base as _base


class ChartModelForHistogram(object):
    def __init__(self):
        self._count = 0
        self._branches = []

        self._row_h = 16

        self._leaf_w = 40
        self._leaf_key_minimum = 40
        self._leaf_key_maximum = 240

        self._branch_w_maximum = 480
        self._branch_w_minimum = 40

        self._leaf_value_frame_w = 40

        self._font = _qt_core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

        self._width_maximum = 32768

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
                    rect=QtCore.QRect(),
                    key_text=i_k,
                    key_text_rect=QtCore.QRect(),
                    color=QtGui.QColor(47, 47, 47),
                    value=i_value_total,
                    value_text_rect=QtCore.QRect(),
                    value_text=i_value_total_text,
                    leafs=[],
                )
                i_percent_pre = 0
                j_key_pre = None
                for j_idx, (j_k, j_v) in enumerate(i_leaf_data):
                    j_percent = j_v/float(i_value_total)
                    j_percent_text = '{}%'.format(
                        bsc_core.BscValue.to_percent_prettify(j_v, i_value_total, 4)
                    )
                    i_r_0, i_g_0, i_b_0 = bsc_core.BscColor.hsv2rgb(
                        360-180*i_percent_pre, .55, .75
                    )
                    j_percent_cur = i_percent_pre+j_percent
                    i_r_1, i_g_1, i_b_1 = bsc_core.BscColor.hsv2rgb(
                        360-180*j_percent_cur, .55, .75
                    )
                    if j_key_pre is None:
                        j_r_0, j_g_0, j_b_0 = bsc_core.BscTextOpt(j_k).to_hash_rgb(s_p=(35, 50), v_p=(65, 85))
                        j_r_1, j_g_1, j_b_1 = j_r_0, j_g_0, j_b_0
                    else:
                        j_r_0, j_g_0, j_b_0 = bsc_core.BscTextOpt(j_k).to_hash_rgb(s_p=(35, 50), v_p=(65, 85))
                        j_r_1, j_g_1, j_b_1 = bsc_core.BscTextOpt(j_k).to_hash_rgb(s_p=(35, 50), v_p=(65, 85))

                    j_leaf = _base._Data(
                        index=j_idx,
                        index_text=str(j_idx+1),
                        index_rect=QtCore.QRect(),
                        
                        key_text=j_k,
                        key_text_rect=QtCore.QRect(),
                        
                        value=j_v,
                        value_text=bsc_core.BscInteger.to_prettify(
                            j_v, language=_gui_core.GuiUtil.get_language()
                        ),
                        value_text_rect=QtCore.QRect(),
                        
                        percent=j_percent,
                        percent_text_rect=QtCore.QRect(),
                        percent_text=j_percent_text,
                        
                        value_frame_rect=QtCore.QRect(),
                        
                        # color_0=QtGui.QColor(i_r_0, i_g_0, i_b_0),
                        # color=QtGui.QColor(i_r_1, i_g_1, i_b_1),

                        color_0=QtGui.QColor(j_r_0, j_g_0, j_b_0),
                        color=QtGui.QColor(j_r_1, j_g_1, j_b_1),
                        color_gradient=QtGui.QLinearGradient()
                    )
                    i_branch.leafs.append(j_leaf)

                    i_percent_pre += j_percent

                    j_key_pre = j_k

                self._branches.append(i_branch)

    @classmethod
    def _to_leaf_data(cls, data):
        ss = [(k, v) for k, v in data.items()]
        ss.sort(key=lambda x: x[1], reverse=True)
        return ss

    def update(self, x, y, w, h):
        c_x, c_y = x+0, y
        row_h = self._row_h
        spc = 2
        for i_branch in self._branches:
            i_branch_w = self.compute_branch_width_for(i_branch)
            i_branch.rect.setRect(
                c_x, c_y, i_branch_w, h
            )
            i_branch.key_text_rect.setRect(
                c_x, c_y, i_branch_w-self._leaf_value_frame_w, row_h
            )
            i_branch.value_text_rect.setRect(
                c_x+i_branch_w-self._leaf_value_frame_w, c_y, self._leaf_value_frame_w, row_h
            )
            i_leaf_index_w = self.compute_leaf_index_width_for(i_branch)
            i_leaf_key_w = self.compute_leaf_key_width_for(i_branch)
            i_leaf_value_w = self.compute_leaf_value_width_for(i_branch)
            i_leaf_percent_w = self.compute_leaf_percent_width_for(i_branch)

            i_c_leaf_key_y = c_y+row_h
            i_c_leaf_value_y = c_y+row_h
            i_value_h = h-row_h

            for j_leaf in i_branch.leafs:
                j_leaf.index_rect.setRect(
                    c_x, i_c_leaf_key_y, i_leaf_index_w-4, row_h
                )
                j_leaf.key_text_rect.setRect(
                    c_x+i_leaf_index_w, i_c_leaf_key_y,
                    i_leaf_key_w-4, row_h
                )
                j_leaf.value_text_rect.setRect(
                    c_x+i_leaf_index_w+i_leaf_key_w, i_c_leaf_key_y,
                    i_leaf_value_w-4, row_h
                )
                j_leaf.percent_text_rect.setRect(
                    c_x+i_leaf_index_w+i_leaf_key_w+i_leaf_value_w, i_c_leaf_key_y,
                    i_leaf_percent_w-4, row_h
                )

                j_leaf_value_h = int(i_value_h*j_leaf.percent)
                j_leaf.value_frame_rect.setRect(
                    c_x+i_leaf_index_w+i_leaf_key_w+i_leaf_value_w+i_leaf_percent_w, i_c_leaf_value_y,
                    self._leaf_value_frame_w, j_leaf_value_h
                )
                j_color_gradient = j_leaf.color_gradient
                j_color_gradient.setStart(j_leaf.value_frame_rect.topLeft())
                j_color_gradient.setFinalStop(j_leaf.value_frame_rect.bottomLeft())

                j_color_gradient.setColorAt(0, j_leaf.color_0)
                j_color_gradient.setColorAt(0.05, j_leaf.color_0)
                j_color_gradient.setColorAt(0.95, j_leaf.color)
                j_color_gradient.setColorAt(1, j_leaf.color)

                i_c_leaf_key_y += row_h
                i_c_leaf_value_y += j_leaf_value_h

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
            self._draw_branch_text_(painter, i_branch.key_text_rect, i_branch.key_text)
            self._draw_branch_text_(painter, i_branch.value_text_rect, i_branch.value_text)
            for j_leaf in i_branch.leafs:
                painter.setFont(self._font)
                self._draw_leaf_index_text(painter, j_leaf.index_rect, j_leaf.index_text)
                self._draw_leaf_key_text(painter, j_leaf.key_text_rect, j_leaf.key_text)
                self._draw_leaf_percent_text(painter, j_leaf.percent_text_rect, j_leaf.percent_text, j_leaf.color_0)
                self._draw_leaf_value_text_0(painter, j_leaf.value_text_rect, j_leaf.value_text)

                self._draw_leaf_value_rect(painter, j_leaf.value_frame_rect, j_leaf.color_gradient)
                self._draw_leaf_value_text_1(painter, j_leaf.value_frame_rect, j_leaf.value_text)

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
    def _draw_leaf_index_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(127, 127, 127))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_key_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)
    
    @classmethod
    def _draw_leaf_percent_text(cls, painter, rect, text, color):
        painter.setPen(color)
        painter.drawText(rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_value_text_0(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_value_rect(cls, painter, rect, color):
        painter.setPen(QtGui.QColor(127, 127, 127))
        painter.setBrush(QtGui.QBrush(color))
        painter.drawRect(rect)

    @classmethod
    def _draw_leaf_value_text_1(cls, painter, rect, text):
        h = rect.height()
        font_size = max(min(h, 12), 2)
        painter.setFont(_qt_core.QtFont.generate_2(size=font_size))

        painter.setPen(QtGui.QColor(31, 31, 31))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    def generate_pixmap(self, x, y, w, h):
        self.update(x, y, w, h)

        size = QtCore.QSize(w, h)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(63, 63, 63, 255))
        painter = _qt_core.QtPainter(pixmap)
        painter._set_font_(self._font)
        painter._set_antialiasing_(False)
        self._draw_branches(painter, self._branches)
        painter.end()
        return pixmap

    def compute_text_width_by(self, text):
        return self._font_metrics.width(text)+16

    def compute_branch_key_width_for(self, branch):
        return self.compute_text_width_by(branch.key_text)
    
    def compute_branch_value_width_for(self, branch):
        return self.compute_text_width_by(branch.value_text)

    def compute_leaf_index_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            return max([self.compute_text_width_by(x.index_text) for x in branch.leafs])
        return 0

    def compute_leaf_key_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            return max([self.compute_text_width_by(x.key_text) for x in branch.leafs])
        return 0

    def compute_leaf_value_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            return max([self.compute_text_width_by(x.value_text) for x in branch.leafs])
        return 0

    def compute_leaf_percent_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            return max([self.compute_text_width_by(x.percent_text) for x in branch.leafs])
        return 0

    def compute_branch_width_for(self, branch):
        branch_key_w = self.compute_branch_key_width_for(branch)
        branch_value_w = self.compute_branch_value_width_for(branch)
        branch_w = branch_key_w+branch_value_w

        leaf_index_w = self.compute_leaf_index_width_for(branch)
        leaf_key_w = self.compute_leaf_key_width_for(branch)
        leaf_value_w = self.compute_leaf_value_width_for(branch)
        leaf_percent_w = self.compute_leaf_percent_width_for(branch)
        leaf_w = leaf_index_w+leaf_key_w+leaf_value_w+leaf_percent_w+self._leaf_value_frame_w
        w = max(branch_w, leaf_w)
        return max(min(w, self._branch_w_maximum), self._branch_w_minimum)

    def compute_width(self):
        if self._branches:
            w = sum([self.compute_branch_width_for(x) for x in self._branches])
            return min(w, self._width_maximum)
        return 0

    def export(self, file_path):
        width = self.compute_width()

        pixmap = self.generate_pixmap(0, 0, width, 1024)
        ext = os.path.splitext(file_path)[-1]
        if ext:
            if ext.lower() not in ['.png', '.jpg', '.jpeg']:
                format_ = 'PNG'
            else:
                format_ = str(ext[1:]).upper()
        else:
            format_ = 'PNG'

        pixmap.save(
            file_path,
            format_
        )
