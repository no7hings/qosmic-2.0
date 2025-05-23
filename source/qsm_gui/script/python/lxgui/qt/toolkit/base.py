# coding:utf-8
import enum

from ... import core as _gui_core

from .. import core as _qt_core

from ..widgets import utility as _utility

from ..core.wrap import *


class ActionFlags(enum.IntEnum):
    PressClicked = 0x00

    PressMove = 0x20


class _AbsModel(object):
    def __init__(self, widget):
        self._widget = widget
        self._data = _gui_core.DictOpt(
            path=None
        )
        self._gui_data = _gui_core.DictOpt(
            index=0,
            path=None,
        )

    @property
    def widget(self):
        return self._widget

    @property
    def data(self):
        return self._data

    @property
    def gui_data(self):
        return self._gui_data

    def set_index(self, value):
        self._gui_data.index = value

    def get_index(self):
        return self._gui_data.index

    def set_path(self, path):
        self._data.path = path

    def get_path(self):
        return self._data.path


class _AbsFrame:
    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_frame(self):
        self.gui_data.update(
            dict(
                frame=_gui_core.DictOpt(
                    rect=QtCore.QRect(),
                    border_color=_qt_core.QtRgba.Transparent,
                    background_color=_qt_core.QtRgba.Transparent,
                    basic_height=20,
                    height=20,
                    hover=_gui_core.DictOpt(
                        border_color=_qt_core.QtRgba.Transparent,
                        background_color=_qt_core.QtRgba.Transparent,
                    )
                )
            )
        )


class _AbsLabel:
    @property
    def widget(self):
        raise NotImplementedError()

    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_label(self):
        self.gui_data.update(
            dict(
                label_enable=False,
                label=_gui_core.DictOpt(
                    rect=QtCore.QRect(),
                    text=None,
                    text_color=QtGui.QColor(223, 223, 223, 255),
                    text_font=_qt_core.QtFont.generate(size=8),
                    text_word_warp=False,
                    text_option=QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter,
                    percent=0.8,
                    height=16,
                ),
                tip=_gui_core.DictOpt(
                    tool_tip=None,
                    action_tip=None,
                )
            )
        )

    def set_label(self, text):
        if text:
            self.gui_data.label_enable = True
            self.gui_data.label.text = text
            self._update_tip()

    def get_label(self):
        return self.gui_data.label.text

    def set_tool_tip(self, text):
        if text:
            self.gui_data.tip.tool_tip = text
            self._update_tip()

    def get_tool_tip(self):
        return self.gui_data.tip.tool_tip

    def set_action_tool_tip(self, text):
        if text:
            self.gui_data.tip.action_tip = text
            self._update_tip()

    def _update_tip(self):
        css = _qt_core.QtUtil.generate_tool_tip_css(
            self.gui_data.label.text,
            self.gui_data.tip.tool_tip,
            action_tip=self.gui_data.tip.action_tip
        )
        self.widget.setToolTip(css)


class _AbsIcon:
    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_icon(self):
        self.gui_data.update(
            dict(
                icon_enable=True,
                icon=_gui_core.DictOpt(
                    rect=QtCore.QRect(),
                    file=_gui_core.GuiIcon.get('application/python'),
                    margin=2, percent=0.8,
                    width=16, height=16,
                )
            )
        )


class _AbsAction:
    ActionFlags = ActionFlags

    @property
    def gui_data(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def _init_action(self):
        self.gui_data.update(
            dict(
                hover_flag=False,
                action=_gui_core.DictOpt(
                    flag=None,
                    sub_flag=None,
                )
            )
        )

    def set_action_flag(self, flag):
        self.gui_data.action.flag = flag

    def set_action_sub_flag(self, flag):
        self.gui_data.action.sub_flag = flag

    def is_action_flag_matching(self, *args):
        return self.gui_data.action.flag in args

    def is_action_sub_flag_matching(self, *args):
        return self.gui_data.action.sub_flag in args

    def clear_action_flag(self):
        self.gui_data.action.flag = None

    def clear_action_sub_flag(self):
        self.gui_data.action.sub_flag = None

    def _update_hover(self, boolean):
        pass

    def _clear_flags(self):
        self.clear_action_flag()

        self.update()


class _AbsExpand:
    @property
    def data(self):
        raise NotImplementedError()

    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_expand(self):
        self.data.update(
            expand_flag=False
        )
        self.gui_data.update(
            dict(
                expand=_gui_core.DictOpt(
                    icon=_gui_core.DictOpt(
                        rect=QtCore.QRect(),
                        file_0=_gui_core.GuiIcon.get('expand-close'),
                        file_1=_gui_core.GuiIcon.get('expand-open'),
                        file=None,
                        width=12, height=12,
                    )
                )
            )
        )


class _AbsPress:
    def _init_press(self):
        pass

    def _do_press_click(self, event):
        pass

    def _do_press_move(self, event):
        pass

    def _do_press_release(self, event):
        pass


class _AbsMenu:
    QT_MENU_CLS = _utility.QtMenu

    @property
    def widget(self):
        raise NotImplementedError()

    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_menu(self):
        self.gui_data.update(
            dict(
                menu_enable=False,
                menu=_gui_core.DictOpt(
                    data=None,
                    data_generate_fnc=None,
                    content=None,
                    content_generate_fnc=None,
                    rect=QtCore.QRect(),
                    icon=_gui_core.DictOpt(
                        rect=QtCore.QRect(),
                        file=_gui_core.GuiIcon.get('state/popup'),
                        margin=2, percent=0.25,
                        width=16, height=16
                    )
                )
            )
        )

    def set_menu_data(self, data):
        if data:
            self.gui_data.menu_enable = True
            self.gui_data.menu.data = data

    def set_menu_content(self, content):
        self.gui_data.menu.content = content

    def _auto_generate_menu(self, qt_menu):
        if qt_menu is None:
            qt_menu = self.QT_MENU_CLS(self.widget)
            if self.gui_data.label.text is not None:
                qt_menu._set_title_text_(self.gui_data.label.text)
        return qt_menu

    def _do_popup_menu(self):
        qt_menu = None
        # add menu content first, menu content operate always clear all
        # when generate function is defining, use generate data
        if self.gui_data.menu.content_generate_fnc is not None:
            menu_content = self.gui_data.menu.content_generate_fnc()
            if menu_content:
                if menu_content.get_is_empty() is False:
                    qt_menu = self._auto_generate_menu(qt_menu)
                    qt_menu._set_menu_content_(menu_content)
                    qt_menu._set_show_()
        else:
            menu_content = self.gui_data.menu.content
            if menu_content:
                if menu_content.get_is_empty() is False:
                    qt_menu = self._auto_generate_menu(qt_menu)
                    qt_menu._set_menu_content_(menu_content)
                    qt_menu._set_show_()

        if self.gui_data.menu.data_generate_fnc is not None:
            qt_menu = self._auto_generate_menu(qt_menu)
            menu_data = self.gui_data.menu.data_generate_fnc()
            if menu_data:
                qt_menu._set_menu_data_(menu_data)
                qt_menu._set_show_()
        else:
            menu_data = self.gui_data.menu.data
            if menu_data:
                qt_menu = self._auto_generate_menu(qt_menu)
                qt_menu._set_menu_data_(menu_data)
                qt_menu._set_show_()


class _AbsWidget:
    class Model:
        pass

    def _init_widget(self, widget):
        self._model = self.Model(widget)
    
    @property
    def model(self):
        return self._model
