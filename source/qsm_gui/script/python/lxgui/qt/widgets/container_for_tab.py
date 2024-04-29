# coding=utf-8
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts


class QtHTabGroup(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtWidgetBaseDef,
    _qt_abstracts.AbsQtFrameBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_(self.rect())
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, rect):
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        self._rect_frame_draw.setRect(
            x, y, w, h
        )

        m_l, m_t, m_r, m_b = self._tab_view_margins
        t_w, t_h = self._tab_w, self._tab_h
        c_t_f_x, c_t_f_y = x, y
        c_t_f_w, c_t_f_h = w, t_h

        self._layout.setContentsMargins(
            m_l, t_h+m_t, m_r, m_b
        )

        c_x, c_y = x, y

        tab_items = self._tab_item_stack.get_all_items()
        if tab_items:
            for i_index, i_tab_item in enumerate(tab_items):
                i_name_text = i_tab_item.get_name()
                if i_name_text is not None:
                    i_text_width = self._get_text_draw_width_(
                        i_name_text
                    )
                else:
                    i_text_width = t_w
                # compute tab width
                i_t_w = i_text_width+t_h*2
                self._item_width_dict[i_index] = i_t_w

            scroll_value = 0
            widths = self._item_width_dict.values()
            for i_index, i_tab_item in enumerate(tab_items):
                i_rect = i_tab_item.get_rect()
                i_widget = i_tab_item.get_widget()
                i_draw_rect = i_tab_item.get_draw_rect()

                i_x = sum(widths[:i_index])
                i_w = self._item_width_dict[i_index]

                i_draw_rect.setRect(
                    c_x + i_x - scroll_value, y, i_w, t_h
                )
                i_rect.setRect(
                    c_x + i_x - scroll_value, y, i_w, t_h
                )
                if i_index == self._index_current:
                    i_widget.show()
                else:
                    i_widget.hide()

        self._tab_bar_draw_rect.setRect(
            x, y, w, t_h-1
        )
        self._tab_bar_rect.setRect(
            c_t_f_x, c_t_f_y, c_t_f_w, c_t_f_h
        )

    def __init__(self, *args, **kwargs):
        super(QtHTabGroup, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )

        self._init_widget_base_def_(self)
        self._init_frame_base_def_(self)

        self._init_action_base_def_(self)

        self._tab_item_stack = _qt_core.GuiQtModForTabItemStack(self)

        self._tab_view_margins = 2, 2, 2, 2
        self._tab_w, self._tab_h = 24, 24

        self._tab_bar_rect = QtCore.QRect()
        self._tab_bar_draw_rect = QtCore.QRect()

        self._item_width_dict = {}

        self._index_current = 0

        self._index_press_tmp = None
        self._index_press = None
        self._index_hover = None

        self._layout = _qt_core.QtHBoxLayout(self)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._clear_item_hover_()
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._index_press_tmp = self._compute_press_index_loc_(
                    event.pos()
                )
                if event.button() == QtCore.Qt.LeftButton:
                    if self._index_press_tmp is not None:
                        self._set_action_flag_(self.ActionFlag.Press)
                        self._update_item_index_pressed_(self._index_press_tmp)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.button() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    # when drag press move less than 10px, do press release also
                    if self._get_action_flag_is_match_(self.ActionFlag.Press):
                        # send signal in release action
                        self._do_press_release_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()

                self._index_press_tmp = None
                self._index_hover = None
                self._clear_all_action_flags_()
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)
                return True
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._draw_virtual_buttons_(
            self._tab_bar_draw_rect,
            virtual_items=self._tab_item_stack.get_all_items(),
            index_hover=self._index_hover,
            index_pressed=self._index_press,
            index_current=self._get_current_index_(),
        )

    def _add_widget_(self, widget, *args, **kwargs):
        # widget.setParent(self)
        # widget.setParent(self)
        self._layout.addWidget(widget)
        tab_item = self._tab_item_stack.create_item(widget)
        if 'key' in kwargs:
            tab_item.set_key(kwargs['key'])
        if 'name' in kwargs:
            tab_item.set_name(kwargs['name'])
        if 'icon_name_text' in kwargs:
            tab_item.set_icon_text(kwargs['name'])
        if 'tool_tip' in kwargs:
            tab_item.set_tool_tip(kwargs['tool_tip'])

        self._refresh_widget_all_()

    def _update_index_current_(self, index):
        self._index_current = index
        self._refresh_widget_all_()

    def _get_current_index_(self):
        return self._index_current
    
    def _update_item_index_pressed_(self, index):

        if index != self._index_press:
            self._index_press = index

            self._refresh_widget_all_()
    
    def _do_press_release_(self, event):
        if self._index_press_tmp is not None:
            self._switch_current_to_(
                self._index_press_tmp
            )
    
    def _switch_current_to_(self, index):
        self._update_index_current_(index)
        self._index_press = None
        self._refresh_widget_all_()

    def _clear_item_hover_(self):
        self._index_hover = None
        self._refresh_widget_draw_()

    def _do_show_tool_tip_(self, event):
        if self._index_hover is not None:
            key = self._tab_item_stack.get_key_at(self._index_hover)
            if key is None:
                title = self._tab_item_stack.get_name_at(self._index_hover)
                tool_tip = self._tab_item_stack.get_tool_tip_at(self._index_hover)
            else:
                title = 'N/a'
                tool_tip = 'N/a'

            css = _qt_core.GuiQtUtil.generate_tool_tip_css(
                title,
                content=tool_tip,
                action_tip=[
                    '"LMB-click" to show this page',
                    '"MMB-wheel" to scroll to other page',
                    '"RMB-click" to show more actions for this page',
                ]
            )
            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _compute_press_index_loc_(self, p):
        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.get_rect().contains(p):
                    return i_index

    def _do_hover_move_(self, event):
        p = event.pos()
        self._index_hover = None
        if self._tab_bar_rect.contains(p):
            for i_index, i_tab_item in enumerate(self._tab_item_stack.get_all_items()):
                if i_tab_item.rect.contains(p):
                    self._index_hover = i_index
                    break

        self._refresh_widget_draw_()

    def _do_wheel_(self, event):
        pass
