# coding:utf-8
import collections

import copy

import json

import enum

import six

import lxbasic.core as bsc_core
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from . import base as _base


class _QtUndoCommand(QtWidgets.QUndoCommand):
    class Flags(enum.IntEnum):
        Connect = 0
        Disconnect = 1
        Reconnect = 4

        Delete = 5

    def __init__(self, scene_model, data):
        super(_QtUndoCommand, self).__init__()
        self._scene_model = scene_model
        self._data = data

    def undo(self):
        for i_flag, i_args in self._data:
            if i_flag == self.Flags.Connect:
                self._scene_model._disconnect_path(i_args)
            elif i_flag == self.Flags.Disconnect:
                self._scene_model._connect_path(i_args)
            elif i_flag == self.Flags.Reconnect:
                i_path_0, i_path_1 = i_args
                self._scene_model._reconnect_path(i_path_1, i_path_0)
            elif i_flag == self.Flags.Delete:
                i_node_args, i_connection_args = i_args
                for j_args in i_node_args:
                    self._scene_model._create_node_by_json_str(j_args)
                for j_args in i_connection_args:
                    self._scene_model._connect_path(j_args)

    def redo(self):
        for i_flag, i_args in self._data:
            if i_flag == self.Flags.Connect:
                self._scene_model._connect_path(i_args)
            elif i_flag == self.Flags.Disconnect:
                self._scene_model._disconnect_path(i_args)
            elif i_flag == self.Flags.Reconnect:
                i_path_0, i_path_1 = i_args
                self._scene_model._reconnect_path(i_path_0, i_path_1)
            elif i_flag == self.Flags.Delete:
                i_node_args, i_connection_args = i_args
                for j_args in i_connection_args:
                    self._scene_model._disconnect_path(j_args)
                for j_args in i_node_args:
                    self._scene_model._remove_node_by_json_str(j_args)


# connection model
class _ConnectionModel(_base._SbjBase):
    SEP = '->'

    def __init__(self, item):
        super(_ConnectionModel, self).__init__(item)

    @classmethod
    def _to_path(cls, source_path, target_path):
        return cls.SEP.join([source_path, target_path])

    @classmethod
    def _to_args(cls, path):
        return path.split(cls.SEP)

    @classmethod
    def _get_source(cls, scene_model, path):
        source_path, _ = path.split(cls.SEP)
        node_path, port_path = bsc_core.BscAttributePath.split_by(source_path)
        return scene_model.get_node(node_path).get_output_port(port_path)

    @classmethod
    def _get_target(cls, scene_model, path):
        _, target_path = path.split(cls.SEP)
        node_path, port_path = bsc_core.BscAttributePath.split_by(target_path)
        return scene_model.get_node(node_path).get_input_port(port_path)

    def get_source(self):
        return self._get_source(self.scene_model, self.get_path())

    def get_target(self):
        return self._get_target(self.scene_model, self.get_path())

    def do_delete(self):
        self.scene_model.remove_connection_path(self.get_path())

    # update
    def update_v(self, *args, **kwargs):
        self._item._update_v(*args, **kwargs)

    def update_h(self, *args, **kwargs):
        self._item._update_h(*args, **kwargs)

    def reset_status(self):
        self._item._set_color(
            QtGui.QColor(255, 255, 0, 255)
        )

    def to_correct_status(self):
        self._item._set_color(
            QtGui.QColor(0, 255, 0, 255)
        )


