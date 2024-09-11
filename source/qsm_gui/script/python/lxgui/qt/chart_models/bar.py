# coding:utf-8
import os

import collections

import math

import lxbasic.core as bsc_core

from ... import core as _gui_core

from ..core.wrap import *

from .. import core as _qt_core

from . import base as _base


class ChartModelForBar(object):
    def __init__(self):
        self._count = 0
        self._branches = []

        self._data_keys = []
        self._data_key_count = 0
        self._active_data_keys = []
        self._active_data_key_count = 0
        self._data_type_dict = {}

        self._value_maximum_dict = {}
        self._value_sum_dict = {}
        self._value_average_dict = {}

        self._branch_sort_key = []

        self._row_h = 16
        self._margin = 2
        self._spacing = 2

        self._name_text = None
        self._name_width_maximum = 240
        self._value_text_width_maximum = 240

        self._font = _qt_core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

        self._normalization_flag = False
        self._height_maximum = 32768

    def set_normalization_flag(self, boolean):
        self._normalization_flag = boolean

    @property
    def font(self):
        return self._font

    def set_name(self, text):
        self._name_text = text

    def compute_branch_coord(self, branch_index, x_offset, y_offset):
        c = self._active_data_key_count
        return (
            x_offset, branch_index*self._row_h*c+y_offset
        )

    def compute_leaf_coord(self, branch_index, leaf_index, x_offset=0, y_offset=0):
        c = self._active_data_key_count
        index = branch_index*c+leaf_index
        return (
            x_offset, index*self._row_h+y_offset
        )

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

        self.sort_branch_by_active()

    def get_active_data_keys(self):
        return self._active_data_keys

    def get_active_data_count(self):
        return self._active_data_key_count

    def set_branch_sort_key(self, key):
        self._branch_sort_key = key
        self.sort_branch_by(self._branch_sort_key)

    def sort_branch_by_active(self):
        if self._active_data_keys:
            self.sort_branch_by(self._active_data_keys[0])

    def set_data(self, data, data_keys, active_data_keys, data_type_dict=None):
        self.set_data_keys(data_keys)
        self._branches = []

        if isinstance(data_type_dict, dict):
            self._data_type_dict = data_type_dict

        value_limit = data.get('VALUE_LIMIT', {})
        for i_idx, (i_k, i_v) in enumerate(data.items()):
            if i_k == 'VALUE_LIMIT':
                continue

            if 'VALUE_LIMIT' in i_v:
                i_value_limit = i_v['VALUE_LIMIT']
            else:
                i_value_limit = value_limit

            self.register_branch(i_idx, i_k, i_v, i_value_limit)

        self._value_maximum_dict = self.compute_value_maximum_dict()
        self._value_sum_dict = self.compute_value_sum_dict()
        self._value_average_dict = self.compute_value_average_dict()

        self.set_active_data_keys(active_data_keys)
        self._count = len(self._branches)

    def generate_info(self):
        dict_ = collections.OrderedDict()
        count = len(self._branches)
        dict_['total'] = bsc_core.BscInteger.to_prettify(
            count, language=_gui_core.GuiUtil.get_language()
        )
        dict_['sum'] = []
        dict_['average'] = []
        for i_data_key in self._active_data_keys:
            i_sum = self._value_sum_dict[i_data_key]
            i_sum_text = bsc_core.BscInteger.to_prettify(
                i_sum, language=_gui_core.GuiUtil.get_language()
            )
            i_average = self._value_average_dict[i_data_key]
            i_average_text = bsc_core.BscInteger.to_prettify(
                i_average, language=_gui_core.GuiUtil.get_language()
            )
            if i_data_key in self._data_type_dict:
                if self._data_type_dict[i_data_key] == 'file_size':
                    i_sum_text = bsc_core.BscInteger.to_prettify_as_file_size(
                        i_sum
                    )
                    i_average_text = bsc_core.BscInteger.to_prettify_as_file_size(
                        i_average
                    )

            dict_['sum'].append(
                '{} is {}'.format(
                    i_data_key, i_sum_text
                )
            )
            dict_['average'].append(
                '{} is {}'.format(
                    i_data_key, i_average_text
                )
            )
        return dict_

    def register_branch(self, index, path, branch_data, value_limit):
        branch = _base._Data(
            leafs={},
            path=path,
            name=bsc_core.BscPath.to_dag_name(path),
            frame_rect=QtCore.QRect(),
            index=index,
            index_text=str(index+1),
            index_rect=QtCore.QRect(),
            name_rect=QtCore.QRect(),
            visible=branch_data.get('visible', True)
        )
        for i_data_key in self._data_keys:
            i_value = branch_data[i_data_key]
            if math.isnan(i_value):
                i_value = 0
                i_value_text = 'N/a'
                i_r, i_g, i_b = 255, 0, 0
            elif math.isinf(i_value):
                i_value = 0
                i_value_text = 'N/a'
                i_r, i_g, i_b = 255, 0, 0
            else:
                i_value_text = bsc_core.BscInteger.to_prettify(
                    i_value, language=_gui_core.GuiUtil.get_language()
                )
                if i_data_key in self._data_type_dict:
                    if self._data_type_dict[i_data_key] == 'file_size':
                        i_value_text = bsc_core.BscInteger.to_prettify_as_file_size(
                            i_value
                        )

                if i_value > 0:
                    i_r, i_g, i_b = bsc_core.BscTextOpt(i_data_key).to_hash_rgb(s_p=(35, 50), v_p=(65, 85))
                else:
                    i_r, i_g, i_b = 127, 127, 127

            # branch[i_data_key] = i_value

            i_leaf = _base._Data(
                frame_rect=QtCore.QRect(),
                value_rect=QtCore.QRect(),
                value_text_rect=QtCore.QRect(),
                value_color=QtGui.QColor(i_r, i_g, i_b),
                name=i_data_key,
                value=i_value,
                value_is_over=False,
            )
            # property for check over limit
            if i_data_key in value_limit:
                i_value_limit = value_limit[i_data_key]
                i_value_text_limit = bsc_core.BscInteger.to_prettify(
                    i_value_limit, language=_gui_core.GuiUtil.get_language()
                )
                if i_data_key in self._data_type_dict:
                    if self._data_type_dict[i_data_key] == 'file_size':
                        i_value_text_limit = bsc_core.BscInteger.to_prettify_as_file_size(
                            i_value_limit
                        )
                if i_value > i_value_limit:
                    i_leaf.value_is_over = True
                    i_leaf['value_limit'] = i_value_limit
                    i_leaf['value_rect_over'] = QtCore.QRect()
                    i_leaf['value_color_over'] = QtGui.QColor(255, 0, 0)
                    i_value_text = '{}(>{})'.format(
                        bsc_core.auto_string(i_value_text), bsc_core.auto_string(i_value_text_limit)
                    )

            i_leaf['value_text'] = i_value_text

            branch.leafs[i_data_key] = i_leaf

        self._branches.append(branch)

    def update(self, x, y, w, h):
        mrg = 2
        spc = 2

        leaf_h = self._row_h

        index_w = self.compute_index_width()
        name_w = self.compute_name_width()

        value_maximum = self.compute_value_maximum()
        value_text_w = self.compute_value_text_width()
        value_w = w-mrg*2-(index_w+spc)-(name_w+spc)-(value_text_w+spc)

        value_text_x, bar_y = x+index_w+name_w+mrg+spc*2, y+mrg
        active_leaf_keys = self.get_active_data_keys()
        active_leaf_key_count = self.get_active_data_count()

        if active_leaf_keys:
            for i_branch_idx, i_branch in enumerate(self.get_branches()):
                i_frm_x, i_frm_y = self.compute_branch_coord(i_branch_idx, value_text_x, bar_y)
                i_frm_h = leaf_h*active_leaf_key_count
                i_index_x = mrg
                i_branch.index = i_branch_idx+1
                i_branch.index_text = str(i_branch_idx+1)
                if i_branch_idx == 2047:
                    print i_frm_y, 'AAA'
                i_branch.index_rect.setRect(i_index_x, i_frm_y, index_w-spc, leaf_h)
                i_name_x = i_index_x+index_w+spc
                i_branch.name_rect.setRect(i_name_x, i_frm_y, name_w, leaf_h)
                i_branch.frame_rect.setRect(x, i_frm_y, w, i_frm_h)
                for j_leaf_index, j_data_key in enumerate(active_leaf_keys):
                    if self._normalization_flag is True:
                        j_value_maximum = self._value_maximum_dict[j_data_key]
                    else:
                        j_value_maximum = value_maximum
                    j_leaf = i_branch.leafs[j_data_key]
                    j_value = j_leaf.value
                    j_value_text_x, j_y = self.compute_leaf_coord(i_branch_idx, j_leaf_index, value_text_x, bar_y)
                    j_value_x = j_value_text_x+value_text_w+spc
                    j_leaf.value_text_rect.setRect(
                        j_value_text_x+1, j_y+2, value_text_w, leaf_h-4
                    )
                    if j_value_maximum > 0:
                        if j_leaf.value_is_over is True:
                            j_value_limit = j_leaf.value_limit
                            j_w = float(j_value_limit)/float(j_value_maximum)*value_w
                            j_leaf.value_rect.setRect(j_value_x, j_y+1, j_w, leaf_h-2)

                            j_bar_w_limit = float(j_value-j_value_limit)/float(j_value_maximum)*value_w
                            j_leaf.value_rect_over.setRect(
                                j_value_x+j_w, j_y+1, j_bar_w_limit, leaf_h-2
                            )
                        else:
                            j_w = float(j_value)/float(j_value_maximum)*value_w
                            j_leaf.value_rect.setRect(j_value_x, j_y+1, j_w, leaf_h-2)
                    else:
                        j_leaf.value_rect.setRect(j_value_x, j_y+1, 1, leaf_h-2)

    def _draw_branches(self, painter, branches):
        active_leaf_keys = self.get_active_data_keys()
        if active_leaf_keys:
            for i_branch_idx, i_branch in enumerate(branches):
                painter.setPen(QtGui.QColor(0, 0, 0, 0))
                if i_branch_idx % 2:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(55, 55, 55)))
                else:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))

                painter.drawRect(i_branch.frame_rect)

                self._draw_branch_index_text(
                    painter, i_branch.index_rect, i_branch.index_text
                )

                self._draw_branch_key_text(
                    painter, i_branch.name_rect, i_branch.name, i_branch.visible
                )

                for j_data_key in active_leaf_keys:
                    j_leaf = i_branch.leafs[j_data_key]

                    painter.setPen(j_leaf.value_color)
                    painter.setBrush(QtGui.QBrush(j_leaf.value_color))
                    painter.drawRect(j_leaf.value_rect)

                    if j_leaf.value_is_over is True:
                        painter.setPen(j_leaf.value_color_over)
                        painter.setBrush(QtGui.QBrush(j_leaf.value_color_over))
                        painter.drawRect(j_leaf.value_rect_over)

                    self._draw_leaf_value_text(
                        painter, j_leaf.value_text_rect, j_leaf.value_text, j_leaf.value_color
                    )

    @classmethod
    def _draw_branch_index_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(127, 127, 127))
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)
    
    @classmethod
    def _draw_branch_key_text(cls, painter, rect, text, visible):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        if visible is True:
            painter.setPen(QtGui.QColor(223, 223, 223))
        else:
            painter.setPen(QtGui.QColor(95, 95, 95))
        painter.drawText(rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_leaf_value_text(cls, painter, rect, text, color):
        painter.setPen(color)
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)

    def generate_pixmap(self, x, y, w, h):
        self.update(x, y, w, h)
        size = QtCore.QSize(w, h)

        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtGui.QColor(63, 63, 63, 255))
        painter = _qt_core.QtPainter(pixmap)
        painter._set_antialiasing_(False)
        painter.setFont(self._font)
        self._draw_branches(painter, self._branches)
        painter.end()
        return pixmap

    def sort_branch_by(self, key, reverse=True):
        self._branches.sort(key=lambda x: x.leafs[key].value, reverse=reverse)

    def get_branches(self):
        return self._branches

    def get_branch_at(self, idx):
        return self._branches[idx]

    def get_data_count(self):
        return self._count

    def get_value_maximum_dict(self):
        return self._value_maximum_dict

    def compute_value_maximum_at(self, key):
        if self._branches:
            return max(x.leafs[key].value for x in self._branches)
        return 0

    def compute_value_maximum_dict(self):
        return {
            k: self.compute_value_maximum_at(k) for k in self._data_keys
        }

    def compute_value_sum_for(self, key):
        if self._branches:
            _ = sum(x.leafs[key].value for x in self._branches)
            if isinstance(_, float):
                return round(_, 2)
            return _
        return 0

    def compute_value_sum_dict(self):
        return {
            k: self.compute_value_sum_for(k) for k in self._data_keys
        }

    def compute_value_average_for(self, key):
        if self._branches:
            values = [x.leafs[key].value for x in self._branches]
            return round(sum(values)/float(len(values)), 2)
        return 0

    def compute_value_average_dict(self):
        return {
            k: self.compute_value_average_for(k) for k in self._data_keys
        }

    def compute_value_maximum(self):
        if self._active_data_keys:
            return max([self.compute_value_maximum_at(x) for x in self._active_data_keys])
        return 0

    def compute_name_width(self):
        if self._branches:
            w = max(self.compute_text_width_by(x.name) for x in self._branches)
            return min(w, self._name_width_maximum)
        return 0

    def compute_value_text_width(self):
        if self._branches:
            w = max(self.compute_value_text_width_for(x) for x in self._branches)
            return min(w, self._value_text_width_maximum)
        return 0

    def compute_value_text_width_for(self, branch):
        leafs = branch.leafs
        if leafs:
            leafs_ = [leafs[x] for x in self._active_data_keys]
            if leafs_:
                return max([self.compute_text_width_by(x.value_text) for x in leafs_])
            return 0
        return 0

    def compute_text_width_by(self, text):
        return self._font_metrics.width(text)+16

    def compute_branch_height(self):
        return self._row_h*self._active_data_key_count

    def compute_index_width(self):
        if self._branches:
            count = len(self._branches)
            return self.compute_text_width_by(str(count))
        return 0

    def compute_height(self):
        if self._branches:
            count = len(self._branches)
            h = self._row_h*count*self._active_data_key_count+self._margin*2
            return min(h, self._height_maximum)
        return 0

    def export(self, directory_path):
        for i_key in self._data_keys:
            self.export_for(directory_path, i_key)

    def export_for(self, directory_path, key):
        file_path = '{}/{}.{}.png'.format(directory_path, self._name_text, key)

        w, h = 1024, self.compute_height()
        
        self.set_active_data_keys([key])
        pixmap = self.generate_pixmap(0, 0, w, h)
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
