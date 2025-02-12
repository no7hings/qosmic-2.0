# coding:utf-8
import lxuniverse.abstracts as unr_abstracts
# qt widgets
from ....qt.widgets import base as _qt_wgt_base

from ....qt.widgets import utility as _qt_wgt_utility
# proxy widgets
from .. import container as _container

from . import _port_base


# node
class _PortStackGroup(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(_PortStackGroup, self).__init__()

    def get_key(self, obj):
        return obj.get_name()


class PrxNodePortGroup(_port_base.AbsPrxPortBaseDef):
    WIDGET_TYPE = 'group'
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = _PortStackGroup

    def __init__(self, port_path, node, is_pseudo_root=False):
        self._init_prx_port_base_def('group', port_path)
        self._set_node(node)
        if is_pseudo_root is True:
            self._set_use_as_pseudo_root()

        self._prx_widget = _container.PrxHToolGroup()
        self._prx_widget.set_height_match_to_minimum()
        self._qt_widget = self._prx_widget.widget
        self._prx_widget.set_name(self.get_gui_name())
        self._prx_widget.set_expanded(True)
        self._port_layout = self._prx_widget._layout
        self._port_layout.setContentsMargins(8, 0, 0, 0)
        self._port_layout.setSpacing(2)
        #
        self._port_stack = self.PORT_STACK_CLS()
        # default use -1
        self._label_width_maximum = -1

    def get_gui_name(self):
        if self.get_is_pseudo_root():
            return self.get_node().get_path()
        return self._label

    def set_gui_name(self, text):
        self._prx_widget.set_name(text)

    def create_child_group(self, name):
        if self.get_is_pseudo_root() is True:
            child_port_path = name
        else:
            child_port_path = '{}.{}'.format(self._port_path, name)
        #
        group = self.__class__(child_port_path, self.get_node())
        group._prx_widget.set_name_font_size(8)
        group._prx_widget.set_name_icon_enable(False)
        group._prx_widget.set_expand_icon_names(
            'qt-style/branch-open', 'qt-style/branch-close'
        )
        group._prx_widget.widget._set_line_draw_enable_(True)
        self._port_layout.addWidget(group._prx_widget._qt_widget)
        self._port_stack.add_object(group)
        return group

    def add_child(self, port):
        port_cur = port
        join_next_pre, port_pre = self._get_pre_child_args()
        join_next_cur = port_cur._get_join_next_flag()
        #
        condition = join_next_pre, join_next_cur
        if condition == (False, False):
            widget_cur = _qt_wgt_utility.QtTranslucentWidget()
            self._port_layout.addWidget(widget_cur)
            port_cur.set_main_widget(widget_cur)
            layout_cur = _qt_wgt_base.QtHBoxLayout(widget_cur)
            layout_cur.setContentsMargins(0, 0, 0, 0)
            layout_cur._set_align_as_top_()
            port_cur._set_layout_(layout_cur)
            #
            cur_key_widget = _qt_wgt_utility.QtTranslucentWidget()
            cur_key_widget.hide()
            port_cur._set_key_widget_(cur_key_widget)
            layout_cur.addWidget(cur_key_widget)
            cur_key_layout = _qt_wgt_base.QtHBoxLayout(cur_key_widget)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_as_top_()
            # + key
            cur_key_layout.addWidget(port_cur._prx_port_enable._qt_widget)
            cur_key_layout.addWidget(port_cur._prx_port_label._qt_widget)
            # + value
            layout_cur.addWidget(port_cur._prx_port_input._qt_widget)
            if port_cur.KEY_HIDE is False:
                cur_key_widget.show()
            if port_cur.LABEL_HIDED is False:
                port_cur._prx_port_label._qt_widget.show()
                cur_key_widget.show()
        # pre is not join and current join to next
        elif condition == (False, True):
            widget_cur = _qt_wgt_utility.QtTranslucentWidget()
            self._port_layout.addWidget(widget_cur)
            port_cur.set_main_widget(widget_cur)
            layout_cur = _qt_wgt_base.QtHBoxLayout(widget_cur)
            layout_cur.setContentsMargins(0, 0, 0, 0)
            layout_cur.setSpacing(2)
            layout_cur._set_align_as_top_()
            port_cur._set_layout_(layout_cur)
            key_widget_cur = _qt_wgt_utility.QtTranslucentWidget()
            # key_widget_cur.hide()
            port_cur._set_key_widget_(key_widget_cur)
            layout_cur.addWidget(key_widget_cur)
            cur_key_layout = _qt_wgt_base.QtHBoxLayout(key_widget_cur)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_as_top_()
            # + key
            #   + enable
            cur_key_layout.addWidget(port_cur._prx_port_enable._qt_widget)
            #   + label
            cur_key_layout.addWidget(port_cur._prx_port_label._qt_widget)
            # + value
            #   + input
            layout_cur.addWidget(port_cur._prx_port_input._qt_widget)
            port_cur._update_sub_name()
            # join
            port_cur._register_join_layout(layout_cur)
            if port_cur.KEY_HIDE is False:
                key_widget_cur.show()
            if port_cur.LABEL_HIDED is False:
                port_cur._prx_port_label._qt_widget.show()
                key_widget_cur.show()
        # pre is join and current also
        elif condition == (True, True):
            # hide status and label
            layout_pre = port_pre._get_join_layout()
            layout_pre.addWidget(port_cur._prx_port_enable._qt_widget)
            port_cur._prx_port_enable._qt_widget.hide()
            layout_pre.addWidget(port_cur._prx_port_label._qt_widget)
            port_cur._prx_port_label._qt_widget.hide()
            port_cur._update_sub_name()
            layout_pre.addWidget(port_cur._prx_port_input._qt_widget)
            port_cur._register_join_layout(layout_pre)
        # pre is join but current is not
        elif condition == (True, False):
            # hide status and label
            layout_pre = port_pre._get_join_layout()
            layout_pre.addWidget(port_cur._prx_port_enable._qt_widget)
            port_cur._prx_port_enable._qt_widget.hide()
            layout_pre.addWidget(port_cur._prx_port_label._qt_widget)
            port_cur._prx_port_label._qt_widget.hide()
            port_cur._update_sub_name()
            layout_pre.addWidget(port_cur._prx_port_input._qt_widget)
        #
        port_cur._prx_port_input.set_show()
        #
        self._port_stack.add_object(port_cur)
        port_cur.set_group(self)
        #
        self.update_children_name_width()
        return port

    def _get_pre_child_args(self):
        ports = self._port_stack.get_objects()
        if ports:
            port_pre = ports[-1]
            if hasattr(port_pre, '_get_join_next_flag') is True:
                return port_pre._get_join_next_flag(), port_pre
            return False, port_pre
        return False, None

    def get_child(self, name):
        return self._port_stack.get_object(name)

    def compute_children_name_width(self):
        widths = []
        children = self.get_children()
        for i_child in children:
            if i_child.get_category() == 'group':
                continue
            #
            if i_child.KEY_HIDE is False:
                if i_child.LABEL_HIDED is False:
                    i_width = i_child._prx_port_label.get_name_draw_width()+16
                else:
                    i_width = 0
                #
                if i_child.get_use_enable() is True:
                    i_width += 22
                #
                widths.append(i_width)
        if widths:
            return max(widths)
        return 0

    def update_children_name_width(self):
        width = self.compute_children_name_width()
        children = self.get_children()
        for i_child in children:
            if i_child.get_category() == 'group':
                continue
            #
            i_key_widget = i_child._key_widget
            if i_key_widget is not None:
                i_width = width
                if i_child.KEY_HIDE is False:
                    if i_width > 0:
                        if i_child.LABEL_HIDED is False:
                            i_key_widget.setFixedWidth(int(i_width))
                        else:
                            if i_child.get_use_enable() is True:
                                i_key_widget.setFixedWidth(22)
                            else:
                                i_key_widget.setFixedWidth(0)
                                i_key_widget.hide()
                    else:
                        i_key_widget.setFixedWidth(0)
                        i_key_widget.hide()
                else:
                    i_key_widget.setFixedWidth(0)
                    i_key_widget.hide()

    def set_expanded(self, boolean):
        self._prx_widget.set_expanded(boolean)

    def set_reset(self):
        pass

    def set_tool_tip(self, text):
        self._prx_widget.set_tool_tip(text)

    def set_visible(self, boolean):
        self._prx_widget.set_visible(boolean)

    def __str__(self):
        return '{}(node="{}", port_path="{}")'.format(
            self.get_type(),
            self.get_node_path(),
            self.get_port_path()
        )

    def __repr__(self):
        return self.__str__()