# port model
class _PortModel(_base._SbjBase):

    def __init__(self, *args, **kwargs):
        super(_PortModel, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.get_path() == other.get_path()
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.get_path() != other.get_path()
        return True


class _InputPortModel(_PortModel):
    def __init__(self, *args, **kwargs):
        super(_InputPortModel, self).__init__(*args, **kwargs)
        self._data.connection = None

    def __str__(self):
        return 'InputPort(path={})'.format(
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def _register_connection(self, path):
        self._data.connection = path

    def _unregister_connection(self, path):
        self._data.connection = None

    def has_source(self):
        return bool(self._data.connection)

    def get_source(self):
        if self._data.connection:
            return _ConnectionModel._get_source(self.scene_model, self._data.connection)

    def get_connection_path_set(self):
        if self._data.connection:
            return {self._data.connection}
        return set()

    def get_connections_itr(self):
        if self._data.connection:
            connection = self.scene_model.get_connection(self._data.connection)
            if connection:
                yield connection

    def get_connections(self):
        return list(self.get_connections_itr())

    def connect(self, source_port):
        if not isinstance(source_port, _OutputPortModel):
            raise RuntimeError()

        self.scene_model._connect_ports(source_port, self)


class _OutputPortModel(_PortModel):
    def __init__(self, *args, **kwargs):
        super(_OutputPortModel, self).__init__(*args, **kwargs)
        self._data.connections = set()

    def __str__(self):
        return 'OutputPort(path={})'.format(
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def _register_connection(self, path):
        if path not in self._data.connections:
            self._data.connections.add(path)

    def _unregister_connection(self, path):
        if path in self._data.connections:
            self._data.connections.remove(path)

    def has_targets(self):
        return bool(self._data.connections)

    def get_target_itr(self):
        for i in self._data.connections:
            yield _ConnectionModel._get_target(self.scene_model, i)

    def get_targets(self):
        return list(self.get_target_itr())

    def get_connection_path_set(self):
        return set(self._data.connections)

    def get_connections_itr(self):
        for i in set(self._data.connections):
            i_connection = self.scene_model.get_connection(i)
            if i_connection:
                yield i_connection

    def get_connections(self):
        return list(self.get_connections_itr())

    def connect(self, target_port):
        if not isinstance(target_port, _InputPortModel):
            raise RuntimeError()

        self.scene_model._connect_ports(self, target_port)


class _AbsAction(object):
    ActionFlags = _base._ActionFlags

    @property
    def gui_data(self):
        raise NotImplementedError()

    def _init_action(self):
        self.gui_data.action = _base._Dict(
            flag=None,
            sub_flag=None,
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


class _AbsRectSbj(_base._SbjBase):
    # hover
    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._gui_data.select.flag:
            self._gui_data.select.flag = flag

    def __init__(self, *args, **kwargs):
        super(_AbsRectSbj, self).__init__(*args, **kwargs)

        self._data.options = _base._Dict(
            position=_base._Dict(
                x=0.0, y=0.0
            ),
            color_enable=False,
            color=_base._Dict(
                r=95, g=95, b=95
            )
        )

        # refresh
        self._gui_data.force_refresh_flag = True
        #
        self._gui_data.cut_flag = False
        # main
        self._gui_data.rect = qt_rect()

        # basic
        self._gui_data.basic = _base._Dict(
            rect=qt_rect(),
            size=QtCore.QSize(),
        )
        # color
        self._gui_data.color = _base._Dict(
            rect=qt_rect(),
            border=_base._QtColors.NodeBorder,
            background=_base._QtColors.NodeBackground,
            alpha=255,
        )

        self._gui_data.head=_base._Dict(
            rect=QtCore.QRectF(),
            size=QtCore.QSize(),
        )

        # text option for draw
        self._gui_data.text = _base._Dict(
            font=gui_qt_core.QtFont.generate(size=10),
            color=_base._QtColors.Text,
            action_color=_base._QtColors.TextHover,
            # all text height
            height=24
        )

        # type
        self._gui_data.type = _base._Dict(
            rect=qt_rect(),
            font=gui_qt_core.QtFont.generate(size=12, weight=75),
            color=_base._QtColors.TypeText,
        )

        self._gui_data.name = _base._Dict(
            rect=qt_rect(),
            font=gui_qt_core.QtFont.generate(size=12, weight=75),
            color=_base._QtColors.TypeText,
        )

        # hover
        self._gui_data.hover = _base._Dict(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*gui_core.GuiRgba.LightOrange),
        )

        # select
        self._gui_data.select = _base._Dict(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*gui_core.GuiRgba.LightAzureBlue),
        )

    def set_position(self, position):
        self._item.setPos(*position)

    # color
    def set_color_enable(self, boolean):
        self._data.options.color_enable = boolean

    def set_color(self, args):
        self.set_color_enable(True)
        self._data.options.color.r = args[0]
        self._data.options.color.g = args[1]
        self._data.options.color.b = args[2]

        self._gui_data.color.background = QtGui.QColor(
            self._data.options.color.r,
            self._data.options.color.g,
            self._data.options.color.b,
            self._gui_data.color.alpha
        )

    def set_basic_size(self, size):
        self._gui_data.basic.size = size
        x, y = self._item.x(), self._item.y()
        w, h = size.width(), size.height()
        self._set_rect(x, y, w, h)

    def _set_rect(self, x, y, w, h):
        self._item.setRect(x, y, w, h)
        self._update_attaches()

    def _update_attaches(self):
        pass

    def set_basic_head_size(self, size):
        self._gui_data.head.size = size

    def set_cut_flag(self, flag):
        self._data.cut_flag = flag
        if flag is True:
            self._item.hide()
        else:
            self._item.show()

    def move_by(self, x, y):
        self._item.moveBy(x, y)


# node model
class _NodeModel(_AbsRectSbj):
    def __init__(self, *args, **kwargs):
        super(_NodeModel, self).__init__(*args, **kwargs)
        # basic
        self._gui_data.color.border=_base._QtColors.NodeBorder
        self._gui_data.color.background = _base._QtColors.NodeBackground
        # port
        self._gui_data.port = _base._Dict(
            input=_base._Dict(
                cls=None
            ),
            output=_base._Dict(
                cls=None
            ),
            size=QtCore.QSize(16, 8),
            spacing=4
        )
        # icon
        self._gui_data.icon_enable = False
        self._gui_data.icon = _base._Dict(
            file_flag=False,
            file=None,

            pixmap_flag=False,
            pixmap=None,

            rect=qt_rect(),
        )
        # menu
        self._gui_data.menu = _base._Dict(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )
        # input port
        self._data.input_ports = collections.OrderedDict()
        # output port
        self._data.output_ports = collections.OrderedDict()

    def set_options(self, options):
        position = options['position']
        self.set_position((position['x'], position['y']))

        color_enable = options['color_enable']
        if color_enable is True:
            color = options['color']
            self.set_color((color['r'], color['g'], color['b']))

    def create_input_port(self, type_name, port_path):
        if port_path in self._data.input_ports:
            return False, self._data.input_ports[port_path]

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()

        port = self._gui_data.port.input.cls(self._item, prt_w, prt_h)
        atr_path = bsc_core.BscAttributePath.join_by(self.get_path(), port_path)

        model = port._model
        self._data.input_ports[port_path] = model
        self._update_input_ports()
        port._update_input()

        model.set_type(type_name)
        model.set_path(atr_path)
        model.set_name(port_path)

        return True, model

    def _create_input_port_by_data(self, data):
        type_name = data['type']
        name = data['name']
        flag, node = self.create_input_port(type_name, name)
        return node

    def get_input_ports(self):
        return list(self._data.input_ports.values())

    def get_input_port(self, name):
        return self._data.input_ports.get(name)

    def _update_input_ports(self):
        rect = self._item.boundingRect()
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        spc = self._gui_data.port.spacing

        ports = self.get_input_ports()
        prt_c = len(ports)
        if not prt_c:
            return

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()
        prt_ws = prt_c*prt_w+spc*(prt_c-1)
        prt_x, prt_y = x+(w-prt_ws)/2, y-prt_h-1

        x_c = prt_x
        for i in ports:
            i._item.setPos(x_c, prt_y)
            x_c += prt_w+spc

    def create_output_port(self, type_name, name):
        if name in self._data.output_ports:
            return False, self._data.output_ports[name]

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()

        port = self._gui_data.port.output.cls(self._item, prt_w, prt_h)
        atr_path = bsc_core.BscAttributePath.join_by(self.get_path(), name)

        model = port._model
        self._data.output_ports[name] = model
        self._update_output_ports()
        port._update_output()

        model.set_type(type_name)
        model.set_path(atr_path)
        model.set_name(name)

        return True, model

    def _create_output_port_by_data(self, data):
        type_name = data['type']
        name = data['name']
        flag, node = self.create_output_port(type_name, name)
        return node

    def get_output_ports(self):
        return list(self._data.output_ports.values())

    def get_output_port(self, name):
        return self._data.output_ports.get(name)

    # connection
    def get_source_connection_path_set(self):
        set_ = set()
        for i in self.get_input_ports():
            set_.update(i.get_connection_path_set())
        return set_
    
    def get_source_connections_itr(self):
        for i in self.get_input_ports():
            for j in i.get_connections_itr():
                yield j
                
    def get_target_connection_path_set(self):
        set_ = set()
        for i in self.get_output_ports():
            set_.update(i.get_connection_path_set())
        return set_

    def get_target_connections_itr(self):
        for i in self.get_output_ports():
            for j in i.get_connections_itr():
                yield j
    
    def get_connection_path_set(self):
        set_ = set()
        set_.update(self.get_source_connection_path_set())
        set_.update(self.get_target_connection_path_set())
        return set_

    def _update_output_ports(self):
        rect = self._item.boundingRect()
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        spc = self._gui_data.port.spacing

        ports = self.get_output_ports()
        prt_c = len(ports)
        if not prt_c:
            return

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()
        prt_ws = prt_c*prt_w+spc*(prt_c-1)
        prt_x, prt_y = x+(w-prt_ws)/2, y+h+2

        x_c = prt_x
        for i in ports:
            i._item.setPos(x_c, prt_y)
            x_c += prt_w+spc

    def update(self, rect):
        # check rect is change
        if rect != self._gui_data.rect or self._gui_data.force_refresh_flag is True:
            self._gui_data.rect = qt_rect(rect)

            x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2

            mrg = 2

            spc = 2
            self._gui_data.basic.rect.setRect(
                x, y, w, h
            )

            hed_size = self._gui_data.head.size
            hed_w, hed_h = hed_size.width(), hed_size.height()

            icn_w = 16
            icn_y = y+((hed_h-icn_w)/2)
            # icon
            icon_frm_w = 0
            if self._gui_data.icon_enable is True:
                icon_frm_w = 20
                self._gui_data.icon.rect.setRect(
                    x+(icon_frm_w-icn_w)/2, icn_y, icn_w, icn_w
                )

            offset = icon_frm_w+spc

            offset = max(4, offset)

            self._gui_data.type.rect.setRect(
                x, y, w, hed_h
            )
            return True
        return False

    def draw(self, painter, option):
        painter.save()

        self.update(option.rect)

        self._update_select(bool(option.state & QtWidgets.QStyle.State_Selected))

        self.draw_base(painter, option)

        painter.restore()

    def draw_base(self, painter, option):
        if self._gui_data.select.flag is True:
            border_color = self._gui_data.select.color
            border_width = 2
        elif self._gui_data.hover.flag is True:
            border_color = self._gui_data.hover.color
            border_width = 2
        else:
            border_color = self._gui_data.color.border
            border_width = 1

        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.basic.rect,
            border_color=border_color,
            background_color=self._gui_data.color.background,
            border_width=border_width,
            border_radius=2
        )
        # draw icon
        if self._gui_data.icon_enable is True:
            if self._gui_data.icon.file_flag is True:
                gui_qt_core.QtItemDrawBase._draw_icon_by_file(painter, self._gui_data.icon.rect, self._gui_data.icon.file)
            elif self._gui_data.icon.pixmap_flag is True:
                gui_qt_core.QtItemDrawBase._draw_icon_by_pixmap(painter, self._gui_data.icon.rect, self._gui_data.icon.pixmap)
        # draw type
        gui_qt_core.QtItemDrawBase._draw_name_text(
            painter, self._gui_data.type.rect, self._data.type,
            self._gui_data.type.color, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            font=self._gui_data.type.font
        )

    # name
    def set_name(self, text):
        if text is not None:
            self._data.name = text
            self._item._name_entry.setPlainText(text)
            return True
        return False

    # icon
    def set_icon_name(self, icon_name):
        # do not check file exists
        file_path = gui_core.GuiIcon.get(icon_name)
        if file_path:
            self._gui_data.icon_enable = True
            self._gui_data.icon.file_flag = True
            self._gui_data.icon.file = file_path

    # menu
    def set_menu_content(self, content):
        self._gui_data.menu.content = content

    def get_menu_content(self):
        return self._gui_data.menu.content

    def set_menu_data(self, data):
        self._gui_data.menu.data = data

    def get_menu_data(self):
        return self._gui_data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._gui_data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._gui_data.menu.data_generate_fnc

    def set_menu_name_dict(self, dict_):
        if isinstance(dict_, dict):
            self._gui_data.menu.name_dict = dict_

    def get_menu_name_dict(self):
        return self._gui_data.menu.name_dict

    # hover
    def _update_hover(self, flag):
        if flag != self._gui_data.hover.flag:
            self._gui_data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._gui_data.select.flag:
            self._gui_data.select.flag = flag

    def _set_rect(self, x, y, w, h):
        self._item.setRect(x, y, w, h)
        self._update_attaches()

    def _update_attaches(self):
        self._update_name()
        self._update_input_ports()
        self._update_output_ports()

    def _update_name(self):
        rect = self._item.boundingRect()
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        self._item._name_entry.setPos(x+w, y)

    def to_json(self):
        return self._data.to_json()

    def do_delete(self):
        for i in self.get_source_connections_itr():
            i.do_delete()

        for i in self.get_target_connections_itr():
            i.do_delete()

        self.scene_model._unregister_node(self)


class _BackdropModel(
    _AbsRectSbj,
    _AbsAction,
):
    def __init__(self, *args, **kwargs):
        super(_BackdropModel, self).__init__(*args, **kwargs)
        # basic
        self._gui_data.color.border = _base._QtColors.BackdropBorder
        self._gui_data.color.background = _base._QtColors.BackdropBackground
        self._gui_data.color.alpha = 31

        self._gui_data.name.color = _base._QtColors.BackdropName

        self._init_action()

        self._data.move = _base._Dict(
            start_point=QtCore.QPointF(),
        )

        self._gui_data.resize = _base._Dict(
            start_point=QtCore.QPointF(),
            start_rect=QtCore.QRect(),
            rect=QtCore.QRectF(),
            icon=_base._Dict(
                file=gui_core.GuiIcon.get('resize'),
            )
        )

        self._data.nodes_set = set()

    def update(self, rect):
        # check rect is change
        if rect != self._gui_data.rect or self._gui_data.force_refresh_flag is True:
            self._gui_data.rect = qt_rect(rect)

            x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2

            spc = 2
            self._gui_data.basic.rect.setRect(
                x, y, w, h
            )

            hed_size = self._gui_data.head.size
            hed_w, hed_h = hed_size.width(), hed_size.height()

            self._gui_data.head.rect.setRect(
                x, y, w, hed_h
            )

            mrg = 4

            icn_w, icn_h = 20, 20

            self._gui_data.resize.rect.setRect(
                x+w-icn_w-mrg, y+h-icn_h-mrg, icn_w, icn_h
            )

            self._gui_data.name.rect.setRect(
                x, y, w, hed_h
            )

            return True
        return False

    def draw(self, painter, option):
        painter.save()

        self.update(option.rect)

        self._update_select(bool(option.state & QtWidgets.QStyle.State_Selected))

        self.draw_base(painter, option)

        painter.restore()

    def draw_base(self, painter, option):
        if self._gui_data.select.flag is True:
            border_color = self._gui_data.select.color
            border_width = 2
        elif self._gui_data.hover.flag is True:
            border_color = self._gui_data.hover.color
            border_width = 2
        else:
            border_color = self._gui_data.color.border
            border_width = 1

        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.basic.rect,
            border_color=border_color,
            background_color=self._gui_data.color.background,
            border_width=border_width,
            border_radius=0
        )

        # name
        gui_qt_core.QtItemDrawBase._draw_name_text(
            painter, self._gui_data.name.rect, self._data.name,
            self._gui_data.name.color, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            font=self._gui_data.name.font
        )

        # headline
        gui_qt_core.QtItemDrawBase._draw_line(
            painter, point_0=self._gui_data.head.rect.bottomLeft(), point_1=self._gui_data.head.rect.bottomRight(),
            border_color=border_color,
        )

        # resize
        gui_qt_core.QtItemDrawBase._draw_icon_by_file(
            painter,
            rect=self._gui_data.resize.rect,
            file_path=self._gui_data.resize.icon.file
        )

    def _set_rect(self, x, y, w, h):
        self._item.setRect(x, y, w, h)

    def _check_move(self, point):
        p = self._item.mapToItem(self._item, point)
        if self._gui_data.head.rect.contains(p):
            return True
        return False

    def do_move_start(self, event):
        self._data.move.start_point = event.pos()
        x, y = self._item.x(), self._item.y()
        rect = self._item.boundingRect()
        w, h = rect.width(), rect.height()

        node_set = set()

        self.scene_model.clear_selection()

        self._item.setSelected(True)
        all_items = self.scene._get_items_by_rect(x, y, w, h)
        for i in all_items:
            if i.SBJ_TYPE == _base._QtSbjTypes.Node:
                node_set.add(i._model)
                i.setSelected(True)

        self._data.node_set = node_set

    def do_move(self, event):
        delta = event.pos()-self._data.move.start_point
        x, y = delta.x(), delta.y()

        self._item.moveBy(x, y)

        node_set = self._data.node_set

        if node_set:
            for i in node_set:
                i._item.moveBy(x, y)

    def _check_resize(self, point):
        p = self._item.mapToItem(self._item, point)
        if self._gui_data.resize.rect.contains(p):
            return True
        return False

    def do_resize_start(self, event):
        self._gui_data.resize.start_point = event.pos()
        self._gui_data.resize.start_rect = self._item.rect()

    def do_resize_move(self, event):
        delta = event.pos()-self._gui_data.resize.start_point
        rect = self._gui_data.resize.start_rect
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        
        self._set_rect(
            x, y, w+delta.x(), h+delta.y()
        )


