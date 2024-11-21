# coding=utf-8
import collections
import copy

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
from ..widgets import base as _wgt_base

from ..widgets import utility as _wgt_utility

from ..view_models import item_for_tag as _vew_mod_item_for_tag


class _AbsTagItem(object):
    INDENT = 20
    HEIGHT = 18

    PATHSEP = '/'

    QT_MENU_CLS = _wgt_utility.QtMenu

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            bsc_core.ensure_string(self._item_model.get_name())
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _do_enter_(self):
        self._item_model._update_hover(True)
        self._refresh_widget_draw_()

    def _do_leave_(self):
        self._item_model._update_hover(False)
        self._expand_is_hovered = False
        self._refresh_widget_draw_()

    def _get_number_flag_(self):
        if self._item_model._data.number_enable is True:
            return self._item_model._data.number.flag
        return False

    def _init_tag_base_(self, widget):
        self._widget = widget

        self._item_model = _vew_mod_item_for_tag.TagItemMode(self)

        self._view_widget = None
        self._parent_widget = None

        self._path_set_pre = set()
        self._path_set = set()

        self._tool_tip_css = None

        self._force_visible_flag = False

    def _set_view_(self, group_widget):
        self._view_widget = group_widget

    def _set_group_(self, group_widget):
        self._parent_widget = group_widget

    def _set_tool_tip_(self, content):
        if self._item_model.get_name():
            self._tool_tip_css = _qt_core.QtUtil.generate_tool_tip_css(
                self._item_model.get_name(), content
            )

    def _is_checked_(self):
        raise NotImplementedError()

    def _get_siblings_(self):
        if self._item_model.get_path() == self.PATHSEP:
            return [
                self._view_widget._item_dict[x]
                for x in self._view_widget._item_dict.keys()
                if x != self.PATHSEP
            ]
        return [
            self._view_widget._item_dict[x]
            for x in fnmatch.filter(
                self._view_widget._item_dict.keys(), '{}/*'.format(self._item_model.get_path())
            )
        ]

    def _get_sibling_check_states_(self):
        return [x._is_checked_() for x in self._get_siblings_()]

    def _get_all_(self, paths):
        return [self._view_widget._item_dict[x] for x in paths]

    def _get_one_(self, path):
        return self._view_widget._item_dict[path]

    def _get_ancestors_(self):
        ancestor_paths = bsc_core.BscNodePathOpt(
            self._item_model.get_path()
        ).get_ancestor_paths()
        return self._get_all_(ancestor_paths)

    def _get_parent_(self):
        parent_path = bsc_core.BscNodePath.get_dag_parent_path(self._item_model.get_path())
        if parent_path:
            return self._get_one_(parent_path)

    def _update_check_state_for_siblings_(self):
        widgets = self._get_siblings_()
        widgets.reverse()
        [x._set_checked_(self._is_checked_()) for x in widgets]

    def _update_check_state_for_ancestors_(self):
        ancestor_paths = bsc_core.BscNodePathOpt(
            self._item_model.get_path()
        ).get_ancestor_paths()
        ancestors = self._get_all_(ancestor_paths)
        if self._is_checked_() is True:
            [x._set_checked_(True) for x in ancestors]
        else:
            [x._set_checked_(False) for x in ancestors if sum(x._get_sibling_check_states_()) == 0]

    def _set_assign_path_set_(self, path_set):
        self._path_set_pre = copy.copy(self._path_set)

        self._path_set = path_set

        self._item_model.set_number(len(self._path_set))

    def _get_assign_path_set_(self):
        return self._path_set

    def _update_path_set_as_intersection_(self, path_set):
        if path_set:
            path_set = set.intersection(path_set, self._path_set)
        else:
            path_set = self._path_set

        self._item_model.set_number(len(path_set))

    def _expand_ancestors_(self):
        ancestor_paths = bsc_core.BscNodePathOpt(
            self._item_model.get_path()
        ).get_ancestor_paths()
        ancestors = self._get_all_(ancestor_paths)
        [x._set_expanded_(True) for x in ancestors]

    def _set_force_hidden_flag_(self, boolean):
        self._force_visible_flag = boolean

    def _update_assign_path_to_parent(self):
        parent_item = self._get_parent_()
        if parent_item:
            path_set = self._path_set
            path_set_pre = self._path_set_pre

            path_set_addition = path_set.difference(path_set_pre)
            path_set_deletion = path_set_pre.difference(path_set)

            # print self, self._path_set, path_set_addition, path_set_deletion
            parent_item._update_assign_path_set(path_set_addition, path_set_deletion)
            parent_item._update_assign_path_to_parent()

    def _update_assign_path_set(self, path_set_addition, path_set_deletion):
        # must use copy
        self._path_set_pre = copy.copy(self._path_set)

        self._path_set.update(path_set_addition)
        self._path_set.difference_update(path_set_deletion)

        self._item_model.set_number(len(self._path_set))

    def _update_assign_path_set_to_ancestors(self):
        self._update_assign_path_to_parent()


