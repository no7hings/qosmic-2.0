# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

from ... import core as _gui_core

from ..core.wrap import *

from .. import core as _core

from . import base as _base


class ChartModelForLine(object):
    def __init__(self):
        self._count = 0
        self._branches = []

        self._data_keys = []
        self._data_key_count = 0
        self._active_data_keys = []
        self._active_data_key_count = 0
        self._data_type_dict = {}

        self._value_maximum_dict = {}

        self._branch_name_width_maximum = 240

        self._name_text = None

        self._font = _core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

        self._normalization_flag = False

    def set_normalization_flag(self, boolean):
        self._normalization_flag = boolean

    def set_name(self, text):
        self._name_text = text

    def set_data_keys(self, keys):
        self._data_keys = keys
        self._data_key_count = len(self._data_keys)

    def get_data_keys(self):
        return self._data_keys

    def get_data_key_count(self):
        return self._data_key_count

    def set_active_data_keys(self, keys):
        self._active_data_keys = keys
        self._active_data_key_count = len(self._active_data_keys)

    def get_active_data_keys(self):
        return self._active_data_keys

    def get_active_data_count(self):
        return self._active_data_key_count

    def sort_branch_by(self, key, reverse=True):
        self._branches.sort(key=lambda x: x.leafs[key].value, reverse=reverse)

    def sort_branch_by_active(self):
        if self._active_data_keys:
            self.sort_branch_by(self._active_data_keys[0])

    def set_data(self, data, data_keys, active_data_keys, data_type_dict):
        self.set_data_keys(data_keys)
        self.set_active_data_keys(active_data_keys)

        if isinstance(data_type_dict, dict):
            self._data_type_dict = data_type_dict

        self._branches = []
        for i_idx, (i_k, i_v) in enumerate(data.items()):
            if not i_v:
                continue

            i_branch = _base._Data(
                index=i_idx,
                index_text=str(i_idx+1),
                index_rect=QtCore.QRect(),
                path=i_k,
                name=bsc_core.BscPath.to_dag_name(i_k),
                rect=QtCore.QRect(),
                name_rect=QtCore.QRect(),
                leafs={},
            )
            for j_data_key in self._data_keys:
                j_value = i_v[j_data_key]
                j_value_text = bsc_core.BscInteger.to_prettify(
                    j_value, language=_gui_core.GuiUtil.get_language()
                )

                if j_data_key in self._data_type_dict:
                    if self._data_type_dict[j_data_key] == 'file_size':
                        j_value_text = bsc_core.BscInteger.to_prettify_as_file_size(
                            j_value
                        )

                if j_value == 0:
                    j_r, j_g, j_b = 255, 0, 0
                else:
                    j_r, j_g, j_b = bsc_core.BscTextOpt(j_data_key).to_hash_rgb(s_p=(35, 50), v_p=(65, 85))

                j_leaf = _base._Data(
                    value=j_value,
                    value_text=j_value_text,
                    value_rect=QtCore.QRect(),

                    point_rect=QtCore.QRect(),
                    point_line=QtCore.QLine(),

                    color=QtGui.QColor(j_r, j_g, j_b),
                )
                i_branch.leafs[j_data_key] = j_leaf

            self._branches.append(i_branch)

        self._value_maximum_dict = self.compute_value_maximum_dict()
        self.sort_branch_by_active()
    
    def update(self, x, y, w, h):
        c_x, c_y = x+0, y
        leaf_h = 20
        mrg = 2
        spc = 2
        point_r = 2

        if not self._active_data_keys:
            return

        value_maximum = self.compute_value_maximum()

        branch_index_w = self.compute_branch_index_width()
        branch_name_w = self.compute_branch_name_width()
        branch_w = branch_index_w+branch_name_w-mrg*2
        line_point_dict = {}

        leaf_value_h = self._active_data_key_count*leaf_h

        branch_h = h-leaf_h*3-leaf_value_h

        for i_idx, i_branch in enumerate(self._branches):
            i_branch.index = i_idx+1
            i_branch.index_text = str(i_idx+1)

            i_branch_x = c_x
            i_branch.rect.setRect(
                c_x, c_y, branch_w, h
            )
            i_branch.index_rect.setRect(
                c_x+2, c_y+h-leaf_h, branch_index_w-4, leaf_h
            )
            i_branch.name_rect.setRect(
                c_x+branch_index_w+2, c_y+h-leaf_h, branch_name_w-4, leaf_h
            )

            i_points = []
            for j_leaf_idx, j_data_key in enumerate(self._active_data_keys):
                j_leaf = i_branch.leafs[j_data_key]
                j_leaf_value_x = i_branch_x
                j_leaf_value_y = h-leaf_h-leaf_value_h+(j_leaf_idx*leaf_h)

                j_leaf.value_rect.setRect(
                    j_leaf_value_x, j_leaf_value_y, branch_w, leaf_h
                )

                j_leaf_point_x = i_branch_x+branch_w/2
                j_value = j_leaf.value
                if self._normalization_flag is True:
                    j_value_maximum = self._value_maximum_dict[j_data_key]
                else:
                    j_value_maximum = value_maximum
                if j_value_maximum > 0:
                    j_leaf_point_y = y+branch_h-(float(j_value)/float(j_value_maximum)*branch_h)+leaf_h
                else:
                    j_leaf_point_y = branch_h-leaf_h

                j_leaf.point_rect.setRect(
                    j_leaf_point_x-point_r, j_leaf_point_y-point_r, point_r*2, point_r*2
                )
                i_points.extend([j_leaf_point_x, j_leaf_point_y])
                if j_data_key in line_point_dict:
                    j_leaf_point_x_pre, j_leaf_point_y_pre = line_point_dict[j_data_key]
                else:
                    j_leaf_point_x_pre, j_leaf_point_y_pre = j_leaf_point_x, j_leaf_point_y

                j_leaf.point_line.setLine(j_leaf_point_x_pre, j_leaf_point_y_pre, j_leaf_point_x, j_leaf_point_y)

                line_point_dict[j_data_key] = (j_leaf_point_x, j_leaf_point_y)

            c_x += branch_w+spc

    def compute_value_maximum_dict(self):
        return {
            k: self.compute_value_maximum_at(k) for k in self._data_keys
        }

    def compute_text_width_by(self, text):
        return self._font_metrics.width(text)+16

    def compute_branch_index_width(self):
        if self._branches:
            return max([self.compute_text_width_by(x.index_text) for x in self._branches])
        return 0

    def compute_branch_name_width(self):
        if self._branches:
            w = max([self.compute_text_width_by(x.name) for x in self._branches])
            return min(w, self._branch_name_width_maximum)
        return 0

    def compute_branch_width(self):
        if self._branches:
            return self.compute_branch_index_width()+self.compute_branch_name_width()
        return 0

    def compute_leaf_width(self):
        if self._branches:
            return 0
        return 0

    def compute_width_maximum(self):
        if self._branches:
            return len(self._branches)*self.compute_branch_width()
        return 0
    
    def compute_value_maximum_at(self, key):
        if self._branches:
            return max(x.leafs[key].value for x in self._branches)
        return 0
    
    def compute_value_maximum(self):
        if self._active_data_keys:
            return max([self.compute_value_maximum_at(x) for x in self._active_data_keys])
        return 0

    def compute_value_minimum_at(self, key):
        if self._branches:
            return min(x.leafs[key].value for x in self._branches)
        return 0

    def compute_value_minimum(self):
        if self._active_data_keys:
            return min([self.compute_value_minimum_at(x) for x in self._active_data_keys])
        return 0
    
    def _draw_branches(self, painter, branches):
        for i_branch_idx, i_branch in enumerate(branches):
            painter.setPen(QtGui.QColor(0, 0, 0, 0))
            if i_branch_idx % 2:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(55, 55, 55)))
            else:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))

            painter.drawRect(i_branch.rect)

            self._draw_branch_index_text(painter, i_branch.index_rect, i_branch.index_text)
            self._draw_branch_key_text(painter, i_branch.name_rect, i_branch.name)
            for j_data_key in self._active_data_keys:
                j_leaf = i_branch.leafs[j_data_key]
                self._draw_leaf_value_point(painter, j_leaf.point_rect, j_leaf.point_line, j_leaf.color)
                self._draw_leaf_value_text(painter, j_leaf.value_rect, j_leaf.value_text, j_leaf.color)

    @classmethod
    def _draw_branch_index_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(127, 127, 127))
        painter.drawText(rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_branch_key_text(cls, painter, rect, text):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_value_point(cls, painter, rect, line, color):
        painter.setPen(color)
        painter.setBrush(QtGui.QBrush(color))
        painter.drawRect(rect)
        painter.drawLine(line)

    @classmethod
    def _draw_leaf_value_text(cls, painter, rect, text, color):
        painter.setPen(color)
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)
    
    def generate_pixmap(self, x, y, w, h):
        self.update(x, y, w, h)

        size = QtCore.QSize(w, h)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(63, 63, 63, 255))
        painter = _core.QtPainter(pixmap)
        painter._set_font_(self._font)
        painter._set_antialiasing_(True)
        self._draw_branches(painter, self._branches)
        painter.end()
        return pixmap
