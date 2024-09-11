# coding=utf-8
import collections

import fnmatch

import os

import six

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

from . import entry_frame as _entry_frame


class _AbsTagBase(object):
    INDENT = 20
    HEIGHT = 18

    PATHSEP = '/'

    def _init_tag_base_(self, widget):
        self._widget = widget

        self._group_root_widget = None
        self._parent_widget = None

        self._path_set = set()

        self._tool_tip_css = None

        self._force_visible_flag = False

    def _get_text_(self):
        raise NotImplementedError()

    def _get_path_text_(self):
        raise NotImplementedError()

    def _set_number_(self, value):
        raise NotImplementedError()

    def _set_group_root_(self, group_widget):
        self._group_root_widget = group_widget

    def _set_group_(self, group_widget):
        self._parent_widget = group_widget

    def _set_tool_tip_(self, content):
        self._tool_tip_css = _qt_core.QtUtil.generate_tool_tip_css(
            self._get_text_(), content
        )

    def _is_checked_(self):
        raise NotImplementedError()

    def _get_siblings_(self):
        if self._get_path_text_() == self.PATHSEP:
            return [
                self._group_root_widget._item_dict[x]
                for x in self._group_root_widget._item_dict.keys()
                if x != self.PATHSEP
            ]
        return [
            self._group_root_widget._item_dict[x]
            for x in fnmatch.filter(
                self._group_root_widget._item_dict.keys(), '{}/*'.format(self._get_path_text_())
            )
        ]

    def _get_sibling_check_states_(self):
        return [x._is_checked_() for x in self._get_siblings_()]

    def _get_all_(self, paths):
        return [self._group_root_widget._item_dict[x] for x in paths]

    def _update_check_state_for_siblings_(self):
        widgets = self._get_siblings_()
        widgets.reverse()
        [x._set_checked_(self._is_checked_()) for x in widgets]

    def _update_check_state_for_ancestors_(self):
        ancestor_paths = bsc_core.BscPathOpt(
            self._get_path_text_()
        ).get_ancestor_paths()
        ancestors = self._get_all_(ancestor_paths)
        if self._is_checked_() is True:
            [x._set_checked_(True) for x in ancestors]
        else:
            [x._set_checked_(False) for x in ancestors if sum(x._get_sibling_check_states_()) == 0]

    def _assign_path_set_(self, path_set):
        self._path_set = path_set
        self._set_number_(len(self._path_set))

    def _update_path_set_as_intersection_(self, path_set):
        if path_set:
            path_set = set.intersection(path_set, self._path_set)
        else:
            path_set = self._path_set

        self._set_number_(len(path_set))

    def _expand_ancestors_(self):
        ancestor_paths = bsc_core.BscPathOpt(
            self._get_path_text_()
        ).get_ancestor_paths()
        ancestors = self._get_all_(ancestor_paths)
        [x._set_expanded_(True) for x in ancestors]

    def _set_force_hidden_flag_(self, boolean):
        self._force_visible_flag = boolean