# scene model
class _SceneModel(_AbsAction):
    ActionFlags = _base._ActionFlags

    @classmethod
    def _json_str_to_data(cls, json_str):
        return json.loads(json_str, object_pairs_hook=collections.OrderedDict)

    def __init__(self, widget):
        self._graph = widget

        self._data = _base._Dict()
        self._gui_data = _base._Dict()

        self._data.nodes = collections.OrderedDict()
        self._data.connections = collections.OrderedDict()

        self._gui_data.node = _base._Dict(
            cls=None,
            group_cls=None,
            size=QtCore.QSize(200, 24),
            head=_base._Dict(
                size=QtCore.QSize(200, 24),
            )
        )

        # backdrop
        self._gui_data.backdrop = _base._Dict(
            cls=None,
            size=QtCore.QSize(320, 240),
            head=_base._Dict(
                size=QtCore.QSize(320, 24),
            )
        )

        # connection
        self._gui_data.connection = _base._Dict(
            cls=None,
        )

        self._init_action()
        self._pan_start = QtCore.QPoint()

        self._data.zoom = _base._Dict(
            factor=1.2
        )
        self._data.track = _base._Dict(
            start_point=QtCore.QPointF()
        )

    def create_node(self, type_name, path, *args, **kwargs):
        if path in self._data.nodes:
            return False, self._data.nodes[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        item = self._gui_data.node.cls()
        self._graph.scene().addItem(item)

        model = item._model
        model.set_type(type_name)
        model.set_path(path)
        model.set_name(kwargs.get('name', path_opt.get_name()))
        model.set_basic_size(self._gui_data.node.size)
        model.set_basic_head_size(self._gui_data.node.head.size)

        self._data.nodes[path] = model
        return True, model

    def _paste_node_by_json_str(self, json_str):
        self._create_node_by_data(json.loads(json_str, object_pairs_hook=collections.OrderedDict))

    def _create_node_by_json_str(self, json_str):
        data = self._json_str_to_data(json_str)
        type_name = data['type']
        path = data['path']
        flag, node = self.create_node(type_name, path)
        node.set_options(data['options'])
        for k, v in data['input_ports'].items():
            node._create_input_port_by_data(v)
        for k, v in data['output_ports'].items():
            node._create_output_port_by_data(v)
        return node

    def _create_node_by_data(self, data):
        type_name = data['type']
        path = '/{}_copy'.format(data['name'])
        flag, node = self.create_node(type_name, path)
        node.set_options(data['options'])
        for k, v in data['input_ports'].items():
            node._create_input_port_by_data(v)
        for k, v in data['output_ports'].items():
            node._create_output_port_by_data(v)
        return node

    def _remove_node_by_json_str(self, json_str):
        data = self._json_str_to_data(json_str)
        node = self.get_node(data['path'])
        self._unregister_node(node)

    def _unregister_node(self, node):
        path = node.get_path()
        self._data.nodes.pop(path)
        item = node._item
        self._graph.scene().removeItem(item)
        del item

    def _push_delete_cmd(self, node_args, connection_args):
        data = [
            (_QtUndoCommand.Flags.Delete, (node_args, connection_args))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def get_node(self, path):
        return self._data.nodes.get(path)

    def create_backdrop(self, type_name, path, *args, **kwargs):
        if path in self._data.nodes:
            return False, self._data.nodes[path]

        path_opt = bsc_core.BscNodePathOpt(path)
        item = self._gui_data.backdrop.cls()
        self._graph.scene().addItem(item)

        model = item._model
        model.set_type(type_name)
        model.set_path(path)
        model.set_name(kwargs.get('name', path_opt.get_name()))
        model.set_basic_size(self._gui_data.backdrop.size)
        model.set_basic_head_size(self._gui_data.backdrop.head.size)

        self._data.nodes[path] = model
        return True, model

    # connection
    def create_connection(self, source_arg, target_args):
        if isinstance(source_arg, six.string_types) and isinstance(target_args, six.string_types):
            self._connect_port_paths(source_arg, target_args)
        else:
            self._connect_ports(source_arg, target_args)

    def _connect_path(self, path):
        self._connect_port_paths(*_ConnectionModel._to_args(path))

    def _connect_paths(self, paths):
        [self._connect_path(x) for x in paths]

    def _to_node_input_port(self, atr_path):
        node_path, port_path = bsc_core.BscAttributePath.split_by(atr_path)
        return self.get_node(node_path).get_input_port(port_path)

    def _to_node_output_port(self, atr_path):
        node_path, port_path = bsc_core.BscAttributePath.split_by(atr_path)
        return self.get_node(node_path).get_output_port(port_path)

    def _connect_port_paths(self, source_path, target_path):
        source_path_opt = bsc_core.BscAttributePathOpt(source_path)
        source_node_path = source_path_opt.obj_path
        source_node = self.get_node(source_node_path)
        if not source_node:
            return False, None
        source_port_path = source_path_opt.port_path
        source_port = source_node.get_output_port(source_port_path)
        if not source_port:
            return False, None
        target_path_opt = bsc_core.BscAttributePathOpt(target_path)
        target_node_path = target_path_opt.obj_path
        target_node = self.get_node(target_node_path)
        if not target_node:
            return False, None
        target_port_path = target_path_opt.port_path
        target_port = target_node.get_input_port(target_port_path)
        if not target_port:
            return False, None

        if source_node_path == target_node_path:
            return False, None

        return self._connect_ports(source_port, target_port)

    def _connect_ports(self, source_port, target_port):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        if path in self._data.connections:
            return False, self._data.connections[path]

        if target_port.has_source():
            # when target port has source, break connection first
            source_port_old = target_port.get_source()
            if self._disconnect_ports(source_port_old, target_port) is False:
                return False, None

        item = self._gui_data.connection.cls(source_port, target_port)
        item._set_hover_enable(True)
        model = item._model
        model.set_path(path)
        model.update_v()

        source_port._register_connection(path)
        target_port._register_connection(path)
        self._graph.scene().addItem(item)

        self._data.connections[path] = model
        return True, model

    def _push_connect_cmd(self, source_port, target_port):
        data = [
            (_QtUndoCommand.Flags.Connect, _ConnectionModel._to_path(source_port.get_path(), target_port.get_path()))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    # disconnect
    def _disconnect_path(self, path):
        self._disconnect_port_paths(*_ConnectionModel._to_args(path))

    def _disconnect_paths(self, paths):
        [self._disconnect_path(x) for x in paths]

    def _disconnect_port_paths(self, source_path, target_path):
        self._disconnect_ports(
            self._to_node_output_port(source_path), self._to_node_input_port(target_path)
        )

    def _disconnect_ports(self, source_port, target_port):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        if path in self._data.connections:
            connection = self._data.connections[path]
            self._data.connections.pop(path)
            source_port._unregister_connection(path)
            target_port._unregister_connection(path)
            self._graph.scene().removeItem(connection._item)
            return True
        return False

    def _push_disconnect_cmd(self, source_port, target_port):
        data = [
            (_QtUndoCommand.Flags.Disconnect, _ConnectionModel._to_path(source_port.get_path(), target_port.get_path()))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _reconnect_path(self, path_0, path_1):
        self._disconnect_path(path_0)
        self._connect_path(path_1)

    def _reconnect_source(self, source_port, target_port, source_port_new):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        self.remove_connection_path(path)
        self._connect_ports(source_port_new, target_port)

    def _push_reconnect_source_cmd(self, source_port, target_port, source_port_new):
        path_0 = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        path_1 = _ConnectionModel._to_path(source_port_new.get_path(), target_port.get_path())
        data = [
            (_QtUndoCommand.Flags.Reconnect, (path_0, path_1))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def _reconnect_target(self, source_port, target_port, target_port_new):
        path = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        self.remove_connection_path(path)
        self._connect_ports(source_port, target_port_new)

    def _push_reconnect_target_cmd(self, source_port, target_port, target_port_new):
        path_0 = _ConnectionModel._to_path(source_port.get_path(), target_port.get_path())
        path_1 = _ConnectionModel._to_path(source_port.get_path(), target_port_new.get_path())
        data = [
            (_QtUndoCommand.Flags.Reconnect, (path_0, path_1))
        ]
        self._graph._undo_stack.push(_QtUndoCommand(self, data))

    def get_connection(self, path):
        return self._data.connections.get(path)

    def remove_connection_path(self, path):
        if path in self._data.connections:
            connection = self._data.connections[path]
            self._remove_connection(connection)
            return True
        return False

    def _remove_connection(self, connection):
        path = connection.get_path()
        source_port = connection.get_source()
        target_port = connection.get_target()
        source_port._unregister_connection(path)
        target_port._unregister_connection(path)
        self._data.connections.pop(path)
        self._graph.scene().removeItem(connection._item)

    @property
    def data(self):
        return self._data

    @property
    def gui_data(self):
        return self._gui_data

    def do_zoom(self, event):
        zoom_in = event.angleDelta().y() > 0

        f = self._data.zoom.factor
        factor = f if zoom_in else 1/f

        mouse_scene_pos = self._graph.mapToScene(event.pos())

        self._graph.scale(factor, factor)

        new_mouse_scene_pos = self._graph.mapToScene(event.pos())
        delta = new_mouse_scene_pos-mouse_scene_pos

        self._graph.translate(delta.x(), delta.y())

    def on_track_start(self, event):
        self._data.track.start_point = event.pos()
        self._graph.setCursor(QtCore.Qt.ClosedHandCursor)

    def do_track_move(self, event):
        delta = event.pos()-self._data.track.start_point
        self._data.track.start_point = event.pos()
        scale_factor = self._graph.transform().m11()

        self._graph.translate(delta.x()/scale_factor, delta.y()/scale_factor)

    def do_tack_end(self):
        self._graph.unsetCursor()

    # actions
    def _on_delete_action(self):
        node_args = []
        connection_args = []
        items = self._graph.scene().selectedItems()
        for i in items:
            if i.SBJ_TYPE in {_base._QtSbjTypes.Node}:
                i_node = i._model
                i_connection_path_set = i_node.get_connection_path_set()
                connection_args.extend(list(i_connection_path_set))
                node_args.append(i._model.to_json())
            elif i.SBJ_TYPE in {_base._QtSbjTypes.Connection}:
                connection_args.append(i._model.get_path())

        if node_args or connection_args:
            self._push_delete_cmd(node_args, connection_args)

    def _on_copy_action(self):
        pass

    def _on_cut_action(self):
        nodes = []

        items = self._graph.scene().selectedItems()
        for i in items:
            if isinstance(i, self._gui_data.node.cls):
                nodes.append(i)

    def _on_paste_action(self):
        pass

    def clear_selection(self):
        self._graph.scene().clearSelection()
