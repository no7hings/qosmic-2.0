# coding:utf-8
import collections

import lxbasic.core as bsc_core
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from .. import base as _base

from .. import undo as _undo

from . import parameter as _param


class _AbsNodeModel(
    _base._SbjBase,
    _base._AbsAction
):
    ENTITY_TYPE = _base.EntityTypes.Node

    NODE_TYPE = None

    # hover
    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._gui_data.select.flag:
            self._gui_data.select.flag = flag

    def __init__(self, *args, **kwargs):
        super(_AbsNodeModel, self).__init__(*args, **kwargs)

        self._data.options = _base._Dict(
            position=_base._Dict(
                x=0.0, y=0.0
            ),
            size=_base._Dict(
                width=160, height=24
            ),
            color_enable=False,
            color=_base._Dict(
                r=95, g=95, b=95
            )
        )

        self._init_action()

        # refresh
        self._gui_data.force_refresh_flag = True
        #
        self._gui_data.cut_flag = False
        # main
        self._gui_data.rect = qt_rect()

        # basic
        self._gui_data.basic = _base._Dict(
            rect=QtCore.QRectF(),
            size=QtCore.QSize(),
        )

        # color
        self._gui_data.color = _base._Dict(
            rect=QtCore.QRectF(),
            border=_base._QtColors.NodeBorder,
            background=_base._QtColors.NodeBackground,
            alpha=255,
        )

        # head
        self._gui_data.head = _base._Dict(
            rect=QtCore.QRectF(),
            size=QtCore.QSize(),
        )

        # edit
        self._gui_data.edited = _base._Dict(
            rect=QtCore.QRectF(),
            value=False,
        )

        # viewed
        self._gui_data.viewed = _base._Dict(
            rect=QtCore.QRectF(),
            value=False,
        )

        # type
        self._gui_data.type = _base._Dict(
            rect=qt_rect(),
            font=gui_qt_core.QtFont.generate(size=12, weight=75),
            color=_base._QtColors.TypeText,
            gui_name=None,
            gui_name_chs=None
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

        # menu
        self._gui_data.menu = _base._Dict(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

    def __str__(self):
        return 'Node(path={})'.format(
            self.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def set_options(self, options):
        position = options['position']
        self.set_position((position['x'], position['y']))

        size = options['size']
        self.set_size((size['width'], size['height']))

        color_enable = options['color_enable']
        if color_enable is True:
            color = options['color']
            self.set_color((color['r'], color['g'], color['b']))

    def set_position(self, position):
        x, y = position
        self._data.options.position.x = x
        self._data.options.position.y = y
        self._gui.setPos(*position)

    def get_position(self):
        return self._gui.x(), self._gui.y()

    def _update_position_option(self):
        self._data.options.position.x = self._gui.x()
        self._data.options.position.y = self._gui.y()

    def set_size(self, size):
        w, h = size
        self._data.options.size.width = w
        self._data.options.size.height = h
        self._gui.setRect(0, 0, w, h)

        self._update_attaches()

    def _auto_resize(self):
        pass

    def _update_size_option(self):
        self._data.options.size.width = self._gui.rect().width()
        self._data.options.size.height = self._gui.rect().height()

    def get_size(self):
        return self._gui.rect().width(), self._gui.rect().height()

    def set_selected(self, boolean):
        self._gui.setSelected(boolean)

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
        self.set_size((size.width(), size.height()))

    def _update_attaches(self):
        pass

    def set_basic_head_size(self, size):
        self._gui_data.head.size = size

    def set_cut_flag(self, flag):
        self._data.cut_flag = flag
        if flag is True:
            self._gui.hide()
        else:
            self._gui.show()

    def move_by(self, x, y):
        self._gui.moveBy(x, y)
        return self.get_position()

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

    def to_json(self):
        self._update_position_option()
        self._update_size_option()
        return _base._ToJson(self._data._dict).generate()

    def to_data(self):
        return self._json_str_to_data(self.to_json())

    def initializer(self):
        pass

    @classmethod
    def create(cls, root, *args, **kwargs):
        raise NotImplementedError()

    def _set_type(self, text, *args, **kwargs):
        if super(_AbsNodeModel, self)._set_type(text) is True:
            self._gui_data.type.gui_name = kwargs.get('gui_name')
            self._gui_data.type.gui_name_chs = kwargs.get('gui_name_chs')

    def get_type_label(self):
        if self._gui_language == 'chs':
            return self._gui_data.type.gui_name_chs or self._gui_data.type.gui_name
        return self._gui_data.type.gui_name or self._data.type


# node model
class StandardNodeModel(_AbsNodeModel):

    def __init__(self, *args, **kwargs):
        super(StandardNodeModel, self).__init__(*args, **kwargs)
        self._data.category = 'node'

        self._data.options.bypass = False
        self._data.options.add_input_enable = False
        # basic and head
        self._gui_data.basic.size = QtCore.QSize(160, 24)
        self._gui_data.head.size = QtCore.QSize(160, 24)
        #
        self._gui_data.color.border=_base._QtColors.NodeBorder
        self._gui_data.color.background = _base._QtColors.NodeBackground
        # input port
        self._data.inputs = collections.OrderedDict()
        # output port
        self._data.outputs = collections.OrderedDict()
        # port
        self._builtin_data.port = _base._Dict(
            input=_base._Dict(
                gui_cls=None,
                prefix='in'
            ),
            output=_base._Dict(
                gui_cls=None,
                prefix='out'
            )
        )
        self._gui_data.port = _base._Dict(
            size=QtCore.QSize(16, 8),
            spacing=4,
            margin=4
        )
        self._gui_data.add_input = _base._Dict(
            size=QtCore.QSize(32, 16)
        )
        # parameter
        self._data.parameters = collections.OrderedDict()
        self._param_root = _param.ParamRoot(self, self._data.parameters)

    # main
    def update(self, rect):
        # check rect is change
        if rect != self._gui_data.rect or self._gui_data.force_refresh_flag is True:
            self._gui_data.rect = qt_rect(rect)

            x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2

            self._gui_data.basic.rect.setRect(
                x, y, w, h
            )

            hed_size = self._gui_data.head.size
            hed_w, hed_h = hed_size.width(), hed_size.height()

            if self._data.options.add_input_enable is True:
                add_h = hed_h
            else:
                add_h = 0

            head_y = y+add_h

            frm_w, frm_h = 14, 14

            self._gui_data.viewed.rect.setRect(
                x+(hed_h-frm_w)/2, head_y+(hed_h-frm_h)/2, frm_w, frm_h
            )
            self._gui_data.edited.rect.setRect(
                x+(w-hed_h)+(hed_h-frm_w)/2, head_y+(hed_h-frm_h)/2, frm_w, frm_h
            )

            self._gui_data.type.rect.setRect(
                x+hed_h, head_y, w-hed_h*2, hed_h
            )
            self._gui_data.head.rect.setRect(
                x, head_y, w, hed_h
            )

            self.update_prc(rect)

            self._update_attaches()

            return True
        return False

    def update_prc(self, rect):
        pass

    def draw(self, painter, option):
        painter.save()

        self.update(option.rect)

        self._update_select(bool(option.state & QtWidgets.QStyle.State_Selected))

        self.draw_prc(painter, option)

        self.draw_base(painter, option)

        painter.restore()

    def draw_prc(self, painter, option):
        pass

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

        if self.is_bypass():
            background_color = _base._QtColors.NodeBackgroundBypass
        else:
            background_color = self._gui_data.color.background

        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.basic.rect,
            border_color=border_color,
            background_color=background_color,
            border_width=border_width,
            border_radius=2
        )

        # draw type
        type_text = self.get_type_label()

        gui_qt_core.QtItemDrawBase._draw_name_text(
            painter,
            rect=self._gui_data.type.rect,
            text=type_text,
            color=self._gui_data.type.color,
            option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            font=self._gui_data.type.font
        )

        # draw viewed
        if self._gui_data.viewed.value is True:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.viewed.rect,
                border_color=QtGui.QColor(*gui_core.GuiRgba.Purple),
                background_color=QtGui.QColor(*gui_core.GuiRgba.Purple),
                border_width=1,
                border_radius=0
            )
        else:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.viewed.rect,
                border_color=QtGui.QColor(47, 47, 47, 255),
                background_color=QtGui.QColor(47, 47, 47, 255),
                border_width=1,
                border_radius=0
            )

        # draw edited
        if self._gui_data.edited.value is True:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.edited.rect,
                border_color=QtGui.QColor(*gui_core.GuiRgba.NeonGreen),
                background_color=QtGui.QColor(*gui_core.GuiRgba.NeonGreen),
                border_width=1,
                border_radius=0
            )
        else:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.edited.rect,
                border_color=QtGui.QColor(47, 47, 47, 255),
                background_color=QtGui.QColor(47, 47, 47, 255),
                border_width=1,
                border_radius=0
            )

        self.draw_base_prc(painter, option)

    def draw_base_prc(self, painter, option):
        pass

    # input
    def set_input_prefix(self, text):
        self._builtin_data.port.input.prefix = text

    def add_input(self, name=None, parent_path=None, port_path=None, prefix=None, *args, **kwargs):
        prefix = prefix or self._builtin_data.port.input.prefix
        if port_path is None:
            if name is None:
                port_path = self._find_next_port_path(self._data.inputs, prefix, parent_path)
            else:
                if parent_path is None:
                    port_path = name
                else:
                    port_path = '{}.{}'.format(parent_path, name)

        if port_path in self._data.inputs:
            return False, self._data.inputs[port_path]

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()

        port = self._builtin_data.port.input.gui_cls(self._gui, prt_w, prt_h)
        atr_path = bsc_core.BscAttributePath.join_by(self.get_path(), port_path)

        model = port._model
        self._data.inputs[port_path] = model
        self._auto_resize()
        self._update_inputs()
        port._update()

        port_path_opt = bsc_core.BscPortPathOpt(port_path)

        type_name = 'input'
        model._set_node(self)
        model._set_type(type_name)
        model._set_path(atr_path)
        model._set_port_path(port_path)
        model.set_name(port_path_opt.get_name())

        return True, model

    def remove_input(self, port_path):
        port = self.get_input(port_path)
        if port:
            gui = port._gui
            gui.setParentItem(None)
            gui.scene().removeItem(gui)
            self._data.inputs.pop(port_path)

        self._update_inputs()

    def _generate_next_input_args(self):
        for i in self.get_inputs():
            if i.has_source() is False:
                return False, i
        if self._data.options.add_input_enable is True:
            return self.add_input()
        return False, None
    
    def get_connectable_input(self):
        flag, port = self._generate_next_input_args()
        return port

    def _generate_next_input_path(self):
        prefix = self._builtin_data.port.input.prefix
        return self._find_next_port_path(self._data.inputs, prefix)

    def _add_input_by_data(self, data):
        port_path = data['path']
        flag, port = self.add_input(port_path=port_path)
        return port

    def get_inputs(self):
        return list(self._data.inputs.values())

    def number_of_inputs(self):
        return len(self._data.inputs)

    def get_input(self, port_path):
        return self._data.inputs.get(port_path)

    def _update_inputs(self):
        rect = self._gui.boundingRect()
        x, y = 0, 0
        w, h = rect.width(), rect.height()

        mrg = self._gui_data.port.margin
        spc = self._gui_data.port.spacing

        ports = self.get_inputs()
        prt_c = len(ports)
        if not prt_c:
            return

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()
        prt_ws = prt_c*prt_w+spc*(prt_c-1)+mrg*2
        prt_x, prt_y = x+(w-prt_ws)/2+mrg, y-prt_h-1

        x_c = prt_x
        for i in ports:
            i._gui.setPos(x_c, prt_y)
            x_c += prt_w+spc

    # output
    def set_output_prefix(self, text):
        self._builtin_data.port.output.prefix = text

    def add_output(self, name=None, parent_path=None, port_path=None, prefix=None, *args, **kwargs):
        if port_path is None:
            if name is None:
                prefix = prefix or self._builtin_data.port.output.prefix
                port_path = self._find_next_port_path(self._data.inputs, prefix, parent_path)
            else:
                if parent_path is None:
                    port_path = name
                else:
                    port_path = '{}.{}'.format(parent_path, name)

        if port_path in self._data.outputs:
            return False, self._data.outputs[port_path]

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()

        port = self._builtin_data.port.output.gui_cls(self._gui, prt_w, prt_h)
        atr_path = bsc_core.BscAttributePath.join_by(self.get_path(), port_path)

        model = port._model
        self._data.outputs[port_path] = model
        self._auto_resize()
        self._update_outputs()
        port._update()

        port_path_opt = bsc_core.BscPortPathOpt(port_path)

        type_name = 'output'
        model._set_node(self)
        model._set_type(type_name)
        model._set_path(atr_path)
        model._set_port_path(port_path)
        model.set_name(port_path_opt.get_name())

        return True, model

    def number_of_outputs(self):
        return len(self._data.outputs)

    def _add_output_by_data(self, data):
        name = data['name']
        flag, port = self.add_output(name)
        return port

    def get_outputs(self):
        return list(self._data.outputs.values())

    def get_output(self, port_path):
        return self._data.outputs.get(port_path)

    def _update_outputs(self):
        rect = self._gui.boundingRect()
        x, y = 0, 0
        w, h = rect.width(), rect.height()

        mrg = self._gui_data.port.margin
        spc = self._gui_data.port.spacing

        ports = self.get_outputs()
        prt_c = len(ports)
        if not prt_c:
            return

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()
        prt_ws = prt_c*prt_w+spc*(prt_c-1)+mrg*2
        prt_x, prt_y = x+(w-prt_ws)/2+mrg, y+h+2

        x_c = prt_x
        for i in ports:
            i._gui.setPos(x_c, prt_y)
            x_c += prt_w+spc

    # connection, source
    def has_source_connections(self):
        for i in self.get_inputs():
            if i.has_source():
                return True
        return False

    def get_source_connection_path_set(self):
        set_ = set()
        for i in self.get_inputs():
            set_.update(i.get_connection_path_set())
        return set_

    def get_source_connections_itr(self):
        for i in self.get_inputs():
            for j in i.get_connections_itr():
                yield j

    # target
    def has_target_connections(self):
        for i in self.get_outputs():
            if i.has_targets():
                return True
        return False

    def get_target_connection_path_set(self):
        set_ = set()
        for i in self.get_outputs():
            set_.update(i.get_connection_path_set())
        return set_

    def get_target_connections_itr(self):
        for i in self.get_outputs():
            for j in i.get_connections_itr():
                yield j

    def get_connection_path_set(self):
        set_ = set()
        set_.update(self.get_source_connection_path_set())
        set_.update(self.get_target_connection_path_set())
        return set_

    def get_target_nodes(self):
        list_ = []
        for i in self.get_outputs():
            for j in i.get_target_itr():
                list_.append(j.get_node())
        return list_

    # parameter
    def add_parameter(self, type_name, name=None, parent_path=None, port_path=None, *args, **kwargs):
        pass

    # name
    def set_name(self, text):
        if super(StandardNodeModel, self).set_name(text) is True:
            self._gui._name_aux.setPlainText(text)
            self._auto_resize()

    # hover
    def _update_hover(self, flag):
        if flag != self._gui_data.hover.flag:
            self._gui_data.hover.flag = flag

    # select
    def _update_select(self, flag):
        if flag != self._gui_data.select.flag:
            self._gui_data.select.flag = flag

    def _auto_resize(self):
        bsc_size = self._gui_data.basic.size
        bsc_w, bsc_h = bsc_size.width(), bsc_size.height()

        # port
        mrg = self._gui_data.port.margin
        spc = self._gui_data.port.spacing

        prt_size = self._gui_data.port.size
        prt_w, prt_h = prt_size.width(), prt_size.height()

        ipt_c = self.number_of_inputs()
        opt_c = self.number_of_outputs()

        prt_w_max = max(ipt_c*prt_w+spc*(ipt_c-1)+mrg*2, opt_c*prt_w+spc*(opt_c-1)+mrg*2)

        type_text = self.get_type_label()

        # frm
        hed_size = self._gui_data.head.size
        hed_w, hed_h = hed_size.width(), hed_size.height()
        nme_w = QtGui.QFontMetrics(self._gui_data.type.font).width(type_text)+16
        frm_w = nme_w+hed_h*2

        # add port
        if self._data.options.add_input_enable is True:
            add_h = hed_h
        else:
            add_h = 0

        w, h = max(bsc_w, prt_w_max, frm_w), bsc_h+add_h
        if w:
            self.set_size((w, h))

    def _update_attaches(self):
        self._update_name()
        self._update_bypass()
        self._update_add_input()
        self._update_inputs()
        self._update_outputs()

    def _update_name(self):
        rect = self._gui_data.head.rect

        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()

        self._gui._name_aux.setPos(x+w, y)

    def set_options(self, options):
        super(StandardNodeModel, self).set_options(options)

        self.set_bypass(options['bypass'])
        self.set_add_port_enable(options['add_input_enable'])

    # bypass
    def _update_bypass(self):
        rect = self._gui.boundingRect()
        x, y = 0, 0
        w, h = rect.width(), rect.height()

        w_0, h_0 = 96, 96

        self._gui._bypass_aux.setRect(
            x+(w-w_0)/2, y+(h-h_0)/2, w_0, h_0
        )

    def set_bypass(self, boolean):
        self._data.options.bypass = boolean
        self._gui._bypass_aux.setVisible(boolean)
        self.update_root_gui()

    def is_bypass(self):
        return self._data.options.bypass

    def _on_swap_bypass(self):
        self.set_bypass(not self.is_bypass())

    # add input
    def set_add_port_enable(self, boolean):
        self._data.options.add_input_enable = boolean
        self._gui._add_input_aux.setVisible(boolean)

    def _update_add_input(self):
        if self._data.options.add_input_enable is True:
            rect = self._gui.boundingRect()
            x, y = 0, 0
            w, h = rect.width(), rect.height()

            hed_size = self._gui_data.head.size
            hed_w, hed_h = hed_size.width(), hed_size.height()

            size_0 = self._gui_data.add_input.size
            w_0, h_0 = size_0.width(), size_0.height()

            self._gui._add_input_aux.setRect(
                x+(w-w_0)/2, y+(hed_h-h_0)/2, w_0, h_0
            )

    # viewed
    def set_viewed(self, boolean):
        if boolean is True:
            self.root_model.set_viewed_node(self)
        else:
            if self.root_model.has_viewed_nodes():
                if self.root_model._check_node_viewed(self) is False:
                    self._update_viewed(boolean)

        self.update_root_gui()

    def _update_viewed(self, boolean):
        self._gui_data.viewed.value = boolean

        self.update_root_gui()

    def is_viewed(self):
        return self._gui_data.viewed.value

    def _on_swap_viewed(self):
        self.set_viewed(not self.is_viewed())

    def _check_viewed(self, point):
        if self._gui_data.viewed.rect.contains(point):
            return True
        return False

    # edited
    @_base.EventFactory.send(_base.EventTypes.NodeSetEdited)
    def set_edited(self, boolean):
        if boolean is True:
            self.root_model.set_edited_node(self)
        else:
            if self.root_model.has_edited_nodes():
                if self.root_model._check_node_edited(self) is False:
                    self._update_edited(boolean)

    def _update_edited(self, boolean):
        self._gui_data.edited.value = boolean

        self.update_root_gui()

    def is_edited(self):
        return self._gui_data.edited.value

    def _on_swap_edited(self):
        self.set_edited(not self.is_edited())

    def _check_edited(self, point):
        if self._gui_data.edited.rect.contains(point):
            return True
        return False

    def do_delete(self):
        for i in self.get_source_connections_itr():
            i.do_delete()

        for i in self.get_target_connections_itr():
            i.do_delete()

        self.root_model._unregister_node(self)
    
    # parameter
    @property
    def parameters(self):
        return self._param_root
    
    def set(self, key, value):
        self._param_root.get_parameter(key).set_value(value)
    
    def get(self, key):
        return self._param_root.get_parameter(key).get_value()


