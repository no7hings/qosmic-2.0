# coding=utf-8
import os

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts
# qt widgets
from . import base as _base

from . import utility as _utility

from . import button as _button

from . import container as _container


class QtItemForHistoryEntity(
    _qt_abstracts.AbsQtWidgetBaseDef,
    QtWidgets.QWidget
):
    HEIGHT = 96

    LEFT_WIDTH = 32
    RIGHT_WIDTH = 24
    ICON_WIDTH = 24
    NAME_HEIGHT = 24
    TEXT_HEIGHT = 20

    delete_accepted = qt_signal(object)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        spc = 4

        m_0 = 4
        m_1 = 8
        
        h_name = self.NAME_HEIGHT
        w_left = self.LEFT_WIDTH
        w_right = self.RIGHT_WIDTH

        self._frame_draw_rect.setRect(
            x+m_0, y+m_0, w-m_0*2, h-m_0*2
        )

        self._frame_draw_line_left.setLine(
            x+m_0+w_left, y+m_0+1, x+w_left+m_0, y+h-m_0*2+2
        )
        self._frame_draw_line_right.setLine(
            x+w-m_0-w_right, y+m_0+1, x+w-m_0-w_right, y+h-m_0*2+2
        )

        icon_w = icon_h = self._file_icon_s
        self._storage_icon_draw_rect.setRect(
            x+m_0+(w_left-icon_w)/2, y+(h-icon_w)/2, icon_w, icon_h
        )

        btn_w = btn_h = self._menu_button_s

        txt_m = 8
        info_h = self._info_h

        txt_y = y+m_0
        w_name_max = w-w_left-w_right-txt_m*2

        self._name_draw_rect.setRect(
            x+w_left+m_0+txt_m, y+m_0, w_name_max, h_name
        )
        txt_y += h_name
        info_w_max = w-m_0*2-w_left-txt_m*2

        self._frame_draw_line.setLine(
            x+m_0+w_left, txt_y, x+w-m_0, txt_y
        )

        if self._storage_path is not None:
            txt_w_0 = _qt_core.GuiQtText.get_draw_width(
                self, self._storage_path
            )+4
            txt_w = min(txt_w_0, info_w_max)
            self._storage_path_draw_rect.setRect(
                x+w_left+m_0+txt_m, txt_y, txt_w, info_h
            )
            txt_y += info_h+spc

        if self._associated_entity_id is not None:
            txt_w_0 = _qt_core.GuiQtText.get_draw_width(
                self, self._associated_entity_id
            )+4
            txt_w = min(txt_w_0, info_w_max)
            self._associate_draw_rect.setRect(
                x+w_left+m_0+txt_m, txt_y, txt_w, info_h
            )

        self._menu_button.setGeometry(
            x+w-m_0-w_right+(w_right-btn_w)/2, y+m_0+(h_name-btn_h)/2, btn_w, btn_h
        )

        self._time_draw_rect.setRect(
            x+w_left+m_0+txt_m, h-m_0-info_h, info_w_max, info_h
        )

    def _do_hover_move_(self, event):
        p = event.pos()
        if self._storage_path_draw_rect.contains(p):
            self._storage_hover_flag = True
            if self._check_file_exists_() is True:
                self.setCursor(
                    QtCore.Qt.PointingHandCursor
                )
        elif self._associate_draw_rect.contains(p):
            self._associate_hover_flag = True
            self.setCursor(
                QtCore.Qt.PointingHandCursor
            )
        else:
            self._storage_hover_flag = False
            self._associate_hover_flag = False
            self.unsetCursor()
            # noinspection PyArgumentList
            QtWidgets.QToolTip.hideText()

    def _do_leave_(self):
        self._storage_hover_flag = False
        self.unsetCursor()
        # noinspection PyArgumentList
        QtWidgets.QToolTip.hideText()

    def _do_show_tool_tip_(self, event):
        if self._storage_hover_flag is True:
            css = _qt_core.GuiQtUtil.generate_tool_tip_css(
                self._storage_path,
                action_tip=[
                    '"LMB-click" to open file',
                ]
            )
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _do_open_any_(self, event):
        self._do_open_file_()
        self._do_open_associate_()

    def _do_open_file_(self):
        if self._storage_hover_flag is True:
            self._open_directory_fnc_()

    def _do_open_associate_(self):
        if self._associate_hover_flag is True:
            _qt_core.GuiQtUtil.copy_text_to_clipboard(
                self._associated_entity_id
            )
            if self._open_associate_fnc_ is not None:
                self._open_associate_fnc_()

    def __init__(self, *args, **kwargs):
        super(QtItemForHistoryEntity, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.setMouseTracking(True)

        self.setFixedHeight(self.HEIGHT)

        self._init_widget_base_def_(self)

        self._group_widget = None
        
        self._key_text = None
        self._name_text = None
        self._name_text_draw = None

        self._storage_hover_flag = False
        self._associate_hover_flag = False

        self._tool_tip_flag = False

        self._associated_entity_id = None
        self._time_text = None
        self._open_associate_fnc_ = None

        self._storage_path = None
        self._storage_icon = None

        self._frame_draw_rect = QtCore.QRect()
        
        self._frame_draw_line = QtCore.QLine()
        self._frame_draw_line_left = QtCore.QLine()
        self._frame_draw_line_right = QtCore.QLine()
        
        self._name_draw_rect = QtCore.QRect()
        self._storage_icon_draw_rect = QtCore.QRect()
        self._storage_path_draw_rect = QtCore.QRect()
        self._time_draw_rect = QtCore.QRect()

        self._associate_draw_rect = QtCore.QRect()

        self._file_icon_s = 24
        self._info_h = self.TEXT_HEIGHT

        self._menu_button = _button.QtIconMenuButton(self)
        self._menu_button._set_icon_name_('tab/tab-menu-v')

        if self._get_language_() == 'chs':
            menu_data = [
                ('在文件夹中显示', 'file/open-folder', self._open_directory_fnc_),
                ('移动到回收站', 'trash', self._delete_fnc_)
            ]
        else:
            menu_data = [
                ('Show in folder', 'file/open-folder', self._open_directory_fnc_),
                ('Send to trash', 'trash', self._delete_fnc_)
            ]

        self._menu_button._set_menu_data_(menu_data)

        self._menu_button_s = 20

        self._frame_border_color = _gui_core.GuiRgba.Gray
        self._frame_background_color = _gui_core.GuiRgba.Basic

        self._name_draw_color = _gui_core.GuiRgba.Light
        self._time_color = _gui_core.GuiRgba.DarkGray
        self._name_font = _qt_core.QtFont.generate(
            size=10
        )
        self._time_font = _qt_core.QtFont.generate(
            size=8
        )
        
        self._file_text_color = _gui_core.GuiRgba.LightAzureBlue
        self._file_text_color_lost = _gui_core.GuiRgba.Gray
        self._file_font = _qt_core.QtFont.generate(
            size=8, underline=True
        )
        self._text_font_lost = _qt_core.QtFont.generate(
            size=8, strike_out=True
        )

        self.setFont(self._file_font)

        self.installEventFilter(self)
        self._menu_button.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Leave:
                self._do_leave_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_open_any_(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)
        elif widget == self._menu_button:
            self._do_leave_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)

        painter._set_border_color_(self._frame_border_color)
        painter._set_background_color_(self._frame_background_color)

        border_radius = 6

        painter._set_antialiasing_(True)
        painter._set_border_width_(2)
        painter.drawRoundedRect(
            self._frame_draw_rect,
            border_radius, border_radius,
            QtCore.Qt.AbsoluteSize
        )

        painter._set_antialiasing_(False)

        painter._set_border_color_(self._frame_border_color)
        painter._set_border_width_(1)
        painter.drawLine(
            self._frame_draw_line_left
        )
        painter.drawLine(
            self._frame_draw_line
        )

        painter._set_font_(self._name_font)
        painter._set_text_color_(self._name_draw_color)

        name_text = painter.fontMetrics().elidedText(
            self._name_text,
            QtCore.Qt.ElideMiddle,
            self._name_draw_rect.width()-4,
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._name_draw_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            name_text
        )

        if self._storage_path is not None:
            pxm = self._storage_icon.pixmap(
                self._storage_icon_draw_rect.width(), self._storage_icon_draw_rect.height()
            )
            painter.drawPixmap(
                self._storage_icon_draw_rect, pxm
            )
            # text
            if self._check_file_exists_():
                painter._set_font_(self._file_font)
                painter._set_text_color_(self._file_text_color)
            else:
                painter._set_font_(self._text_font_lost)
                painter._set_text_color_(self._file_text_color_lost)

            text_elided = painter.fontMetrics().elidedText(
                self._storage_path,
                QtCore.Qt.ElideMiddle,
                self._storage_path_draw_rect.width()-4,
                QtCore.Qt.TextShowMnemonic
            )
            # noinspection PyArgumentEqualDefault
            painter.drawText(
                self._storage_path_draw_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                text_elided
            )

        if self._associated_entity_id:
            painter._set_font_(self._file_font)
            painter._set_text_color_(self._name_draw_color)

            text_elided = painter.fontMetrics().elidedText(
                self._associated_entity_id,
                QtCore.Qt.ElideMiddle,
                self._associate_draw_rect.width()-4,
                QtCore.Qt.TextShowMnemonic
            )
            # noinspection PyArgumentEqualDefault
            painter.drawText(
                self._associate_draw_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                text_elided
            )

        if self._time_text:
            painter._set_font_(self._time_font)
            painter._set_text_color_(self._time_color)

            text_elided = painter.fontMetrics().elidedText(
                self._time_text,
                QtCore.Qt.ElideMiddle,
                self._time_draw_rect.width()-4,
                QtCore.Qt.TextShowMnemonic
            )
            # noinspection PyArgumentEqualDefault
            painter.drawText(
                self._time_draw_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
                text_elided
            )

    def _open_directory_fnc_(self):
        if self._storage_path is not None:
            if os.path.isfile(self._storage_path):
                directory_path = os.path.dirname(self._storage_path)
                os.startfile(
                    directory_path
                )
            elif os.path.isdir(self._storage_path):
                os.startfile(
                    self._storage_path
                )

    def _delete_fnc_(self):
        self.close()
        self.deleteLater()

        self.delete_accepted.emit(self)

    def _set_associated_entity_id_(self, path):
        self._associated_entity_id = path

    def _set_open_associate_fnc_(self, fnc):
        self._open_associate_fnc_ = fnc

    def _set_storage_path_(self, path):
        self._storage_path = bsc_core.auto_unicode(path)
        if os.path.isfile(self._storage_path):
            self._storage_icon = _qt_core.GuiQtDcc.generate_qt_file_icon(self._storage_path)
        elif os.path.isdir(self._storage_path):
            self._storage_icon = _qt_core.GuiQtDcc.generate_qt_directory_icon(self._storage_path)
        else:
            self._storage_icon = _qt_core.GuiQtIcon.generate_by_icon_name('file/lost')
    
    def _check_file_exists_(self):
        if self._storage_path is not None:
            return os.path.exists(self._storage_path)
        return False

    def _set_group_widget_(self, widget):
        self._group_widget = widget
    
    def _get_group_widget_(self):
        return self._group_widget

    def _set_key_text_(self, text):
        self._key_text = text

    def _get_key_text_(self):
        return self._key_text
    
    def _set_name_text_(self, text):
        self._name_text = text
        # self._update_name_draw_()

    def _set_time_text_(self, text):
        self._time_text = text
        # self._update_name_draw_()

    def _update_name_draw_(self):
        self._name_text_draw = ' | '.join([x for x in [self._time_text, self._name_text] if x])

    def _connect_delete_to_(self, fnc):
        self.delete_accepted.connect(fnc)