class _QtTagNode(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtPathBaseDef,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForCheckDef,

    _qt_abstracts.AbsQtThreadBaseDef,

    _AbsTagBase
):
    user_filter_checked = qt_signal()
    
    def _refresh_widget_all_(self):
        self._painter_flag = True
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self._generate_pixmap_cache_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        spc = 2
        c_x = 0

        txt_w, txt_h = QtGui.QFontMetrics(self._text_font).width(self._text)+8, h
        self._frame_border_radius = 2
        # text
        self._text_draw_rect.setRect(
            c_x, y, txt_w, txt_h
        )
        c_x += txt_w
        # number
        if self._number_flag is True:
            num_w, num_h = QtGui.QFontMetrics(self._number_font).width(self._number_text)+8, h

            self._number_draw_rect.setRect(
                c_x, y, num_w, num_h
            )
            c_x += num_w

        fix_w = c_x
        self._frame_draw_rect.setRect(
            x+1, y+1, fix_w-1, h-1
        )
        self.setFixedWidth(fix_w)

    def _generate_pixmap_cache_(self):
        if self.isHidden():
            return

        size = QtCore.QSize(self.width(), self.height())
        self._pixmap_cache = QtGui.QPixmap(size)
        painter = _qt_core.QtPainter(self._pixmap_cache)
        self._pixmap_cache.fill(QtGui.QColor(*_gui_core.GuiRgba.Dim))

        if self._is_hovered:
            bkg_color = _gui_core.GuiRgba.LightOrange
        elif self._is_checked:
            bkg_color = self._frame_background_color_checked
        else:
            bkg_color = self._frame_background_color

        painter._set_border_color_(_qt_core.QtBorderColors.Transparent)
        painter._set_background_color_(bkg_color)
        painter.drawRect(
            self._frame_draw_rect
        )
        # text
        text = painter.fontMetrics().elidedText(
            self._text,
            QtCore.Qt.ElideMiddle,
            self._text_draw_rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter._set_text_color_([self._text_color, self._text_color_checked][self._is_hovered or self._is_checked])
        painter._set_font_(self._text_font)
        painter.drawText(
            self._text_draw_rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            text
        )
        number_text = painter.fontMetrics().elidedText(
            self._number_text,
            QtCore.Qt.ElideMiddle,
            self._number_draw_rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._number_draw_rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            number_text
        )
        painter.end()

    def _do_enter_(self):
        self._is_hovered = True
        self._refresh_widget_draw_()

    def _do_leave_(self):
        self._is_hovered = False
        self._expand_is_hovered = False
        self._refresh_widget_draw_()

    def _do_mouse_press_(self, event):
        if self._get_action_is_enable_() is True:
            self._set_action_flag_(self.ActionFlag.Press)

    def _do_mouse_press_release_(self, event):
        if self._is_action_flag_match_(self.ActionFlag.Press):
            self._swap_check_()

            self._update_check_state_for_ancestors_()

            self.user_filter_checked.emit()

    def _do_press_dbl_click_(self, event):
        if self._get_action_is_enable_() is True:
            self._set_action_flag_(self.ActionFlag.PressDblClick)
            self._do_check_exclusive_()

            self._update_check_state_for_ancestors_()

    def _do_check_exclusive_(self):
        self._parent_widget._set_all_node_checked_(False)
        self._set_checked_(True)

    def _do_show_tool_tip_(self, event):
        if self._tool_tip_css is not None:
            p = self._frame_draw_rect.bottomRight()
            p = self.mapToGlobal(p) + QtCore.QPoint(0, -18)
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                p, self._tool_tip_css, self
            )

    def __init__(self, *args, **kwargs):
        super(_QtTagNode, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedHeight(self.HEIGHT)

        self._pixmap_cache = QtGui.QPixmap()

        self._init_path_base_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)

        self._init_thread_base_def_(self)

        self._init_tag_base_(self)

        self._is_hovered = False

        self._painter_flag = False

        self._frame_draw_rect = QtCore.QRect()
        self._frame_border_radius = 0
        self._frame_background_color = _gui_core.GuiRgba.DarkWhite
        self._frame_background_color_checked = _gui_core.GuiRgba.LightAzureBlue

        self._text = None
        self._text_color = _gui_core.GuiRgba.LightBlack
        self._text_color_checked = _gui_core.GuiRgba.LightBlack
        self._text_w_maximum = 96

        self._text_font = _qt_core.QtFont.generate(size=8)

        self._text_draw_rect = QtCore.QRect()

        self._number_flag = False
        self._number = None
        self._number_text = None
        self._number_draw_rect = QtCore.QRect()

        self._number_font = _qt_core.QtFont.generate(size=8)
        
        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)

            elif event.type() == QtCore.QEvent.Enter:
                self._do_enter_()
            elif event.type() == QtCore.QEvent.Leave:
                self._do_leave_()

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_mouse_press_(event)
            # elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            #     if event.button() == QtCore.Qt.LeftButton:
            #         self._do_press_dbl_click_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_mouse_press_release_(event)

                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter.drawPixmap(0, 0, self._pixmap_cache)
        painter.device()

    def _set_text_(self, text):
        self._text = text

        self._refresh_widget_all_()
        # update when text is changed
        self._parent_widget._refresh_widget_all_()

    def _get_text_(self):
        return self._text

    def _set_number_(self, value):
        self._number_flag = True

        self._number = value
        self._number_text = '({})'.format(value)

        if value > 0:
            self._frame_background_color = _gui_core.GuiRgba.DarkWhite
            self._frame_background_color_checked = _gui_core.GuiRgba.LightAzureBlue
            self._text_color = _gui_core.GuiRgba.LightBlack
            self._text_font.setItalic(False)
            self._number_font.setItalic(False)
            self._text_font.setStrikeOut(False)
            self._number_font.setStrikeOut(False)
        else:
            self._frame_background_color = _gui_core.GuiRgba.Dim
            self._frame_background_color_checked = _gui_core.GuiRgba.DarkAzureBlue
            self._text_color = _gui_core.GuiRgba.Gray
            self._text_font.setItalic(True)
            self._number_font.setItalic(True)
            self._text_font.setStrikeOut(True)
            self._number_font.setStrikeOut(True)

        self._refresh_widget_all_()
        # update when text is changed
        self._parent_widget._refresh_widget_all_()

    def _apply_check_state_(self, boolean):
        self._set_checked_(boolean)
        self._update_check_state_for_ancestors_()


