# coding:utf-8
import sys

import collections

import functools

import json

import lxbasic.core as bsc_core

from lxgui.qt.core.wrap import *

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

from ...core import base as _scn_cor_base


class _AbsCustomGui(QtWidgets.QWidget):
    QT_INPUT_WGT_CLS = None

    def __init__(self, *args, **kwargs):
        super(_AbsCustomGui, self).__init__(*args, **kwargs)

        self._param = None

        self._wgt_lot = QtWidgets.QHBoxLayout(self)
        self._wgt_lot.setContentsMargins(*[0]*4)
        self._wgt_lot.setSpacing(2)

    def _build_input_wgt(self):
        pass

    def _set_param(self, param):
        self._param = param
        self._set_label(param.get_label())
        self._build_input_wgt()

    def _accept_value(self, value):
        pass

    def _set_label(self, text):
        pass

    def _set_value(self, value):
        pass

    def _set_lock_mode(self):
        pass

    def _set_label_width(self, w):
        pass

    def _get_label_width(self):
        return -1

    def _refresh(self):
        pass

    def _exec_script_fnc(self, script):
        if script:
            node = self._param.node
            # noinspection PyRedundantParentheses
            exec (script)


# button
class ButtonGui(_AbsCustomGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtPressButton

    def __init__(self, *args, **kwargs):
        super(ButtonGui, self).__init__(*args, **kwargs)

        self.setFixedHeight(24)

        self._input_wgt = self.QT_INPUT_WGT_CLS()
        self._wgt_lot.addWidget(self._input_wgt)

        self._input_wgt.press_clicked.connect(self._exec_script)

    def _exec_script(self):
        self._exec_script_fnc(self._param.options.get('script'))

    def _set_label(self, text):
        self._input_wgt._set_name_text_(text)


class ButtonsGui(_AbsCustomGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtPressButton

    def __init__(self, *args, **kwargs):
        super(ButtonsGui, self).__init__(*args, **kwargs)

        self.setFixedHeight(24)

    def _build_input_wgt(self):
        ui_language = bsc_core.BscEnviron.get_gui_language()
        options = self._param.get_options()
        data = options.get('data')
        if data:
            for i in data:
                i_input_wgt = self.QT_INPUT_WGT_CLS()
                self._wgt_lot.addWidget(i_input_wgt)

                i_gui_name = i.get('gui_name')
                if ui_language == 'chs':
                    i_label = i.get('gui_name_chs')
                else:
                    i_label = i_gui_name
                i_label = i_label or 'N/a'
                i_input_wgt._set_name_text_(i_label)

                i_script = i.get('script')
                if i_script:
                    i_input_wgt.press_clicked.connect(functools.partial(self._exec_script_fnc, i_script))


class _AbsTypedParamGui(QtWidgets.QWidget):
    QT_INPUT_WGT_CLS = None

    def __init__(self, *args, **kwargs):
        super(_AbsTypedParamGui, self).__init__(*args, **kwargs)

        self._param = None

        self._wgt_lot = QtWidgets.QHBoxLayout(self)
        self._wgt_lot.setContentsMargins(*[0]*4)
        self._wgt_lot.setSpacing(2)

        self._label_wgt = gui_qt_widgets.QtTextItem()
        self._wgt_lot.addWidget(self._label_wgt)

        self._input_wgt = self.QT_INPUT_WGT_CLS()
        self._wgt_lot.addWidget(self._input_wgt)

    def _set_param(self, param):
        self._param = param
        self._set_label(param.get_label())
        self._set_value(self._param.get_value())
        self._connect_value_change()

    def _connect_value_change(self):
        pass

    def _accept_value(self, value):
        self._param._set_value(value)
        # sys.stdout.write(
        #     'set value: {}.\n'.format(self._param.get_path())
        # )

    def _set_label(self, text):
        self._label_wgt._set_name_text_(text)

    def _set_value(self, value):
        self._input_wgt._set_value_(value)

    def _set_lock_mode(self):
        self._input_wgt._set_entry_enable_(False)

    def _set_label_width(self, w):
        self._label_wgt.setFixedWidth(w)

    def _get_label_width(self):
        return self._label_wgt._get_name_text_draw_width_()+16

    def _refresh(self):
        self._set_value(self._param.get_value())


class JsonGui(_AbsTypedParamGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtInputForContent

    def __init__(self, *args, **kwargs):
        super(JsonGui, self).__init__(*args, **kwargs)

        self.setFixedHeight(96)

        self._input_wgt._get_resize_handle_()._set_resize_target_(self)
        self._input_wgt._set_resize_enable_(True)
        self._input_wgt._set_input_entry_drop_enable_(True)
        self._input_wgt._set_item_value_entry_enable_(True)
        self._input_wgt._set_size_policy_height_fixed_mode_()

        self._input_wgt._set_entry_enable_(True)

    def _set_value(self, value):
        self._input_wgt._set_value_(
            json.dumps(value, indent=4)
        )

    def _accept_value(self, value):
        if self._param._set_value(
            json.loads(value, object_pairs_hook=collections.OrderedDict)
        ):
            sys.stdout.write(
                'update value at: {}.\n'.format(self._param.get_path())
            )

    def _connect_value_change(self):
        self._input_wgt.input_value_accepted.connect(
            self._accept_value
        )


# constant
class ConstantGui(_AbsTypedParamGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtInputForConstant

    def __init__(self, *args, **kwargs):
        super(ConstantGui, self).__init__(*args, **kwargs)

        self.setFixedHeight(24)

    def _set_value_type(self, type_):
        self._input_wgt._set_value_type_(type_)

    def _connect_value_change(self):
        self._input_wgt.input_value_accepted.connect(
            self._accept_value
        )

    def _accept_value(self, value):
        if self._param._set_value(value):
            sys.stdout.write(
                'update value at: {}.\n'.format(self._param.get_path())
            )


class PathGui(_AbsTypedParamGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtInputForConstant

    def __init__(self, *args, **kwargs):
        super(PathGui, self).__init__(*args, **kwargs)

        self._input_wgt._set_value_entry_validator_use_as_path_()

    def _connect_value_change(self):
        self._input_wgt.input_value_accepted.connect(
            self._accept_value
        )

    def _accept_value(self, value):
        if self._param._set_value(value):
            sys.stdout.write(
                'update value at: {}.\n'.format(self._param.get_path())
            )


class TupleGui(_AbsTypedParamGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtInputForTuple

    def __init__(self, *args, **kwargs):
        super(TupleGui, self).__init__(*args, **kwargs)

    def _set_value_type(self, ptype):
        self._input_wgt._set_value_type_(ptype)

    def _set_value_size(self, size):
        self._input_wgt._set_value_size_(size)


class ArrayGui(_AbsTypedParamGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtInputForTuple

    def __init__(self, *args, **kwargs):
        super(ArrayGui, self).__init__(*args, **kwargs)

    def _set_value_type(self, ptype):
        self._input_wgt._set_value_type_(ptype)

    def _set_value_size(self, size):
        self._input_wgt._set_value_size_(size)


# boolean
class BooleanGui(_AbsTypedParamGui):
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtCheckButton

    def __init__(self, *args, **kwargs):
        super(BooleanGui, self).__init__(*args, **kwargs)

        self.setFixedHeight(24)

    def _connect_value_change(self):
        self._input_wgt.check_toggled.connect(
            self._accept_value
        )

    def _set_label(self, text):
        self._input_wgt._set_name_text_(text)

    def _get_label_width(self):
        return 0

    def _set_value(self, value):
        self._input_wgt._set_checked_(value)


# storage
class _AbsStorageGui(_AbsTypedParamGui):
    
    QT_INPUT_WGT_CLS = gui_qt_widgets.QtInputForStorage
    
    def __init__(self, *args, **kwargs):
        super(_AbsStorageGui, self).__init__(*args, **kwargs)

    def _connect_value_change(self):
        self._input_wgt.input_value_accepted.connect(
            self._accept_value
        )


class FileGui(_AbsStorageGui):
    def __init__(self, *args, **kwargs):
        super(FileGui, self).__init__(*args, **kwargs)

        self._input_wgt._set_storage_scheme_(
            self._input_wgt.StorageScheme.FileOpen
        )
        
    def _set_open_mode(self):
        self._input_wgt._set_storage_scheme_(
            self._input_wgt.StorageScheme.FileOpen
        )
    
    def _set_save_mode(self):
        self._input_wgt._set_storage_scheme_(
            self._input_wgt.StorageScheme.FileSave
        )

    def _set_ext_includes(self, ext_includes):
        if ext_includes:
            self._input_wgt._set_ext_includes_(ext_includes)


class DirectoryGui(_AbsStorageGui):
    def __init__(self, *args, **kwargs):
        super(DirectoryGui, self).__init__(*args, **kwargs)

    def _set_open_mode(self):
        self._input_wgt._set_storage_scheme_(
            self._input_wgt.StorageScheme.DirectoryOpen
        )

    def _set_save_mode(self):
        self._input_wgt._set_storage_scheme_(
            self._input_wgt.StorageScheme.DirectorySave
        )


class _AbsGroupGui(QtWidgets.QWidget):
    GROUP_HEAD_H = 28
    GROUP_INDENT_W = 4

    @classmethod
    def _update_children_label_width(cls, layout):
        c = layout.count()
        if c:
            widths = []
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_wgt = i_item.widget()
                    if isinstance(i_wgt, _AbsTypedParamGui):
                        i_w = i_wgt._get_label_width()
                        widths.append(i_w)

            if widths:
                w = max(widths)
                for i in range(c):
                    i_item = layout.itemAt(i)
                    if i_item:
                        i_wgt = i_item.widget()
                        if isinstance(i_wgt, _AbsTypedParamGui):
                            i_wgt._set_label_width(w)

    def __init__(self, *args, **kwargs):
        super(_AbsGroupGui, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )

        self.setMinimumHeight(self.GROUP_HEAD_H)

        self._group_wgt = None

        self._gui_data = _scn_cor_base._Dict(
            indent=8,
            force_refresh_flag=True,
            rect=QtCore.QRect(),
            expand_flag=True,

            main=_scn_cor_base._Dict(
                rect=QtCore.QRect(),
                border_color=QtGui.QColor(79, 79, 79, 255),
                background_color=QtGui.QColor(71, 71, 71, 255),
            ),
            head=_scn_cor_base._Dict(
                size=(-1, self.GROUP_HEAD_H),
                rect=QtCore.QRect(),
                icon=_scn_cor_base._Dict(
                    rect=QtCore.QRect(),
                    frame_size=(20, 20),
                    size=(12, 12),
                    file=gui_core.GuiIcon.get('expand-open'),
                    file_0=gui_core.GuiIcon.get('expand-open'),
                    file_1=gui_core.GuiIcon.get('expand-close'),
                ),
                text=_scn_cor_base._Dict(
                    rect=QtCore.QRect(),
                    color_0=QtGui.QColor(223, 223, 223, 255),
                    color_1=QtGui.QColor(127, 127, 127, 255),
                    font=gui_qt_core.QtFont.generate(10)
                )
            ),
            body=_scn_cor_base._Dict(
                rect=QtCore.QRect(),
                border_color=QtGui.QColor(63, 63, 63, 255),
                background_color=QtGui.QColor(63, 63, 63, 255),
            ),
        )

        self._lot = QtWidgets.QVBoxLayout(self)
        self._lot.setAlignment(QtCore.Qt.AlignTop)
        self._lot.setContentsMargins(
            self.GROUP_INDENT_W+6, self.GROUP_HEAD_H+2, 0, 0
        )

        self._wgt = QtWidgets.QWidget()
        self._lot.addWidget(self._wgt)
        self._wgt.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )

        self._wgt_lot = QtWidgets.QVBoxLayout(self._wgt)
        self._wgt_lot.setAlignment(QtCore.Qt.AlignTop)
        self._wgt_lot.setContentsMargins(*[0]*4)
        self._wgt_lot.setSpacing(2)

        self._update_expand()

        self.installEventFilter(self)
        self._wgt.installEventFilter(self)

    def _update(self, rect):
        if rect != self._gui_data.rect or self._gui_data.force_refresh_flag is True:
            x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2
            idt = self._gui_data.indent
            hed_w, hed_h = self._gui_data.head.size

            self._gui_data.rect.setRect(
                x, y, w, h
            )

            min_h = h-hed_h

            if self._gui_data.expand_flag is True:
                self._gui_data.main.rect.setRect(
                    x, y, w, hed_h+min_h
                )
            else:
                self._gui_data.main.rect.setRect(
                    x, y, w, hed_h
                )

            self._gui_data.head.rect.setRect(
                x, y, w, hed_h
            )
            icn_w, icn_h = self._gui_data.head.icon.size
            self._gui_data.head.icon.rect.setRect(
                int(x+(hed_h-icn_w)/2), int(y+(hed_h-icn_h)/2), icn_w, icn_h
            )

            self._gui_data.head.text.rect.setRect(
                x+hed_h, y, w-hed_h, hed_h
            )
            self._gui_data.body.rect.setRect(
                x+idt, y+hed_h, w-idt, min_h
            )
            return True
        return False

    def _draw(self, painter):
        if self._param is not None:
            gui_qt_core.QtDrawBase._draw_frame(
                painter,
                rect=self._gui_data.main.rect,
                border_color=self._gui_data.main.border_color,
                background_color=self._gui_data.main.background_color,
                border_width=1,
                border_radius=2
            )

            gui_qt_core.QtDrawBase._draw_icon_by_file(
                painter,
                rect=self._gui_data.head.icon.rect,
                file_path=self._gui_data.head.icon.file
            )

            gui_qt_core.QtDrawBase._draw_name_text(
                painter,
                rect=self._gui_data.head.text.rect,
                text=self._param.get_label(),
                text_color=self._gui_data.head.text.color_0,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                text_font=self._gui_data.head.text.font
            )

            if self._gui_data.expand_flag is True:
                gui_qt_core.QtDrawBase._draw_frame(
                    painter,
                    rect=self._gui_data.body.rect,
                    border_color=self._gui_data.body.border_color,
                    background_color=self._gui_data.body.background_color,
                    border_width=1,
                    border_radius=0
                )

    def _swap_expand(self):
        self._set_expanded(not self._get_expanded())

    def _update_expand(self):
        boolean = self._gui_data.expand_flag
        self._gui_data.head.icon.file = [self._gui_data.head.icon.file_1, self._gui_data.head.icon.file_0][boolean]

        if boolean is True:
            self._wgt.show()
        else:
            self._wgt.hide()

        self._update_self()
        self._update_previous()

    def _set_expanded(self, boolean):
        self._gui_data.expand_flag = boolean

        self._update_expand()

    def _get_expanded(self):
        return self._gui_data.expand_flag

    def _add_wgt(self, wgt):
        self._wgt_lot.addWidget(wgt)

        self._update(self.rect())
        self.update()
        
        self._update_children_label_width(self._wgt_lot)

    def _set_group_wgt(self, wgt):
        self._group_wgt = wgt
        
    def _get_group_wgt(self):
        return self._group_wgt

    def _update_previous(self):
        group_wgt = self._get_group_wgt()
        if group_wgt is not None:
            group_wgt._update_self()
            group_wgt._update_previous()

    def _update_self(self):
        self._update(self.rect())
        self.update()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._update_self()
                self._update_previous()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    p = event.pos()
                    if self._gui_data.head.rect.contains(p):
                        self._swap_expand()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
        elif widget == self._wgt:
            if event.type() == QtCore.QEvent.ChildAdded:
                self._update_self()
                self._update_previous()
        return False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._draw(painter)


class GroupGui(_AbsGroupGui):
    GROUP_HEAD_H = 24
    GROUP_INDENT_W = 4

    def __init__(self, *args, **kwargs):
        super(GroupGui, self).__init__(*args, **kwargs)
        self._param = None

    def _set_param(self, param):
        self._param = param


class ParamRootGuiFactory:
    @staticmethod
    def add_one(scheme='typed'):
        def decorator(fnc):
            def wrapper(self, param, *args, **kwargs):
                param_path = param.get_param_path()
                if param_path in self._dict:
                    return self._dict[param]

                group_wgt = self._get_parent_wgt(param_path)

                gui = fnc(self, param, *args, **kwargs)

                # set param first
                gui._set_param(param)
                group_wgt._add_wgt(gui)
                if scheme == 'group':
                    gui._set_group_wgt(group_wgt)
                elif scheme == 'typed':
                    options = param.get_options()
                    if options.get('lock'):
                        gui._set_lock_mode()
                self._dict[param_path] = gui
                return gui
            return wrapper
        return decorator


# root
class ParamRootGui(_AbsGroupGui):
    GROUP_HEAD_H = 28
    GROUP_INDENT_W = 4

    def __init__(self, *args, **kwargs):
        super(ParamRootGui, self).__init__(*args, **kwargs)

        self._node = None
        self._dict = {}

    def _set_node(self, node):
        self._node = node
        self._build_parameters()

    def _get_node(self):
        return self._node

    def _draw(self, painter):
        if self._node is not None:
            gui_qt_core.QtDrawBase._draw_frame(
                painter,
                rect=self._gui_data.main.rect,
                border_color=self._gui_data.main.border_color,
                background_color=self._gui_data.main.background_color,
                border_width=1,
                border_radius=2
            )

            gui_qt_core.QtDrawBase._draw_icon_by_file(
                painter,
                rect=self._gui_data.head.icon.rect,
                file_path=self._gui_data.head.icon.file
            )

            type_text = bsc_core.ensure_string(self._node.get_type_label())
            path_text = bsc_core.ensure_string(self._node.get_path())

            txt_rect = self._gui_data.head.text.rect
            # type
            txt_x, txt_y, txt_w, txt_h = txt_rect.x(), txt_rect.y(), txt_rect.width(), txt_rect.height()

            txt_w_1 = QtGui.QFontMetrics(self._gui_data.head.text.font).width(type_text)+8
            txt_rect_1 = QtCore.QRect(txt_x, txt_y, txt_w_1, txt_h)

            gui_qt_core.QtDrawBase._draw_name_text(
                painter,
                rect=txt_rect_1,
                text=type_text,
                text_color=self._gui_data.head.text.color_1,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                text_font=self._gui_data.head.text.font
            )

            # path
            txt_w_0 = QtGui.QFontMetrics(self._gui_data.head.text.font).width(path_text)+8
            txt_rect_0 = QtCore.QRect(txt_x++txt_w_1, txt_y, txt_w_0, txt_h)

            gui_qt_core.QtDrawBase._draw_name_text(
                painter,
                rect=txt_rect_0,
                text=path_text,
                text_color=self._gui_data.head.text.color_0,
                text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                text_font=self._gui_data.head.text.font
            )

            if self._gui_data.expand_flag is True:
                gui_qt_core.QtDrawBase._draw_frame(
                    painter,
                    rect=self._gui_data.body.rect,
                    border_color=self._gui_data.body.border_color,
                    background_color=self._gui_data.body.background_color,
                    border_width=1,
                    border_radius=0
                )

    def _get_parent_wgt(self, param_path):
        prot_path_opt = bsc_core.BscPortPathOpt(param_path)
        parent_path = prot_path_opt.get_parent_path()
        if parent_path is not None:
            if parent_path not in self._dict:
                raise RuntimeError()
            return self._dict[parent_path]
        return self

    @ParamRootGuiFactory.add_one('group')
    def _add_group(self, param):
        gui = GroupGui()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_json(self, param):
        gui = JsonGui()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_constant(self, param):
        gui = ConstantGui()
        if param.get_type() == 'string':
            gui._set_value_type(str)
        elif param.get_type() == 'integer':
            gui._set_value_type(int)
        elif param.get_type() == 'float':
            gui._set_value_type(float)
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_path(self, param):
        gui = PathGui()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_boolean(self, param):
        gui = BooleanGui()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_button(self, param):
        gui = ButtonGui()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_buttons(self, param):
        gui = ButtonsGui()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_file(self, param):
        options = param.get_options()
        gui = FileGui()
        if options.get('open') is True:
            gui._set_open_mode()
        elif options.get('save') is True:
            gui._set_save_mode()
        else:
            raise RuntimeError()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_directory(self, param):
        options = param.get_options()
        gui = DirectoryGui()
        if options.get('open') is True:
            gui._set_open_mode()
        elif options.get('save') is True:
            gui._set_save_mode()
        else:
            raise RuntimeError()
        return gui

    @ParamRootGuiFactory.add_one()
    def _add_tuple(self, param):

        options = param.get_options()
        gui = TupleGui()
        if options['widget'] == 'integer2':
            gui._set_value_type(int)
            gui._set_value_size(2)
        elif options['widget'] == 'integer3':
            gui._set_value_type(int)
            gui._set_value_size(3)
        elif options['widget'] == 'float2':
            gui._set_value_type(float)
            gui._set_value_size(2)
        elif options['widget'] == 'float3':
            gui._set_value_type(float)
            gui._set_value_size(3)

        return gui

    @ParamRootGuiFactory.add_one()
    def _add_array(self, param):
        options = param.get_options()
        gui = ArrayGui()
        return gui

    def _build_parameters(self):
        param_handle = self._node.parameters
        params = param_handle.get_parameters()
        for i in params:
            i_options = i.get_options()
            i_widget = i_options.widget
            if i_widget == 'group':
                self._add_group(i)
            # constant
            elif i_widget in {'string', 'integer', 'float'}:
                self._add_constant(i)
            elif i_widget in {'path'}:
                self._add_path(i)
            elif i_widget == 'checkbox':
                self._add_boolean(i)
            elif i_widget == 'button':
                self._add_button(i)
            elif i_widget == 'buttons':
                self._add_buttons(i)
            elif i_widget == 'file':
                self._add_file(i)
            elif i_widget == 'directory':
                self._add_directory(i)
            elif i_widget in {'json'}:
                self._add_json(i)
            # tuple
            elif i_widget in {'integer2', 'integer3', 'float2', 'float3'}:
                self._add_tuple(i)
            else:
                self._add_json(i)
    
    def _get_parameter(self, param_path):
        return self._dict.get(param_path)
    
    def _set(self, key, value):
        self._get_parameter(key)._set_value(value)


# root stack
class ParamRootStackGui(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ParamRootStackGui, self).__init__(*args, **kwargs)

        self._dict = {}

        lot = QtWidgets.QVBoxLayout(self)
        lot.setAlignment(QtCore.Qt.AlignTop)
        lot.setContentsMargins(*[0]*4)
        lot.setSpacing(0)

        sca = gui_qt_widgets.QtVScrollArea()
        lot.addWidget(sca)

        self._stack = QtWidgets.QStackedWidget()
        sca._add_widget_(self._stack)

    def _load_node(self, node):
        node_path = node.get_path()
        if node_path in self._dict:
            param_root_gui = self._dict[node_path]
            self._stack.setCurrentWidget(param_root_gui)
        else:
            param_root_gui = ParamRootGui()
            self._stack.addWidget(param_root_gui)
            param_root_gui._set_node(node)
            self._dict[node_path] = param_root_gui
            sys.stdout.write('Load parameters: {}\n'.format(node_path))
            self._stack.setCurrentWidget(param_root_gui)

    def _unregister_node(self, node):
        path = node.get_path()
        if path in self._dict:
            param_root_gui = self._dict[path]
            self._stack.removeWidget(param_root_gui)
            param_root_gui.close()
            param_root_gui.deleteLater()
            self._dict.pop(path)

    def _get_current(self):
        return self._stack.currentWidget()

    def _get_one(self, node_path):
        return self._dict.get(node_path)