# media
class MediaNodeModel(StandardNodeModel):
    def __init__(self, *args, **kwargs):
        super(MediaNodeModel, self).__init__(*args, **kwargs)
        self._data.options.image = None

        self._data.options.video = None

        self._gui_data.image_enable = False
        self._gui_data.video_enable = False
        self._gui_data.basic.size = QtCore.QSize(160, 160)

    def set_options(self, options):
        super(MediaNodeModel, self).set_options(options)

        self.set_image(options['image'])

    def set_image(self, file_path):
        if file_path is not None:
            self._gui_data.image = _base._Dict(
                load_flag=False,
                pixmap=None,
                size=None,

                reload_flag=False,

                rect=QtCore.QRect(),
                image_rect=QtCore.QRect(),
                margin=4
            )

            self._gui_data.image_enable = False
            self._gui_data.image.load_flag = True
            self._data.options.image = file_path

    def _load_image_auto(self):
        if self._data.options.image is not None:
            if self._gui_data.image.load_flag is True:
                self._gui_data.image.load_flag = False
                self._load_image()

    def _load_image(self):
        def cache_fnc_():
            _file_path = self._data.options.image

            if self._gui_data.image.reload_flag is True:
                self.root_model.remove_image_cache(_file_path)

            _ = self.root_model.pull_image_cache(_file_path)
            if _:
                return _

            _image = QtGui.QImage()
            _image.load(_file_path)
            if _image.isNull() is False:
                _pixmap = QtGui.QPixmap.fromImage(_image, QtCore.Qt.AutoColor)
                _cache = [_pixmap]
                self.root_model.push_image_cache(_file_path, _cache)
                return _cache
            return []

        def build_fnc_(data_):
            if self.root_model._close_flag is True:
                return

            if data_:
                _pixmap = data_[0]
                self._gui_data.image_enable = True
                self._gui_data.image.pixmap = _pixmap
                self._gui_data.image.size = _pixmap.size()
                self.update_root_gui()

        trd = self.root_model._gui._generate_thread_(
            cache_fnc_, build_fnc_
        )
        trd.start()

    def set_video(self, file_path):
        if file_path is not None:
            self._gui_data.video = _base._Dict(
                load_flag=False,
                capture_opt=None,
                size=None,
                index=0,
                # in play is disable show image at default index
                index_default=0,
                index_maximum=1,
                fps=24,

                pixmap_cache_dict={},

                rect=QtCore.QRect(),
                image_rect=QtCore.QRect(),
                margin=4
            )
            self._data.options.video = file_path
            self._gui_data.video.load_flag = True

    def _load_video_auto(self):
        if self._data.options.video is not None:
            if self._gui_data.video.load_flag is True:
                self._gui_data.video.load_flag = False
                self._load_video()

    def _load_video(self):
        def cache_fnc_():
            _file_path = self._data.options.video
            _ = self.root_model.pull_video_cache(_file_path)
            if _:
                return _

            import lxbasic.cv.core as bsc_cv_core

            _capture_opt = bsc_cv_core.VideoCaptureOpt(_file_path)
            # catch first frame
            if _capture_opt.is_valid():
                _image = _capture_opt.generate_qt_image(QtGui.QImage, frame_index=_capture_opt.get_middle_frame_index())
                _frame_count = _capture_opt.get_frame_count()
                _fps = _capture_opt.get_frame_rate()
                _pixmap = QtGui.QPixmap.fromImage(_image, QtCore.Qt.AutoColor)
                _cache = [_capture_opt, _pixmap, _frame_count, _fps]
                self.root_model.push_video_cache(_file_path, _cache)
                return _cache
            return []

        def build_fnc_(data_):
            if self.root_model._close_flag is True:
                return

            if data_:
                _capture_opt, _pixmap, _frame_count, _fps = data_
                self._gui_data.video_enable = True
                self._gui_data.video.capture_opt = _capture_opt
                self._gui_data.video.pixmap = _pixmap
                self._gui_data.video.size = _pixmap.size()
                self._gui_data.video.index_default = int(_frame_count/2)
                self._gui_data.video.index_maximum = _frame_count-1
                self._gui_data.video.fps = _fps

                self.update_root_gui()

        trd = self.root_model._gui._generate_thread_(
            cache_fnc_, build_fnc_
        )
        trd.start()

    def update_prc(self, rect):
        x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2

        hed_size = self._gui_data.head.size
        hed_w, hed_h = hed_size.width(), hed_size.height()

        if self._gui_data.image_enable is True:
            mrg = self._gui_data.image.margin

            frm_x, frm_y = x+mrg, y+hed_h+mrg
            frm_w, frm_h = w-mrg*2, h-hed_h-mrg*2

            self._gui_data.image.rect.setRect(
                x+mrg, y+hed_h+mrg, frm_w, frm_h
            )

            img_w, img_h = self._gui_data.image.size.width(), self._gui_data.image.size.height()
            img_x_, img_y_, img_w_, img_h_ = bsc_core.BscSize.fit_to_center(
                (img_w, img_h), (frm_w, frm_h)
            )
            self._gui_data.image.image_rect.setRect(
                frm_x+img_x_, frm_y+img_y_, img_w_, img_h_
            )
        elif self._gui_data.video_enable is True:
            mrg = self._gui_data.video.margin

            frm_x, frm_y = x+mrg, y+hed_h+mrg
            frm_w, frm_h = w-mrg*2, h-hed_h-mrg*2

            self._gui_data.video.rect.setRect(
                x+mrg, y+hed_h+mrg, frm_w, frm_h
            )

            img_w, img_h = self._gui_data.video.size.width(), self._gui_data.video.size.height()
            img_x_, img_y_, img_w_, img_h_ = bsc_core.BscSize.fit_to_center(
                (img_w, img_h), (frm_w, frm_h)
            )
            self._gui_data.video.image_rect.setRect(
                frm_x+img_x_, frm_y+img_y_, img_w_, img_h_
            )

    def draw_prc(self, painter, option):
        self._load_image_auto()
        self._load_video_auto()

    def draw_base_prc(self, painter, options):
        if self._gui_data.image_enable is True:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.image.rect,
                border_color=QtGui.QColor(31, 31, 31, 255),
                background_color=QtGui.QColor(31, 31, 31, 255),
                border_width=1,
                border_radius=0
            )
            gui_qt_core.QtItemDrawBase._draw_pixmap(
                painter,
                rect=self._gui_data.image.image_rect,
                pixmap=self._gui_data.image.pixmap
            )
        elif self._gui_data.video_enable is True:
            gui_qt_core.QtItemDrawBase._draw_frame(
                painter,
                rect=self._gui_data.video.rect,
                border_color=QtGui.QColor(31, 31, 31, 255),
                background_color=QtGui.QColor(31, 31, 31, 255),
                border_width=1,
                border_radius=0
            )
            gui_qt_core.QtItemDrawBase._draw_pixmap(
                painter,
                rect=self._gui_data.video.image_rect,
                pixmap=self._gui_data.video.pixmap
            )