class _QtTagGroup(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtPathBaseDef,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForExpandDef,
    _qt_abstracts.AbsQtActionForCheckDef,

    _qt_abstracts.AbsQtThreadBaseDef,

    _AbsTagBase
):
    SPACING = 2

    user_filter_checked = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self._generate_pixmap_cache_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        vpt_w = self._viewport.width()

        spc = 2
        frm_w = frm_h = self.HEIGHT

        # head frame
        self._head_frame_rect.setRect(
            x+1, y+1, w-2, frm_h-2
        )
        c_x = x
        # check
        icn_w = icn_h = 16
        self._check_frame_rect.setRect(
            c_x+1, y+1, frm_w-2, frm_h-2
        )
        self._check_icon_draw_rect.setRect(
            c_x+(frm_w-icn_w)/2, y+(frm_h-icn_h)/2, icn_w, icn_h
        )
        c_x += frm_w+spc
        # expand
        icn_w = icn_h = 16
        self._expand_frame_rect.setRect(
            c_x+1, y+1, w-c_x, frm_h-2
        )
        self._expand_icon_draw_rect.setRect(
            c_x+(frm_w-icn_w)/2, y+(frm_h-icn_h)/2, icn_w, icn_h
        )
        c_x += frm_w+spc
        # text
        txt_w, txt_h = QtGui.QFontMetrics(self._text_font).width(self._text)+8, frm_h
        self._text_draw_rect.setRect(
            c_x, y, txt_w, txt_h
        )
        c_x += txt_w+spc
        # number
        if self._number_flag is True:
            num_w, num_h = QtGui.QFontMetrics(self._number_font).width(self._number_text)+8, frm_h

            self._number_draw_rect.setRect(
                c_x, y, num_w, num_h
            )
            c_x += num_w
        # sub text
        self._sub_text_draw_rect.setRect(
            c_x, y, w-c_x, txt_h
        )

        self._sub_text = None

        if self._is_expanded is True:
            self._viewport.show()
            # node
            nod_h_min = 0
            if len(self._node_widgets) > 0:
                i_x, i_y = 0, 0
                for i_widget in self._node_widgets:
                    i_w, i_h = i_widget.width(), i_widget.height()
                    if (i_x+i_w) >= vpt_w:
                        i_y += frm_h+spc
                        i_x = 0

                    i_widget.setGeometry(
                        i_x, i_y, i_w, i_h
                    )
                    i_widget.show()
                    i_widget._refresh_widget_all_()

                    i_x += i_w+spc

                vpt_h = i_y+frm_h

                nod_h_min = vpt_h
                # update to parent
                if nod_h_min != h:
                    if self._parent_widget is not None:
                        self._parent_widget._refresh_widget_all_()

                self._group_lot.setContentsMargins(
                    0, nod_h_min+spc, 0, 0
                )
            else:
                self._group_lot.setContentsMargins(
                    0, 0, 0, 0
                )

            grp_h_min = 0
            if self._group_widgets:
                grp_hs = 0
                for i in self._group_widgets:
                    grp_hs += i.minimumHeight()+spc

                grp_h_min = grp_hs

            if nod_h_min > 0:
                if grp_h_min > 0:
                    self.setMinimumHeight(frm_h+spc+nod_h_min+spc+grp_h_min)
                else:
                    self.setMinimumHeight(frm_h+spc+nod_h_min+spc+grp_h_min)
            else:
                self.setMinimumHeight(frm_h+spc+grp_h_min)
        else:
            self._viewport.hide()

            if len(self._node_widgets) > 0:
                checked_nodes = self._get_all_checked_nodes_()
                if checked_nodes:
                    self._sub_text = six.u('[{}]').format('+'.join([x._get_text_() for x in checked_nodes]))

            self.setMinimumHeight(frm_h)

    def _generate_pixmap_cache_(self):
        size = QtCore.QSize(self.width(), self.height())
        self._pixmap_cache = QtGui.QPixmap(size)
        painter = _qt_core.QtPainter(self._pixmap_cache)
        self._pixmap_cache.fill(QtGui.QColor(*_gui_core.GuiRgba.Dim))

        offset = self._get_action_offset_()
        # expand
        painter._draw_icon_file_by_rect_(
            rect=self._expand_icon_draw_rect,
            file_path=self._expand_icon_file_path_current,
            offset=offset,
            is_hovered=self._expand_is_hovered
        )
        # check
        painter._draw_icon_file_by_rect_(
            rect=self._check_icon_draw_rect,
            file_path=self._check_icon_file_path_current,
            offset=offset,
            is_hovered=self._is_check_hovered
        )
        # text
        painter._draw_text_by_rect_(
            self._text_draw_rect,
            text=self._text,
            text_color=self._text_color,
            font=self._text_font,
            offset=offset,
        )
        # number
        painter._draw_text_by_rect_(
            self._number_draw_rect,
            text=self._number_text,
            text_color=self._text_color,
            font=self._number_font,
            offset=offset
        )
        # sub text
        if self._sub_text is not None:
            painter._draw_text_by_rect_(
                self._sub_text_draw_rect,
                text=self._sub_text,
                text_color=self._text_color,
                font=self._sub_text_font,
                offset=offset,
                text_option=QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,
            )

        painter.end()

    def _do_enter_(self):
        self._is_hovered = True
        self._refresh_widget_draw_()

    def _do_leave_(self):
        self._is_hovered = False

        self._expand_is_hovered = False
        self._is_check_hovered = False

        # print 'leave', self._text, self._expand_is_hovered

        self._refresh_widget_draw_()

    def _do_hover_move_(self, event):
        p = event.pos()

        self._expand_is_hovered = False
        self._is_check_hovered = False
        if self._head_frame_rect.contains(p):
            if self._expand_frame_rect.contains(p):
                self._expand_is_hovered = True
            elif self._check_frame_rect.contains(p):
                self._is_check_hovered = True

        # print self._text, self._expand_is_hovered

        self._refresh_widget_draw_()

    def _do_mouse_press_(self, event):
        if self._head_frame_rect.contains(event.pos()):
            if self._get_action_is_enable_() is True:
                self._set_action_flag_(self.ActionFlag.Press)

    def _do_mouse_press_release_(self, event):
        if self._is_action_flag_match_(self.ActionFlag.Press):
            if self._expand_is_hovered is True:
                self._swap_expand_()
            elif self._is_check_hovered is True:
                self._swap_check_()

                self._update_check_state_for_siblings_()
                self._update_check_state_for_ancestors_()
                # todo: must refresh for children change
                self._refresh_widget_all_()

                self.user_filter_checked.emit()

    def _do_show_tool_tip_(self, event):
        if self._tool_tip_css is not None:
            if self._head_frame_rect.contains(event.pos()):
                p = self._head_frame_rect.bottomRight()
                p = self.mapToGlobal(p) + QtCore.QPoint(0, -18)
                # noinspection PyArgumentList
                QtWidgets.QToolTip.showText(
                    p, self._tool_tip_css, self
                )

    def __init__(self, *args, **kwargs):
        super(_QtTagGroup, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setMinimumHeight(self.HEIGHT)
        self.setMouseTracking(True)

        self._pixmap_cache = QtGui.QPixmap()

        self._init_path_base_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_expand_def_(self)
        self._init_action_for_check_def_(self)

        self._init_thread_base_def_(self)

        self._init_tag_base_(self)

        self._is_hovered = False

        self._group_root_widget = None
        self._parent_widget = None

        self._lot = _base.QtVBoxLayout(self)
        self._lot.setContentsMargins(self.INDENT, self.HEIGHT+self.SPACING, 0, 0)
        self._lot.setAlignment(QtCore.Qt.AlignTop)
        self._lot.setSpacing(0)

        self._viewport = QtWidgets.QWidget()
        self._viewport.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self._viewport.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self._lot.addWidget(self._viewport)
        self._viewport.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._viewport.setMinimumHeight(self.HEIGHT)

        self._group_lot = _base.QtVBoxLayout(self._viewport)
        self._group_lot.setContentsMargins(0, 0, 0, 0)
        self._group_lot.setAlignment(QtCore.Qt.AlignTop)
        self._group_lot.setSpacing(0)

        self._expand_icon_file_path_0 = _gui_core.GuiIcon.get('file/folder-close')
        self._expand_icon_file_path_1 = _gui_core.GuiIcon.get('file/folder-open')
        self._update_expand_icon_file_()

        self._check_icon_file_path_0 = _gui_core.GuiIcon.get('tag-filter-unchecked')
        self._check_icon_file_path_1 = _gui_core.GuiIcon.get('tag-filter-checked')
        self._update_check_icon_file_()

        self._text_font = _qt_core.QtFont.generate(size=8, weight=75)
        self.setFont(self._text_font)

        self._text = None
        self._text_color = _gui_core.GuiRgba.Light

        self._text_draw_rect = QtCore.QRect()

        self._sub_text = None
        self._sub_text_font = _qt_core.QtFont.generate(size=8)
        self._sub_text_draw_rect = QtCore.QRect()

        self._head_frame_rect = QtCore.QRect()
        self._frame_border_color = _gui_core.GuiRgba.Gray
        self._frame_background_color = _gui_core.GuiRgba.Basic

        self._frame_draw_line = QtCore.QLine()

        self._number_flag = False
        self._number = None
        self._number_text = None
        self._number_draw_rect = QtCore.QRect()

        self._number_font = _qt_core.QtFont.generate(size=8)

        self._group_widgets = []
        self._node_widgets = []

        self.installEventFilter(self)

        self._viewport.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if not hasattr(event, 'type'):
                return False

            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)

            elif event.type() == QtCore.QEvent.Enter:
                self._do_enter_()
            elif event.type() == QtCore.QEvent.Leave:
                self._do_leave_()
            # elif event.type() == QtCore.QEvent.ToolTip:
            #     self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_mouse_press_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_mouse_press_release_(event)

                self._clear_all_action_flags_()
        elif widget == self._viewport:
            if event.type() == QtCore.QEvent.Enter:
                self._do_leave_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter.drawPixmap(0, 0, self._pixmap_cache)
        painter.device()

    def _refresh_expand_(self):
        self._update_expand_icon_file_()

        self._refresh_widget_all_()

        if self._parent_widget is not None:
            self._parent_widget._refresh_widget_all_()

    def _refresh_check_(self):
        self._update_check_icon_file_()

        self._refresh_widget_all_()

    def _set_text_(self, text):
        self._text = text
        self._refresh_widget_all_()

    def _get_text_(self):
        return self._text

    def _set_number_(self, value):
        self._number_flag = True

        self._number = value
        self._number_text = '({})'.format(value)

        self._refresh_widget_all_()

    def _create_group_(self, path, *args, **kwargs):
        widget = _QtTagGroup(self._viewport)
        self._group_lot.addWidget(widget)
        self._group_widgets.append(widget)
        widget._set_group_(self)
        widget._set_path_text_(path)
        if 'show_name' in kwargs:
            widget._set_text_(kwargs['show_name'])
        else:
            widget._set_text_(
                bsc_core.RawTextMtd.to_prettify(
                    bsc_core.BscPath.to_dag_name(path),
                    capitalize=True
                )
            )
        # self._refresh_widget_all_()
        return widget

    def _create_node_(self, path, *args, **kwargs):
        widget = _QtTagNode(self._viewport)
        self._node_widgets.append(widget)
        widget._set_group_(self)
        widget._set_path_text_(path)
        if 'show_name' in kwargs:
            widget._set_text_(kwargs['show_name'])
        else:
            widget._set_text_(
                bsc_core.RawTextMtd.to_prettify(
                    bsc_core.BscPath.to_dag_name(path),
                    capitalize=True
                )
            )
        # self._refresh_widget_all_()
        return widget

    def _get_all_checked_nodes_(self):
        return [x for x in self._group_widgets or self._node_widgets if x._is_checked_() is True]

    def _set_all_node_checked_(self, boolean):
        [x._set_checked_(boolean) for x in self._group_widgets or self._node_widgets]