class _QtTagNodeItem(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForCheckDef,

    _qt_abstracts.AbsQtThreadBaseDef,

    _AbsTagItem,
):
    user_filter_checked = qt_signal()

    def _on_context_menu_(self, event):
        menu = None

        menu_data = self._item_model.get_menu_data()
        menu_content = self._item_model.get_menu_content()
        menu_data_generate_fnc = self._item_model.get_menu_data_generate_fnc()

        if menu_content:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            menu._set_menu_content_(menu_content, append=True)

        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            menu._set_menu_data_(menu_data)

        if menu_data_generate_fnc:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            menu._set_menu_data_(menu_data_generate_fnc())

        if menu is not None:
            menu._popup_start_()

    def _refresh_widget_all_(self):
        self._painter_flag = True
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self._generate_pixmap_cache_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        item_model_data = self._item_model._data

        x, y = 0, 0
        w, h = self.width(), self.height()

        spc = 2
        c_x = 0

        font = item_model_data.text.font

        txt_w, txt_h = QtGui.QFontMetrics(font).width(item_model_data.name.text)+8, h
        self._frame_border_radius = 2
        # text
        item_model_data.name.rect.setRect(
            c_x, y, txt_w, txt_h
        )
        c_x += txt_w
        # number
        if item_model_data.number_enable is True:
            num_w, num_h = QtGui.QFontMetrics(font).width(item_model_data.number.text)+8, h

            item_model_data.number.rect.setRect(
                c_x, y, num_w, num_h
            )
            c_x += num_w

        fix_w = c_x
        self._frame_draw_rect.setRect(
            x+1, y+1, fix_w-1, h-1
        )
        item_model_data.frame.rect.setRect(
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
        
        item_model_data = self._item_model._data
        is_hovered = item_model_data.hover.flag

        if item_model_data.number_enable is True:
            if item_model_data.number.flag is True:
                if is_hovered:
                    bkg_color = item_model_data.hover.color
                elif self._is_checked:
                    bkg_color = QtGui.QColor(*_gui_core.GuiRgba.LightPurple)
                else:
                    bkg_color = QtGui.QColor(223, 223, 223)

                txt_color = QtGui.QColor(*_gui_core.GuiRgba.LightBlack)
            else:
                txt_color = QtGui.QColor(*_gui_core.GuiRgba.Gray)
                if is_hovered:
                    bkg_color = item_model_data.hover.color
                elif self._is_checked:
                    bkg_color = QtGui.QColor(*_gui_core.GuiRgba.DarkPurple)
                else:
                    bkg_color = QtGui.QColor(0, 0, 0, 0)
        else:
            if is_hovered:
                bkg_color = item_model_data.hover.color
            elif self._is_checked:
                bkg_color = QtGui.QColor(*_gui_core.GuiRgba.LightPurple)
            else:
                bkg_color = QtGui.QColor(223, 223, 223)

            txt_color = QtGui.QColor(*_gui_core.GuiRgba.LightBlack)

        painter.setPen(QtGui.QColor(0, 0, 0, 0))
        painter.setBrush(bkg_color)
        painter.drawRect(item_model_data.frame.rect)

        painter.setPen(txt_color)
        painter.setFont(item_model_data.text.font)
        # text
        text = painter.fontMetrics().elidedText(
            item_model_data.name.text,
            QtCore.Qt.ElideMiddle,
            item_model_data.name.rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            item_model_data.name.rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            text
        )
        # number
        number_text = painter.fontMetrics().elidedText(
            item_model_data.number.text,
            QtCore.Qt.ElideMiddle,
            item_model_data.number.rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            item_model_data.number.rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            number_text
        )
        painter.end()

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
            p = self._frame_draw_rect.bottomLeft()
            p = self.mapToGlobal(p)+QtCore.QPoint(0, -15)
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                p, self._tool_tip_css, self
            )

    def __init__(self, *args, **kwargs):
        super(_QtTagNodeItem, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedHeight(self.HEIGHT)

        self._pixmap_cache = QtGui.QPixmap()

        self._init_action_base_def_(self)
        self._init_action_for_check_def_(self)

        self._init_thread_base_def_(self)

        self._init_tag_base_(self)

        self._painter_flag = False

        self._frame_draw_rect = QtCore.QRect()
        self._frame_border_radius = 0
        self._frame_background_color = _gui_core.GuiRgba.DarkWhite
        self._frame_background_color_checked = _gui_core.GuiRgba.LightAzureBlue

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
                elif event.button() == QtCore.Qt.RightButton:
                    self._on_context_menu_(event)
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

    def _update_check_state_(self, boolean):
        self._set_checked_(boolean)
        self._update_check_state_for_ancestors_()


class _QtTagGroupItem(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForExpandDef,
    _qt_abstracts.AbsQtActionForCheckDef,

    _qt_abstracts.AbsQtThreadBaseDef,

    _AbsTagItem,
):
    SPACING = 2

    user_filter_checked = qt_signal()

    def _on_context_menu_(self, event):
        if self._item_model._data.frame.rect.contains(event.pos()):
            menu = None

            menu_data = self._item_model.get_menu_data()
            menu_content = self._item_model.get_menu_content()
            menu_data_generate_fnc = self._item_model.get_menu_data_generate_fnc()

            if menu_content:
                if menu is None:
                    menu = self.QT_MENU_CLS(self)
                menu._set_menu_content_(menu_content, append=True)

            if menu_data:
                if menu is None:
                    menu = self.QT_MENU_CLS(self)
                menu._set_menu_data_(menu_data)

            if menu_data_generate_fnc:
                if menu is None:
                    menu = self.QT_MENU_CLS(self)
                menu._set_menu_data_(menu_data_generate_fnc())

            if menu is not None:
                menu._popup_start_()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self._generate_pixmap_cache_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        item_model_data = self._item_model._data

        font = item_model_data.text.font

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
        item_model_data.frame.rect.setRect(
            x+1, y+1, w-1, frm_h-1
        )
        c_x += frm_w+spc
        # text
        txt_w, txt_h = QtGui.QFontMetrics(font).width(item_model_data.name.text)+8, frm_h
        item_model_data.name.rect.setRect(
            c_x, y, txt_w, txt_h
        )
        c_x += txt_w+spc
        # number
        if item_model_data.number_enable is True:
            num_w, num_h = QtGui.QFontMetrics(font).width(item_model_data.number.text)+8, frm_h

            item_model_data.number.rect.setRect(
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

                # move group layout to nodes bottom
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
            # when is close show checked node names
            if len(self._node_widgets) > 0:
                checked_nodes = self._get_all_checked_nodes_()
                if checked_nodes:
                    self._sub_text = six.u('[{}]').format('+'.join([x._item_model.get_name() for x in checked_nodes]))

            self.setMinimumHeight(frm_h)

    def _generate_pixmap_cache_(self):
        size = QtCore.QSize(self.width(), self.height())
        self._pixmap_cache = QtGui.QPixmap(size)
        painter = _qt_core.QtPainter(self._pixmap_cache)
        self._pixmap_cache.fill(QtGui.QColor(*_gui_core.GuiRgba.Dim))

        item_model_data = self._item_model._data
        is_hovered = item_model_data.hover.flag

        if item_model_data.number_enable is True:
            if item_model_data.number.flag is True:
                txt_color = QtGui.QColor(*_gui_core.GuiRgba.DarkWhite)
            else:
                txt_color = QtGui.QColor(*_gui_core.GuiRgba.Gray)
        else:
            txt_color = QtGui.QColor(*_gui_core.GuiRgba.DarkWhite)
        # expand
        self._item_model._draw_icon_by_file(
            painter, self._expand_icon_draw_rect, self._expand_icon_file_path_current
        )
        # check
        self._item_model._draw_icon_by_file(
            painter, self._check_icon_draw_rect, self._check_icon_file_path_current
        )
        painter.setFont(item_model_data.text.font)
        painter.setPen(txt_color)
        # text
        text = painter.fontMetrics().elidedText(
            item_model_data.name.text,
            QtCore.Qt.ElideMiddle,
            item_model_data.name.rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            item_model_data.name.rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            text
        )
        # number
        number_text = painter.fontMetrics().elidedText(
            item_model_data.number.text,
            QtCore.Qt.ElideMiddle,
            item_model_data.number.rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            item_model_data.number.rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            number_text
        )
        # sub text
        if self._sub_text is not None:
            sub_text = painter.fontMetrics().elidedText(
                self._sub_text,
                QtCore.Qt.ElideMiddle,
                self._sub_text_draw_rect.width(),
                QtCore.Qt.TextShowMnemonic
            )
            painter.drawText(
                self._sub_text_draw_rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                sub_text
            )

        painter.end()

    def _do_hover_move_(self, event):
        p = event.pos()

        self._expand_is_hovered = False
        self._is_check_hovered = False
        if self._head_frame_rect.contains(p):
            if self._expand_frame_rect.contains(p):
                self._expand_is_hovered = True
            elif self._check_frame_rect.contains(p):
                self._is_check_hovered = True

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
                p = self._head_frame_rect.bottomLeft()
                p = self.mapToGlobal(p)+QtCore.QPoint(0, -18)
                # noinspection PyArgumentList
                QtWidgets.QToolTip.showText(
                    p, self._tool_tip_css, self
                )

    def __init__(self, *args, **kwargs):
        super(_QtTagGroupItem, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setMinimumHeight(self.HEIGHT)
        self.setMouseTracking(True)

        self._pixmap_cache = QtGui.QPixmap()

        self._init_action_base_def_(self)
        self._init_action_for_expand_def_(self)
        self._init_action_for_check_def_(self)

        self._init_thread_base_def_(self)

        self._init_tag_base_(self)

        self._view_widget = None
        self._parent_widget = None

        self._lot = _wgt_base.QtVBoxLayout(self)
        self._lot.setContentsMargins(self.INDENT, self.HEIGHT+self.SPACING, 0, 0)
        self._lot.setAlignment(QtCore.Qt.AlignTop)
        self._lot.setSpacing(0)

        # for children layout
        self._viewport = QtWidgets.QWidget()
        self._lot.addWidget(self._viewport)
        self._viewport.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._viewport.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # do not set minimum size, may be empty
        # self._viewport.setMinimumHeight(self.HEIGHT)

        # for group layout
        self._group_lot = _wgt_base.QtVBoxLayout(self._viewport)
        self._group_lot.setContentsMargins(0, 0, 0, 0)
        self._group_lot.setAlignment(QtCore.Qt.AlignTop)
        self._group_lot.setSpacing(0)

        self._expand_icon_file_path_0 = _gui_core.GuiIcon.get('file/folder-close')
        self._expand_icon_file_path_1 = _gui_core.GuiIcon.get('file/folder-open')
        self._update_expand_icon_file_()

        self._check_icon_file_path_0 = _gui_core.GuiIcon.get('tag-filter-unchecked')
        self._check_icon_file_path_1 = _gui_core.GuiIcon.get('tag-filter-checked')
        self._update_check_icon_file_()

        self._sub_text = None
        self._sub_text_draw_rect = QtCore.QRect()

        self._head_frame_rect = QtCore.QRect()
        self._frame_border_color = _gui_core.GuiRgba.Gray
        self._frame_background_color = _gui_core.GuiRgba.Basic

        self._frame_draw_line = QtCore.QLine()

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
                elif event.button() == QtCore.Qt.RightButton:
                    self._on_context_menu_(event)
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

        if _qt_core.QtApplication.is_shift_modifier():
            widgets = self._get_siblings_()
            for i in widgets:
                if isinstance(i, self.__class__):
                    i._set_expanded_(self._is_expanded)

    def _refresh_check_(self):
        self._update_check_icon_file_()

        self._refresh_widget_all_()

    def _create_group_(self, path, *args, **kwargs):
        widget = _QtTagGroupItem(self._viewport)
        self._group_lot.addWidget(widget)
        self._group_widgets.append(widget)
        widget._set_group_(self)
        widget._item_model.set_path(path)
        # self._refresh_widget_all_()
        return widget

    def _create_node_(self, path, *args, **kwargs):
        widget = _QtTagNodeItem(self._viewport)
        self._node_widgets.append(widget)
        widget._set_group_(self)
        widget._item_model.set_path(path)
        # self._refresh_widget_all_()
        return widget

    def _get_all_checked_nodes_(self):
        return [x for x in self._group_widgets or self._node_widgets if x._is_checked_() is True]

    def _add_node_(self, item):
        item._set_group_(self)
        self._node_widgets.append(item)

    def _set_all_node_checked_(self, boolean):
        [x._set_checked_(boolean) for x in self._group_widgets or self._node_widgets]