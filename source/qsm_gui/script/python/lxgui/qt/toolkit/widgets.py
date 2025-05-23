# coding:utf-8
import collections

import functools

import types

import six

from ... import core as _gui_core

from ..core.wrap import *

from .. import core as _qt_core

from . import base as _base


class QtToolTabBar(
    QtWidgets.QWidget,
    _base._AbsWidget
):
    H = 24

    current_index_change_accepted = qt_signal(int)

    class Model(
        _base._AbsModel,
        _base._AbsAction, _base._AbsPress
    ):
        def __init__(self, *args, **kwargs):
            super(QtToolTabBar.Model, self).__init__(*args, **kwargs)

            self._init_action()
            self._init_press()

            self._tab_widget = self._widget.parent()
            self._tab_model = self._tab_widget.model

            self._gui_data.update(
                dict(
                    tab=_gui_core.DictOpt(
                        current_index_tmp=None,
                        indices=[],
                        label=_gui_core.DictOpt(
                            text_font=_qt_core.QtFont.generate(9, weight=75),
                            text_color_0=QtGui.QColor(127, 127, 127, 255),
                            text_color_1=QtGui.QColor(223, 223, 223, 255),
                            texts=[]
                        ),
                        tip=_gui_core.DictOpt(
                            tool_tips=[]
                        ),
                        frame=_gui_core.DictOpt(
                            rects=[],
                            rect=QtCore.QRect(),
                            border_color=_qt_core.QtRgba.BdrTabGroup,
                            background_color=_qt_core.QtRgba.BkgTabGroup,
                            hover=_gui_core.DictOpt(
                                border_color=_qt_core.QtRgba.BdrTabGroup,
                                background_color=_qt_core.QtRgba.BkgTabGroupActive,
                            ),
                        ),
                    )
                )
            )

        def update_from(self, model):
            x, y = 0, 0
            w, h = self._widget.width(), self._widget.height()
            # if model.get_refresh_flag() is True:
            pages = list(model.get_all_pages())

            c = len(pages)

            font = self._gui_data.tab.label.text_font
            self._gui_data.tab.indices = range(c)
            self._gui_data.tab.frame.rects = rects = []
            self._gui_data.tab.label.texts = texts = []
            self._gui_data.tab.tip.tool_tips = tool_tips = []

            frame_h = QtToolTabBar.H

            c_y = y
            c_x = 0

            pages = list(model.get_all_pages())
            for i in pages:
                i_model = i.model
                i_text = i_model.get_label()
                i_tool_tip = i_model.get_tool_tip()
                i_w = QtGui.QFontMetrics(font).width(i_text)+16

                if (c_x+i_w+1) > w:
                    c_y += frame_h
                    c_x = 0

                i_rect = QtCore.QRect(
                    c_x, c_y, i_w, frame_h-2
                )
                rects.append(i_rect)
                texts.append(i_text)
                tool_tips.append(i_tool_tip)

                c_x += i_w

            fixed_h = c_y+frame_h
            self._widget.setFixedHeight(fixed_h)

            # model.set_refresh_flag(False)

            self._gui_data.tab.frame.rect.setRect(
                x, y, w, h-1
            )

        def update(self):
            self._widget.update()

        def draw(self, painter):
            index = self._tab_model.data.tab.current_index
            index_tmp = self._gui_data.tab.current_index_tmp
            indices = self._gui_data.tab.indices
            texts = self._gui_data.tab.label.texts
            rects = self._gui_data.tab.frame.rects
            for i_idx in indices:
                i_rect = rects[i_idx]
                i_text = texts[i_idx]
                # current
                if i_idx == index:
                    i_border_color = self._gui_data.tab.frame.hover.border_color
                    i_background_color = self._gui_data.tab.frame.hover.background_color
                    i_text_color = self._gui_data.tab.label.text_color_1

                else:
                    i_border_color = self._gui_data.tab.frame.border_color
                    i_background_color = self._gui_data.tab.frame.background_color
                    i_text_color = self._gui_data.tab.label.text_color_0

                # pressed
                if i_idx == index_tmp:
                    i_rect = QtCore.QRect(
                        i_rect.x()+2, i_rect.y()+2, i_rect.width()-2, i_rect.height()-2
                    )

                _qt_core.QtDrawBase._draw_frame(
                    painter,
                    rect=i_rect,
                    border_color=i_border_color,
                    background_color=i_background_color
                )
                _qt_core.QtDrawBase._draw_name_text(
                    painter,
                    rect=i_rect,
                    text=i_text,
                    text_color=i_text_color,
                    text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    text_font=self._gui_data.tab.label.text_font,
                )

            p_0, p_1 = self._gui_data.tab.frame.rect.bottomLeft(), self._gui_data.tab.frame.rect.bottomRight()
            _qt_core.QtDrawBase._draw_line(
                painter, p_0, p_1, self._gui_data.tab.frame.border_color
            )

        def _do_popup_tool_tip(self, event):
            p = event.pos()
            indices = self._gui_data.tab.indices
            rects = self._gui_data.tab.frame.rects
            texts = self._gui_data.tab.label.texts
            tool_tips = self._gui_data.tab.tip.tool_tips
            text = None
            tool_tip = None
            for i_idx in indices:
                i_rect = rects[i_idx]
                if i_rect.contains(p):
                    text = texts[i_idx]
                    tool_tip = tool_tips[i_idx]
                    break

            if text:
                css = _qt_core.QtUtil.generate_tool_tip_css(
                    text, tool_tip
                )
                # noinspection PyArgumentList
                QtWidgets.QToolTip.showText(
                    QtGui.QCursor.pos(), css, self._widget
                )

        def _do_press_click(self, event):
            p = event.pos()

            indices = self._gui_data.tab.indices
            rects = self._gui_data.tab.frame.rects

            self._gui_data.tab.current_index_tmp = None
            for i_idx in indices:
                i_rect = rects[i_idx]
                if i_rect.contains(p):
                    self._gui_data.tab.current_index_tmp = i_idx
                    break

            if self._gui_data.tab.current_index_tmp is not None:
                self.set_action_flag(self.ActionFlags.PressClicked)

            self.update()

        def _do_press_move(self, event):
            p = event.pos()

            indices = self._gui_data.tab.indices
            rects = self._gui_data.tab.frame.rects

            self._gui_data.tab.current_index_tmp = None
            for i_idx in indices:
                i_rect = rects[i_idx]
                if i_rect.contains(p):
                    self._gui_data.tab.current_index_tmp = i_idx
                    break

            self._update_from_index_temp()

        def _do_press_release(self, event):
            self._update_from_index_temp()

            self._gui_data.tab.current_index_tmp = None

        def _update_from_index_temp(self):
            if self._gui_data.tab.current_index_tmp is not None:
                index_tmp = self._gui_data.tab.current_index_tmp
                if index_tmp != self._tab_model.data.tab.current_index:
                    self._tab_model.data.tab.current_index = index_tmp
                    self._widget.current_index_change_accepted.emit(index_tmp)

            self.update()

        def _do_wheel(self, event):
            delta = event.angleDelta().y()
            percent_pre = self._tab_model.data.scale_percent

            step = 0.05

            if delta > 0:
                percent = percent_pre+step
            else:
                percent = percent_pre-step

            percent = max(min(percent, 8.0), 0.5)
            self._tab_model.data.scale_percent = percent

            for i in self._tab_model.get_all_pages():
                i.model.set_scale_percent(percent)

    def __init__(self, *args, **kwargs):
        super(QtToolTabBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setFixedHeight(self.H)

        self._init_widget(self)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._model.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._model._update_hover(True)
            elif event.type() == QtCore.QEvent.ToolTip:
                self._model._do_popup_tool_tip(event)
            elif event.type() == QtCore.QEvent.Leave:
                self._model._update_hover(False)
                self._model._clear_flags()
            elif event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                if event.button() == QtCore.Qt.LeftButton:
                    self._model._do_press_click(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._model._do_press_move(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._model._do_press_release(event)
                self._model._clear_flags()
        return False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._model.draw(painter)

    def wheelEvent(self, event):
        if _qt_core.QtUtil.is_ctrl_modifier():
            self._model._do_wheel(event)
            event.accept()
        else:
            super(QtToolTabBar, self).wheelEvent(event)


class QtToolTabWidget(
    QtWidgets.QWidget,
    _base._AbsWidget
):
    class Model(
        _base._AbsModel,
        _base._AbsAction
    ):
        def __init__(self, *args, **kwargs):
            super(QtToolTabWidget.Model, self).__init__(*args, **kwargs)

            self._init_action()

            self._data.update(
                dict(
                    tab=_gui_core.DictOpt(
                        current_index=0
                    ),
                    scale_percent=1.0
                )
            )

            self._gui_data.update(
                dict(
                    refresh_flag=False,
                    head=_gui_core.DictOpt(
                        rect=QtCore.QRect()
                    ),
                    viewport=_gui_core.DictOpt(
                        rect=QtCore.QRect()
                    ),
                    pages=collections.OrderedDict()
                )
            )

        def update(self):
            # x, y = 0, 0
            # w, h = self._widget.width(), self._widget.height()

            self._widget._tab_bar.model.update_from(self)

        def draw(self, painter):
            pass

        def mark_refresh_flag(self):
            self.set_refresh_flag(True)

        def get_refresh_flag(self):
            return self._gui_data.refresh_flag

        def set_refresh_flag(self, boolean):
            self._gui_data.refresh_flag = boolean

        def get_current_page_index(self):
            return self._widget._stack.currentIndex()

        def get_page_count(self):
            return self._widget._stack.count()

        def add_page(self, path, widget):
            index = self.get_page_count()

            # add scroll area
            scroll_area = QtToolTabWidget.QtScrollArea()
            self._widget._stack.addWidget(scroll_area)
            scroll_area._lot.addWidget(widget)
            self._gui_data.pages[path] = widget
            widget.model.set_path(path)
            widget.model.set_index(index)
            self.mark_refresh_flag()

        def get_all_pages(self):
            return self._gui_data.pages.values()

        def get_page_at(self, index):
            return self._widget._stack.widget(index)

        def set_current_page_index(self, index):
            self._widget._stack.setCurrentIndex(index)

    class QtScrollArea(QtWidgets.QScrollArea):
        def __init__(self, *args, **kwargs):
            super(QtToolTabWidget.QtScrollArea, self).__init__(*args, **kwargs)
            self.setFocusPolicy(QtCore.Qt.NoFocus)
            self.setWidgetResizable(True)

            self._wgt = QtWidgets.QWidget()
            self.setWidget(self._wgt)
            self._wgt.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

            self._lot = QtWidgets.QVBoxLayout(self._wgt)
            self._lot.setContentsMargins(*[0]*4)
            self._lot.setSpacing(2)
            self._lot.setAlignment(QtCore.Qt.AlignTop)

            self.setStyleSheet(_qt_core.QtStyle.get('QScrollArea'))

            self.verticalScrollBar().setStyleSheet(_qt_core.QtStyle.get('QScrollBar'))
            self.horizontalScrollBar().setStyleSheet(_qt_core.QtStyle.get('QScrollBar'))

    def __init__(self, *args, **kwargs):
        super(QtToolTabWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._init_widget(self)

        lot = QtWidgets.QVBoxLayout(self)
        lot.setContentsMargins(*[0]*4)
        lot.setSpacing(2)

        # must instance by self as parent
        self._tab_bar = QtToolTabBar(self)
        lot.addWidget(self._tab_bar)

        self._stack = QtWidgets.QStackedWidget()
        lot.addWidget(self._stack)

        self._lot = self._stack.layout()

        self._tab_bar.current_index_change_accepted.connect(self._model.set_current_page_index)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._model.update()
        return False


class QtToolPage(
    QtWidgets.QWidget,
    _base._AbsWidget
):
    class Model(
        _base._AbsModel,
        _base._AbsLabel,
        _base._AbsAction
    ):
        def __init__(self, *args, **kwargs):
            super(QtToolPage.Model, self).__init__(*args, **kwargs)

            self._init_label()
            self._init_action()

            self._gui_data.scale_percent = 1.0

        def add_group(self, widget):
            self._widget._lot.addWidget(widget)

        def get_all_groups(self):
            return _qt_core.QtUtil.get_all_widgets_at(self._widget._lot)

        def set_scale_percent(self, value):
            for i in self.get_all_groups():
                i.model.set_scale_percent(value)

    def __init__(self, *args, **kwargs):
        super(QtToolPage, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._init_widget(self)

        self._lot = QtWidgets.QVBoxLayout(self)
        self._lot.setContentsMargins(*[0]*4)
        self._lot.setSpacing(2)
        self._lot.setAlignment(QtCore.Qt.AlignTop)


class QtToolGroup(
    QtWidgets.QWidget,
    _base._AbsWidget
):
    H = 24
    ICN_H = 12

    class Model(
        _base._AbsModel,
        _base._AbsFrame, _base._AbsLabel,
        _base._AbsAction, _base._AbsPress, _base._AbsExpand,
    ):
        def __init__(self, *args, **kwargs):
            super(QtToolGroup.Model, self).__init__(*args, **kwargs)

            self._init_frame()
            self._init_label()
            self._init_action()
            self._init_press()
            self._init_expand()

            self._gui_data.update(
                dict(
                    column_count=1,
                    head=_gui_core.DictOpt(
                        rect=QtCore.QRect(),
                        border_color=_qt_core.QtRgba.BdrHead,
                        background_color=_qt_core.QtRgba.BkgHead,
                        height=QtToolGroup.H
                    )
                )
            )

            self._gui_data.frame.height = QtToolGroup.H
            self._gui_data.frame.border_color = _qt_core.QtRgba.BdrHead
            self._gui_data.frame.background_color = _qt_core.QtRgba.BkgHead

            self._gui_data.label.text_color = QtGui.QColor(191, 191, 191, 255)
            self._gui_data.label.text_font = _qt_core.QtFont.generate(size=9, weight=75)

            self._gui_data.tip.action_tip = '"LMB-click" to expand "on" / "off"'

        def update(self):
            x, y = 0, 0
            w, h = self._widget.width(), self._widget.height()
            head_frame_w =  head_frame_h = self._gui_data.frame.height

            if self.is_action_flag_matching(self.ActionFlags.PressClicked) is True:
                x += 2
                y += 2
                w -= 2
                head_frame_h -= 2

            self._gui_data.frame.rect.setRect(
                x+1, y+1, w-2, head_frame_h-2
            )

            head_icon_w, head_icon_h = self._gui_data.expand.icon.width, self._gui_data.expand.icon.height

            self._gui_data.expand.icon.rect.setRect(
                x+(head_frame_w-head_icon_w)/2, y+(head_frame_h-head_icon_h)/2, head_icon_w, head_icon_h
            )
            self._gui_data.label.rect.setRect(
                x+head_frame_w, y, w-head_frame_w, head_frame_h
            )

            self._widget.update()

        def draw(self, painter):
            _qt_core.QtDrawBase._draw_frame(
                painter,
                rect=self._gui_data.frame.rect,
                border_color=self._gui_data.frame.border_color,
                background_color=self._gui_data.frame.background_color
            )
            _qt_core.QtDrawBase._draw_icon_by_file(
                painter,
                rect=self._gui_data.expand.icon.rect,
                file_path=self._gui_data.expand.icon.file
            )
            _qt_core.QtDrawBase._draw_name_text(
                painter,
                rect=self._gui_data.label.rect,
                text=self._gui_data.label.text,
                text_color=self._gui_data.label.text_color,
                text_font=self._gui_data.label.text_font,
            )

        def set_expanded(self, boolean):
            if boolean != self._data.expand_flag:
                self._data.expand_flag = boolean
                self._update_expand()

        def is_expanded(self):
            return self._data.expand_flag

        def _swap_expand(self):
            self.set_expanded(not self.is_expanded())

        def _update_expand(self):
            self._gui_data.expand.icon.file = [
                self._gui_data.expand.icon.file_0, self._gui_data.expand.icon.file_1
            ][self._data.expand_flag]

            self._widget._viewport.setVisible(self._data.expand_flag)

            self._update_widget_minimum_height()

        def _update_widget_minimum_height(self):
            if self._data.expand_flag is True:
                size = self._widget._lot.minimumSize()
                self._widget.setMinimumHeight(size.height()+self._widget.H)
            else:
                self._widget.setMinimumHeight(self._widget.H)

        def _do_press_click(self, event):
            p = event.pos()

            if self._gui_data.frame.rect.contains(p):
                self.set_action_flag(self.ActionFlags.PressClicked)

            self.update()

        def _do_press_release(self, event):
            if self.is_action_flag_matching(self.ActionFlags.PressClicked) is True:
                self._swap_expand()

        def _clear_flags(self):
            self.clear_action_flag()

            self.update()

        def get_tool_count(self):
            return self._widget._lot.count()

        def add_tool(self, widget):
            column_count = self._gui_data.column_count
            idx = self.get_tool_count()
            column = idx%column_count
            row = int(idx/column_count)
            self._widget._lot.addWidget(widget, row, column)

            self._update_widget_minimum_height()

            self.update()

        def get_all_tools(self):
            return _qt_core.QtUtil.get_all_widgets_at(self._widget._lot)

        def set_scale_percent(self, value):
            for i in self.get_all_tools():
                i.model.set_scale_percent(value)

            self._update_widget_minimum_height()

        def set_column_count(self, value):
            self._gui_data.column_count = value

    def __init__(self, *args, **kwargs):
        super(QtToolGroup, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setMinimumHeight(self.H)

        self._init_widget(self)

        lot = QtWidgets.QVBoxLayout(self)
        lot.setContentsMargins(0, self.H, 0, 0)
        lot.setSpacing(2)

        self._viewport = QtWidgets.QWidget()
        lot.addWidget(self._viewport)

        self._lot = QtWidgets.QGridLayout(self._viewport)
        self._lot.setContentsMargins(0, 2, 0, 0)
        self._lot.setSpacing(2)

        self._model._update_expand()

        self.setAcceptDrops(True)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._model.update()
            elif event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                if event.button() == QtCore.Qt.LeftButton:
                    self._model._do_press_click(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._model._do_press_release(event)

                self._model._clear_flags()
        return False

    # drop
    def dragEnterEvent(self, event):
        # mime_data = event.mimeData()
        # keys = mime_data.formats()
        # for i_key in keys:
        #     print(i_key, mime_data.data(i_key))
        return

    def dragMoveEvent(self, event):
        # print('B')
        return

    def dropEvent(self, event):
        # print('ABC')
        return

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._model.draw(painter)


class QtTool(
    QtWidgets.QWidget,
    _base._AbsWidget
):
    H = 40
    ICN_H = 20

    press_clicked = _qt_core.qt_signal()

    class Model(
        _base._AbsModel,
        _base._AbsFrame, _base._AbsLabel, _base._AbsIcon,
        _base._AbsAction, _base._AbsPress, _base._AbsMenu
    ):
        def __init__(self, *args, **kwargs):
            super(QtTool.Model, self).__init__(*args, **kwargs)

            self._init_frame()
            self._init_label()
            self._init_icon()
            self._init_action()
            self._init_press()
            self._init_menu()

            self._data.update(
                dict(
                    scale_percent=1.0
                )
            )

            self._gui_data.frame.basic_height = self._gui_data.frame.height = QtTool.H
            self._gui_data.frame.border_color = _qt_core.QtRgba.BdrButton
            self._gui_data.frame.background_color = _qt_core.QtRgba.BkgButton
            self._gui_data.frame.hover.border_color = _qt_core.QtRgba.BdrButtonHoverA
            self._gui_data.frame.hover.background_color = _qt_core.QtRgba.BkgButtonHoverA

            self._gui_data.label.text_color = QtGui.QColor(223, 223, 223, 255)
            self._gui_data.label.text_word_warp = True
            self._gui_data.label.text_font = _qt_core.QtFont.generate(size=9)

            self._gui_data.tip.action_tip = '"LMB-click" to execute'

        def update(self):
            x, y = 0, 0
            w, h = self._widget.width(), self._widget.height()

            mrg = 4

            frame_w, frame_h = self._gui_data.frame.height, self._gui_data.frame.height

            if self.is_action_flag_matching(self.ActionFlags.PressClicked) is True:
                x += 2
                y += 2
                w -= 2
                frame_h -= 2

            c_x = x
            c_w = w
            if self._gui_data.icon_enable is True:
                icn_frm_w, icn_frm_h = frame_w, frame_h
                icn_margin = self._gui_data.icon.margin
                icn_w, icn_h = icn_frm_w-icn_margin*2, icn_frm_h-icn_margin*2
                self._gui_data.icon.rect.setRect(
                    c_x+(icn_frm_w-icn_w)/2, y+(icn_frm_h-icn_h)/2, icn_w, icn_h,
                )
                c_x += icn_frm_w
            if self._gui_data.label_enable is True:
                c_x = max(mrg, c_x)
                lbl_percent = self._gui_data.label.percent
                lbl_h = frame_h*lbl_percent
                # self._gui_data.label.text_font = _qt_core.QtFont.generate_2(size=lbl_h)
                self._gui_data.label.rect.setRect(
                    c_x, y, c_w-c_x-mrg, h
                )

            if self._gui_data.menu_enable is True:
                menu_icon_percent = self._gui_data.menu.icon.percent
                menu_icn_w, menu_icn_h = int(frame_h*menu_icon_percent), int(frame_h*menu_icon_percent)

                self._gui_data.menu.icon.rect.setRect(
                    w-menu_icn_w, y+frame_h-menu_icn_h, menu_icn_w, menu_icn_h
                )

                menu_frm_w, menu_frm_h = menu_icn_w*2, menu_icn_h*2
                self._gui_data.menu.rect.setRect(
                    w-menu_frm_w, y+frame_h-menu_frm_h, menu_frm_w, menu_frm_h
                )

            self._gui_data.frame.rect.setRect(
                x+1, y+1, c_w-2, frame_h-2
            )

            self._widget.update()

        def draw(self, painter):
            _qt_core.QtDrawBase._draw_frame(
                painter,
                rect=self._gui_data.frame.rect,
                border_color=self._gui_data.frame.border_color,
                background_color=self._gui_data.frame.background_color,
                border_radius=3
            )

            if self._gui_data.icon_enable is True:
                _qt_core.QtDrawBase._draw_icon_by_file(
                    painter,
                    rect=self._gui_data.icon.rect,
                    file_path=self._gui_data.icon.file
                )
            if self._gui_data.menu_enable is True:
                _qt_core.QtDrawBase._draw_icon_by_file(
                    painter,
                    rect=self._gui_data.menu.icon.rect,
                    file_path=self._gui_data.menu.icon.file
                )

            if self._gui_data.label_enable is True:
                _qt_core.QtDrawBase._draw_name_text(
                    painter,
                    rect=self._gui_data.label.rect,
                    text=self._gui_data.label.text,
                    text_color=self._gui_data.label.text_color,
                    text_font=self._gui_data.label.text_font,
                    text_word_warp=self._gui_data.label.text_word_warp,
                )

            if self._gui_data.hover_flag is True:
                _qt_core.QtDrawBase._draw_frame(
                    painter,
                    rect=self._gui_data.frame.rect,
                    border_color=self._gui_data.frame.hover.border_color,
                    background_color=self._gui_data.frame.hover.background_color,
                    border_radius=3
                )

        def set_scale_percent(self, percent):
            basic_h = self._gui_data.frame.basic_height
            self._data.scale_percent = percent

            h = int(basic_h*percent)
            self._widget.setFixedHeight(h)
            self._gui_data.frame.height = h

            self.update()

        def set_icon_file(self, file_path):
            if file_path:
                self._gui_data.icon_enable = True
                self._gui_data.icon.file = file_path

        def _do_press_click(self, event):
            p = event.pos()

            if self._gui_data.menu.rect.contains(p):
                self._do_popup_menu()
            elif self._gui_data.frame.rect.contains(p):
                self.set_action_flag(self.ActionFlags.PressClicked)

            self.update()

        def _do_press_move(self, event):
            self.set_action_flag(self.ActionFlags.PressMove)

        def _do_press_release(self, event):
            if self.is_action_flag_matching(self.ActionFlags.PressClicked) is True:
                self._widget.press_clicked.emit()

        def _clear_flags(self):
            self.clear_action_flag()

            self.update()

        def _update_hover(self, boolean):
            self._gui_data.hover_flag = boolean
            self.update()

        @staticmethod
        def _exec_script(script):
            exec (script)

        def connect_press_clicked_to(self, arg):
            if isinstance(arg, six.string_types):
                self._widget.press_clicked.connect(functools.partial(self._exec_script, arg))
            elif isinstance(arg, (types.FunctionType, types.MethodType, types.LambdaType, functools.partial)):
                self._widget.press_clicked.connect(arg)

    def __init__(self, *args, **kwargs):
        super(QtTool, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setFixedHeight(self.H)

        self._init_widget(self)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._model.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._model._update_hover(True)
            elif event.type() == QtCore.QEvent.Leave:
                self._model._update_hover(False)
                self._model._clear_flags()
            elif event.type() in {QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick}:
                if event.button() == QtCore.Qt.LeftButton:
                    self._model._do_press_click(event)
                elif event.button() == QtCore.Qt.RightButton:
                    self._model._do_popup_menu()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._model._do_press_move(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._model._do_press_release(event)

                self._model._clear_flags()
        return False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._model.draw(painter)