# backdrop
class BackdropModel(_AbsNodeModel):
    def __init__(self, *args, **kwargs):
        super(BackdropModel, self).__init__(*args, **kwargs)
        self._data.category = 'backdrop'
        # basic and head
        self._gui_data.basic.size = QtCore.QSize(320, 240)
        self._gui_data.head.size = QtCore.QSize(320, 24)
        #
        self._gui_data.color.border = _base._QtColors.BackdropBorder
        self._gui_data.color.background = _base._QtColors.BackdropBackground
        self._gui_data.color.alpha = 31

        self._gui_data.name.color = _base._QtColors.BackdropName

        self._gui_data.move = _base._Dict(
            start_position=QtCore.QPointF(),
            start_point=QtCore.QPointF(),
            node_position_data=[],
            node_set=set(),
        )

        self._gui_data.resize = _base._Dict(
            start_point=QtCore.QPointF(),
            start_rect=QtCore.QRect(),
            rect=QtCore.QRectF(),
            icon_rect=QtCore.QRectF(),
            icon=_base._Dict(
                file=gui_core.GuiIcon.get('resize'),
            )
        )

        self._gui_data.description = _base._Dict(
            rect=QtCore.QRect(),
            text_rect=QtCore.QRect(),
            text='',
            color=QtGui.QColor(223, 223, 223, 255),
            font=gui_qt_core.QtFont.generate(size=12)
        )

        self.set_menu_data(
            [
                [
                    'Backdrop', 'file/folder',
                    [
                        ('Set Description', 'file/file', self._add_description_action)
                    ]
                ]
            ]
        )

    def _add_description_action(self):
        pass

    def set_description(self, text):
        self._gui_data.description.text = text

    def update(self, rect):
        # check rect is change
        if rect != self._gui_data.rect or self._gui_data.force_refresh_flag is True:
            self._gui_data.rect = qt_rect(rect)

            x, y, w, h = rect.x()+1, rect.y()+1, rect.width()-2, rect.height()-2

            self._gui_data.basic.rect.setRect(
                x, y, w, h
            )

            hed_size = self._gui_data.head.size
            hed_w, hed_h = hed_size.width(), hed_size.height()

            self._gui_data.head.rect.setRect(
                x, y, w, hed_h
            )

            mrg = 4

            self._gui_data.description.rect.setRect(
                x+mrg, y+hed_h+mrg, w-mrg*2, h-hed_h-mrg*2
            )
            self._gui_data.description.text_rect.setRect(
                x+mrg*2, y+hed_h+mrg*2, w-mrg*4, h-hed_h-mrg*4
            )

            icn_w, icn_h = 20, 20

            self._gui_data.resize.rect.setRect(
                x+w-icn_w-mrg*2, y+h-icn_h-mrg*2, icn_w+mrg*2, icn_h+mrg*2
            )
            self._gui_data.resize.icon_rect.setRect(
                x+w-icn_w-mrg*2, y+h-icn_h-mrg*2, icn_w, icn_h
            )

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
            border_radius=0
        )

        # type
        gui_qt_core.QtItemDrawBase._draw_name_text(
            painter, self._gui_data.type.rect, self._data.type,
            color=self._gui_data.type.color,
            option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            font=self._gui_data.type.font
        )

        # headline
        gui_qt_core.QtItemDrawBase._draw_line(
            painter, point_0=self._gui_data.head.rect.bottomLeft(), point_1=self._gui_data.head.rect.bottomRight(),
            border_color=border_color, border_width=border_width
        )

        # description
        gui_qt_core.QtItemDrawBase._draw_frame(
            painter,
            rect=self._gui_data.description.rect,
            border_color=border_color,
            background_color=QtGui.QColor(0, 0, 0, 0),
            border_width=1,
            border_radius=4
        )

        gui_qt_core.QtItemDrawBase._draw_description_text(
            painter,
            rect=self._gui_data.description.text_rect,
            text=self._gui_data.description.text,
            color=self._gui_data.description.color,
            font=self._gui_data.description.font
        )

        # resize
        gui_qt_core.QtItemDrawBase._draw_icon_by_file(
            painter,
            rect=self._gui_data.resize.icon_rect,
            file_path=self._gui_data.resize.icon.file
        )

    def _check_move(self, point):
        if self._gui_data.head.rect.contains(point):
            return True
        return False

    def _check_scene_move(self, point):
        return self._check_move(point-self._gui.pos())

    def do_move_start(self, event):
        self._gui_data.move.start_point = event.pos()
        self._gui_data.move.start_position = self.get_position()
        x, y = self._gui.x(), self._gui.y()
        rect = self._gui.boundingRect()
        w, h = rect.width(), rect.height()

        node_position_data = []

        self.root_model.clear_selection()

        self._gui.setSelected(True)
        all_items = self.scene._get_items_by_rect(x, y, w, h)
        for i in all_items:
            if i.ENTITY_TYPE == _base.EntityTypes.Node:
                i_node = i._model
                node_position_data.append(
                    (i_node, i_node.get_position())
                )
                # i.setSelected(True)

        self._gui_data.move.node_position_data = node_position_data

    def do_move(self, event):
        delta = event.pos()-self._gui_data.move.start_point
        x, y = delta.x(), delta.y()

        self._gui.moveBy(x, y)

        for i in self._gui_data.move.node_position_data:
            i[0]._gui.moveBy(x, y)

    def _push_move_cmd(self):
        data = [
            (
                _undo.QtUndoCommand.Actions.NodeMove,
                (self.get_path(), self._gui_data.move.start_position, self.get_position())
            )
        ]
        for i in self._gui_data.move.node_position_data:
            i_node = i[0]
            data.append(
                (
                    _undo.QtUndoCommand.Actions.NodeMove,
                    (i_node.get_path(), i[1], i_node.get_position())
                )
            )
        self.root_model._gui._undo_stack.push(_undo.QtUndoCommand(self.root_model, data))

    def do_move_end(self):
        self._push_move_cmd()

    def _check_scene_resize(self, point):
        return self._check_resize(point-self._gui.pos())

    def _check_resize(self, point):
        if self._gui_data.resize.rect.contains(point):
            return True
        return False

    def do_resize_start(self, event):
        self._gui_data.resize.start_point = event.pos()
        self._gui_data.resize.start_rect = self._gui.rect()

    def do_resize_move(self, event):
        delta = event.pos()-self._gui_data.resize.start_point
        rect = self._gui_data.resize.start_rect
        w, h = rect.width()+delta.x(), rect.height()+delta.y()
        w, h = max(min(w, 4096), 128), max(min(h, 4096), 64)
        self.set_size((w, h))

    def _push_resize_cmd(self):
        rect = self._gui_data.resize.start_rect
        data = [
            (_undo.QtUndoCommand.Actions.NodeResize, (self.get_path(), (rect.width(), rect.height()), self.get_size()))
        ]
        self.root_model._gui._undo_stack.push(_undo.QtUndoCommand(self.root_model, data))

    def do_resize_end(self):
        self._push_resize_cmd()

    def _auto_resize(self):
        bsc_size = self._gui_data.basic.size
        bsc_w, bsc_h = bsc_size.width(), bsc_size.height()

        # frm
        hed_size = self._gui_data.head.size
        hed_w, hed_h = hed_size.width(), hed_size.height()

        type_text = self.get_type_label()

        nme_w = QtGui.QFontMetrics(self._gui_data.type.font).width(type_text)+16
        frm_w = nme_w+hed_h*2

        w, h = max(bsc_w, frm_w), bsc_h
        if w:
            self.set_size((w, h))