class QtViewForHistoryEntity(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtBusyBaseDef,
):
    item_delete_accepted = qt_signal(str)

    @classmethod
    def _update_by_item_delete_(cls, widget):
        group_widget = widget._get_group_widget_()
        all_widgets = group_widget._get_widgets_()
        # fixme: when emit send, widget is already exists?
        if all_widgets == [widget]:
            group_widget.close()
            group_widget.deleteLater()

    def __init__(self, *args, **kwargs):
        super(QtViewForHistoryEntity, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._init_busy_base_def_(self)

        self._lot = _base.QtVBoxLayout(self)

        self._sca = _utility.QtVScrollArea()
        self._lot.addWidget(self._sca)

        self._layout = self._sca._layout

        self._group_dict = {}
        self._item_dict = {}

    def _prepend_group_(self, text):
        wgt = _container.QtHToolGroupStyleC()
        self._layout.insertWidget(0, wgt)
        wgt._set_name_text_(text)
        wgt._set_expanded_(True)

        self._group_dict[text] = wgt
        return wgt

    def _prepend_item_(self, key_text, group_text, name_text):
        if group_text in self._group_dict:
            group_widget = self._group_dict[group_text]
        else:
            group_widget = self._prepend_group_(group_text)

        wgt = QtItemForHistoryEntity()
        group_widget._prepend_widget_(wgt)
        
        wgt._set_key_text_(key_text)
        wgt._set_name_text_(name_text)
        wgt._set_group_widget_(group_widget)
        
        wgt.delete_accepted.connect(self._update_by_item_delete_)
        return wgt

    def _restore_(self):
        self._group_dict = {}
        self._item_dict = {}
        _qt_core.GuiQtLayout.clear_all_widgets(
            self._layout
        )