class QtViewForTagRoot(
    QtWidgets.QWidget,

    _AbsTagBase,
):
    SPACING = 2

    MARGIN = 2

    check_paths_change_accepted = qt_signal(list)
    check_paths_changed = qt_signal()

    focus_changed = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        pass

    def _user_filter_check_cbk_(self):
        self.check_paths_change_accepted.emit(
            self._get_all_checked_node_paths_()
        )
        self.check_paths_changed.emit()

    def __init__(self, *args, **kwargs):
        super(QtViewForTagRoot, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setMinimumHeight(self.HEIGHT)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._init_tag_base_(self)

        self._frame_background_color = _qt_core.QtBackgroundColors.Dim

        self._lot = _base.QtVBoxLayout(self)
        self._lot.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        self._lot.setAlignment(QtCore.Qt.AlignTop)

        self._sca = _utility.QtVScrollArea()
        self._lot.addWidget(self._sca)
        self._sca._set_background_color_(self._frame_background_color)
        self._sca._set_empty_draw_flag_(True)
        self._sca._layout.setAlignment(QtCore.Qt.AlignTop)

        self._item_dict = collections.OrderedDict()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.FocusIn:
                self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _entry_frame.QtEntryFrame):
                    parent._set_focused_(True)
                self.focus_changed.emit()
            elif event.type() == QtCore.QEvent.FocusOut:
                self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _entry_frame.QtEntryFrame):
                    parent._set_focused_(False)
                self.focus_changed.emit()
        return False

    def paintEvent(self, event):
        pass
        # if not self._item_dict:
        #     painter = _qt_core.QtPainter(self)
        #     painter._draw_empty_image_by_rect_(
        #         self.rect(),
        #         self._empty_icon_name
        #     )
        # offset = self._sca.verticalScrollBar().value()
        # h = self._sca._layout.minimumSize().height()
        # x, y = 0, 0
        # print offset, h

    def _create_group_root_(self, path, *args, **kwargs):
        widget = _QtTagGroup()
        self._sca._add_widget_(widget)
        widget._set_path_text_(path)
        if 'show_name' in kwargs:
            widget._set_text_(kwargs['show_name'])
        else:
            widget._set_text_('All')

        widget._set_group_root_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        self._sca._set_empty_draw_flag_(False)
        return widget

    def _create_group_(self, path, *args, **kwargs):
        if path in self._item_dict:
            return self._item_dict[path]

        if path == self.PATHSEP:
            return self._create_group_root_(path, *args, **kwargs)

        group_widget = self._item_dict[bsc_core.BscPath.get_dag_parent_path(path)]
        widget = group_widget._create_group_(path, *args, **kwargs)

        widget._set_group_root_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        return widget

    def _create_node_(self, path, *args, **kwargs):
        if path in self._item_dict:
            return self._item_dict[path]

        group_widget = self._item_dict[bsc_core.BscPath.get_dag_parent_path(path)]
        widget = group_widget._create_node_(path, *args, **kwargs)

        widget._set_group_root_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        return widget

    def _check_exists_(self, path):
        return path in self._item_dict

    def _clear_all_checked_(self):
        [x._set_checked_(False) for x in self._item_dict.values()]

    def _get_one_(self, path):
        return self._item_dict[path]

    def _get_all_checked_node_paths_(self):
        return [x._get_path_text_() for x in self._get_all_checked_nodes_()]

    def _get_all_checked_nodes_(self):
        return [x for x in self._item_dict.values() if x._is_checked_() and isinstance(x, _QtTagNode)]

    def _apply_intersection_paths_(self, path_set):
        [x._update_path_set_as_intersection_(path_set) for x in self._item_dict.values()]

    def _restore_(self):
        self._item_dict.clear()
        self._sca._layout._clear_all_widgets_()
        self._sca._set_empty_draw_flag_(True)

    def _collapse_all_groups_(self):
        [x._set_expanded_(False) for x in self._item_dict.values() if isinstance(x, _QtTagGroup)]

    def _expand_exclusive_for_node_(self, path):
        self._collapse_all_groups_()
        paths = bsc_core.BscPath.get_dag_component_paths(path)
        for i in paths:
            if i in self._item_dict:
                i_widget = self._item_dict[i]
                if isinstance(i_widget, _QtTagGroup):
                    i_widget._set_expanded_(True)
    
    def _expand_all_groups_(self):
        [x._set_expanded_(True) for x in self._item_dict.values() if isinstance(x, _QtTagGroup)]

    def _expand_for_all_from_(self, path):
        self._collapse_all_groups_()
        paths = bsc_core.BscPath.get_dag_component_paths(path)
        self._set_expanded_for_(paths, True)
        descendant_paths = bsc_core.BscPath.find_dag_descendant_paths(path, self._item_dict.keys())
        self._set_expanded_for_(descendant_paths, True)

    def _set_expanded_for_(self, paths, boolean):
        for i in paths:
            if i in self._item_dict:
                i_widget = self._item_dict[i]
                if isinstance(i_widget, _QtTagGroup):
                    i_widget._set_expanded_(boolean)

    def _set_force_hidden_flag_for_group_(self, path, boolean):
        pass

    def _generate_chart_data_(self):
        dict_ = {}
        for i_wgt in self._item_dict.values():
            if isinstance(i_wgt, _QtTagGroup):
                i_dict = {}
                for j_wgt in i_wgt._node_widgets:
                    j_value = j_wgt._number
                    if j_value:
                        i_dict[j_wgt._text] = j_value
                if i_dict:
                    dict_[i_wgt._text] = i_dict
        return dict_

