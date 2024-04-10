# coding:utf-8
import six
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import input_for_guide as gui_qt_wgt_input_for_guide

from ...qt.widgets import item_for_list as gui_qt_wgt_item_for_list

from ...qt.widgets import item_for_tree as gui_qt_wgt_item_for_tree
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class AbsPrxTreeDef(object):
    def _set_prx_tree_def_init_(self):
        pass

    @classmethod
    def _add_item_(cls, add_method, *args, **kwargs):
        if kwargs:
            if 'name' in kwargs:
                _name = kwargs['name']
                if isinstance(_name, (tuple, list)):
                    name = _name
                else:
                    name = [_name]
            else:
                name = None
            #
            if 'item_class' in kwargs:
                item_class = kwargs['item_class']
            else:
                item_class = PrxTreeItem
            #
            if 'tool_tip' in kwargs:
                _tool_tip = kwargs['tool_tip']
                if isinstance(_tool_tip, (tuple, list)):
                    tool_tip = _tool_tip
                else:
                    tool_tip = [_tool_tip]
            else:
                tool_tip = None
            #
            if 'icon' in kwargs:
                _file_icon = kwargs['icon']
                if isinstance(_file_icon, (tuple, list)):
                    file_icons = _file_icon
                else:
                    file_icons = [_file_icon]
            else:
                file_icons = None
            #
            if 'icon_name_text' in kwargs:
                _name_icon = kwargs['icon_name_text']
                if isinstance(_name_icon, (tuple, list)):
                    name_icons = _name_icon
                else:
                    name_icons = [_name_icon]
            else:
                name_icons = None
            #
            if 'menu' in kwargs:
                menu = kwargs['menu']
            else:
                menu = None
        else:
            name = None
            item_class = PrxTreeItem
            tool_tip = None
            file_icons = None
            name_icons = None
            menu = None
        #
        if args:
            name = args
        #
        item_prx = item_class()
        #
        if name is not None:
            for column, name_ in enumerate(name):
                item_prx.set_name(name_, column)
        #
        if tool_tip is not None:
            for column, tool_tip_ in enumerate(tool_tip):
                item_prx.set_tool_tip(tool_tip_, column)
        #
        if file_icons is not None:
            for column, i_file_icon in enumerate(file_icons):
                if i_file_icon is not None:
                    item_prx.set_icon_by_file(i_file_icon, column)
        #
        if name_icons is not None:
            for column, i_name_icon in enumerate(name_icons):
                if i_name_icon is not None:
                    item_prx.set_icon_by_name(i_name_icon, column)
        #
        if name is not None:
            pass
        #
        if menu is not None:
            item_prx.set_gui_menu_raw(menu)
        #
        add_method(item_prx.widget)
        item_prx.widget._connect_item_show_()
        #
        if 'filter_key' in kwargs:
            _filter_key = kwargs['filter_key']
            view_prx = item_prx.get_view()
            view_prx._item_dict[_filter_key] = item_prx
        return item_prx


class PrxTreeItemCheckState(object):
    def __init__(self, prx_tree_item):
        self._item_prx = prx_tree_item

    @property
    def widget(self):
        return self._item_prx.widget

    @property
    def item(self):
        return self._item_prx

    def set(self, check_tag, column=0):
        if 'ignore' in check_tag:
            self.set_ignored(column)
        elif 'error' in check_tag:
            self.set_error(column)
        elif 'warning' in check_tag:
            self.set_warning(column)
        else:
            self.set_passed(column)

    def set_normal(self, column=0):
        self.widget.setForeground(column, gui_qt_core.QtBrushes.Text)
        self._item_prx.set_gui_attribute(
            'state', 'normal'
        )

    def set_error(self, column=0):
        self.widget.setForeground(column, gui_qt_core.QtBrushes.TextError)
        self._item_prx.set_gui_attribute(
            'state', 'error'
        )

    def set_warning(self, column=0):
        self.widget.setForeground(column, gui_qt_core.QtBrushes.TextWarning)
        self._item_prx.set_gui_attribute(
            'state', 'warning'
        )

    def set_passed(self, column=0):
        self.widget.setForeground(column, gui_qt_core.QtBrushes.TextCorrect)
        self._item_prx.set_gui_attribute(
            'state', 'adopt'
        )

    def set_ignored(self, column=0):
        self.widget.setForeground(column, gui_qt_core.QtBrushes.TextTemporary)
        self._item_prx.set_gui_attribute(
            'state', 'temporary'
        )


class PrxTreeItem(
    gui_prx_abstracts.AbsPrxWidget,
    gui_prx_abstracts.AbsPrxMenuDef,
    AbsPrxTreeDef,
    gui_prx_abstracts.AbsPrxStateDef,
    #
    gui_prx_abstracts.AbsPrxItemFilterTgtDef,
    gui_prx_abstracts.AbsPrxItemVisibleConnectionDef
):
    QT_WIDGET_CLS = gui_qt_wgt_item_for_tree.QtTreeWidgetItem

    def __init__(self, *args, **kwargs):
        super(PrxTreeItem, self).__init__(*args, **kwargs)
        self._set_prx_tree_def_init_()
        #
        self._gui_menu_raw = []
        self._menu_title = None
        #
        self._loading_item_prx = None

    def get_item(self):
        return self._qt_widget

    item = property(get_item)

    def set_type(self, text):
        self._qt_widget._set_type_text_(text)

    def set_name(self, text, column=0):
        self._qt_widget._set_name_text_(text, column)

    def set_name_orig(self, text):
        self._qt_widget._set_name_text_orig_(text)

    def get_name(self, column=0):
        return self._qt_widget.text(column)

    def get_names(self):
        qt_tree_widget = self._qt_widget.treeWidget()
        column_count = qt_tree_widget.columnCount()
        return [self.get_name(i) for i in range(column_count)]

    def set_names(self, texts):
        for column, text in enumerate(texts):
            self.set_name(text, column)

    def get_path(self):
        parent = self.get_parent()
        if parent:
            if parent.get_name() != '/':
                return '{}/{}'.format(parent.get_path(), self.get_name())
            return '/{}'.format(self.get_name())
        return '/'

    def set_icon_by_file(self, icon, column=0):
        if isinstance(icon, six.string_types):
            self._qt_widget._set_icon_file_path_(icon, column)
        elif isinstance(icon, gui_qt_core.QtGui.QIcon):
            qt_icon = icon
            self._qt_widget._set_icon_(qt_icon, column)

    def set_icon_by_color(self, color, column=0):
        self._qt_widget._set_icon_color_rgb_(color, column)

    def set_icon_by_name(self, text, column=0):
        self._qt_widget._set_icon_name_text_(text, column)

    def get_parent(self):
        _ = self._qt_widget.parent()
        if _ is not None:
            return _.gui_proxy

    def get_ancestors(self):
        return [i.gui_proxy for i in self.item._get_ancestors_()]

    def add_child(self, *args, **kwargs):
        return self._add_item_(
            self._qt_widget.addChild,
            *args, **kwargs
        )

    def clear_children(self):
        self._qt_widget.takeChildren()

    def get_children(self):
        lis = []
        count = self._qt_widget.childCount()
        if count:
            for i in range(count):
                qt_tree_item = self._qt_widget.child(i)
                lis.append(qt_tree_item.gui_proxy)
        return lis

    def get_descendants(self):
        return [i.gui_proxy for i in self._qt_widget._get_descendants_()]

    def get_gui_menu_raw(self):
        return self._qt_widget._get_menu_data_()

    def set_gui_menu_raw(self, raw):
        self._qt_widget._set_menu_data_(raw)

    def set_gui_menu_raw_append(self, raw):
        self._qt_widget._add_menu_data_(raw)

    def set_gui_menu_raw_extend(self, raw):
        self._qt_widget._extend_menu_data_(raw)

    def set_tool_tip(self, raw, column=0):
        self._qt_widget._set_tool_tip_(raw, column)

    def set_tool_tips(self, texts):
        for column, text in enumerate(texts):
            self.set_tool_tip(text, column)

    def set_enable(self, boolean):
        self._qt_widget.setDisabled(not boolean)

    def get_is_enable(self):
        return self._qt_widget.isDisabled() is False

    # checked
    def set_checked(self, boolean=True, extra=False, column=0):
        self._qt_widget.setCheckState(column, [gui_qt_core.QtCore.Qt.Unchecked, gui_qt_core.QtCore.Qt.Checked][boolean])
        if extra is True:
            self._qt_widget._set_check_state_extra_(column)

    def get_check_enable(self):
        return self._qt_widget._get_check_action_is_enable_()

    def set_check_enable(self, boolean, descendants=False, column=0):
        self._qt_widget.setDisabled(not boolean)
        self._qt_widget._set_check_enable_(boolean, column=column)
        if descendants is True:
            [i.set_check_enable(boolean, column=column) for i in self.get_descendants()]

    def get_is_checked(self, column=0):
        return [False, True][self._qt_widget.checkState(column) == gui_qt_core.QtCore.Qt.Checked]

    def get_is_selected(self, column=0):
        return self._qt_widget.isSelected()

    # expanded
    def set_expanded(self, boolean=True, ancestors=False):
        self._qt_widget._set_expanded_(boolean, ancestors)

    # expand
    def set_expand(self, ancestors=False):
        self._qt_widget.setExpanded(True)
        if ancestors is True:
            [i.widget.setExpanded(True) for i in self.get_ancestors()]

    def get_is_expanded(self):
        return self._qt_widget.isExpanded()

    def set_selected(self, boolean):
        self._qt_widget._set_selected_(boolean)

    def set_current(self):
        self._qt_widget._set_current_()

    def set_ancestors_expand(self):
        [i.widget.setExpanded(True) for i in self.get_ancestors()]

    def set_expand_branch(self):
        self.set_expand()
        descendants = self.get_descendants()
        [i.set_expand() for i in descendants]

    def set_expand_branch_by_condition(self, condition_fnc, conditions):
        self.set_expand()
        match_prx_items = []
        descendants = self.get_descendants()
        for i in descendants:
            i_condition = condition_fnc(i)
            if i_condition in conditions:
                match_prx_items.append(i)
            i.set_collapse()
        #
        [i.set_ancestors_expand() for i in match_prx_items]

    # collapse
    def set_collapse(self):
        self._qt_widget.setExpanded(False)

    def set_collapse_branch(self):
        self.set_collapse()
        descendants = self.get_descendants()
        [i.set_collapse() for i in descendants]

    # select
    def set_select(self):
        self._qt_widget.setSelected(True)

    # hidden
    def set_hidden(self, boolean=True, ancestors=False):
        self._qt_widget.setHidden(boolean)
        self.set_gui_attribute('visible', not boolean)
        if ancestors is True:
            [i.set_visible_by_has_visible_children() for i in self.get_ancestors()]
        #
        self.set_visible_connection_refresh()

    def get_is_hidden(self, ancestors=False):
        return self._qt_widget._get_is_hidden_(ancestors=ancestors)

    def set_emit_send_enable(self, boolean):
        self._qt_widget._set_emit_send_enable_(boolean)

    def set_visible(self, boolean, ancestors=False):
        self.set_hidden(not boolean, ancestors=ancestors)

    def get_is_visible(self, ancestors=False):
        return not self._qt_widget._get_is_hidden_(ancestors=ancestors)

    def set_force_hidden(self, boolean):
        self._qt_widget._set_force_hidden_(boolean)

    def set_tag_filter_tgt_key_add(self, key, ancestors=False):
        gui_prx_abstracts.AbsPrxItemFilterTgtDef.set_tag_filter_tgt_key_add(
            self, key
        )
        if ancestors is True:
            self._set_tag_filter_tgt_ancestors_update_()

    def _set_tag_filter_tgt_ancestors_update_(self):
        parent_item_prxes = self.get_ancestors()
        tag_filter_tgt_mode = self.get_tag_filter_tgt_mode()
        tag_filter_tgt_keys = self.get_tag_filter_tgt_keys()
        for parent_item_prx in parent_item_prxes:
            for tag_filter_tgt_key in tag_filter_tgt_keys:
                parent_item_prx.set_tag_filter_tgt_key_add(tag_filter_tgt_key)
            #
            parent_item_prx.set_tag_filter_tgt_mode(tag_filter_tgt_mode)
            parent_item_prx.set_tag_filter_tgt_statistic_enable(False)

    def set_tag_filter_src_key_add(self, key):
        lis = self.get_gui_attribute(
            'tag_filter_src_keys',
            default=[]
        )
        if key not in lis:
            lis.append(key)
        #
        self.set_gui_attribute('tag_filter_src_keys', lis)

    def get_tag_filter_src_keys(self):
        return self.get_gui_attribute(
            'tag_filter_src_keys',
            default=[]
        )

    def _set_tag_filter_hidden_(self, boolean):
        self.set_gui_attribute('tag_filter_hidden', boolean)

    def get_is_tag_filter_hidden(self):
        return self.get_gui_attribute('tag_filter_hidden') or False

    # keyword-filter
    def set_keyword_filter_enable(self, boolean):
        self.set_gui_attribute('keyword_filter_enable', boolean)

    def get_keyword_filter_enable(self):
        return self.get_gui_attribute('keyword_filter_enable', default=False)

    def _set_keyword_filter_hidden_(self, boolean):
        self.set_gui_attribute('keyword_filter_hidden', boolean)

    def get_is_keyword_filter_hidden(self):
        return self.get_gui_attribute('keyword_filter_hidden') or False

    def get_has_visible_children(self):
        return gui_qt_core.GuiQtTreeWidget._get_item_has_visible_children_(
            self._qt_widget.treeWidget(),
            self._qt_widget
        )

    def set_visible_by_has_visible_children(self):
        self.set_visible(
            self.get_has_visible_children()
        )

    def _get_all_branch_items_(self):
        def _rcs_fnc(item_proxy_):
            lis.append(item_proxy_)
            _parent = item_proxy_.get_parent()
            if _parent is not None:
                _rcs_fnc(_parent)

        lis = []
        _rcs_fnc(self)
        return lis

    def set_foregrounds_raw(self, raw, column=0):
        _ = self._qt_widget.data(column, gui_qt_core.QtCore.Qt.UserRole)
        if isinstance(_, dict):
            user_data = _
        else:
            user_data = {}
        #
        user_data['foregrounds'] = raw
        self._qt_widget.setData(column, gui_qt_core.QtCore.Qt.UserRole, user_data)

    def set_states_raw(self, raw, column=0):
        _ = self._qt_widget.data(column, gui_qt_core.QtCore.Qt.UserRole)
        if isinstance(_, dict):
            user_data = _
        else:
            user_data = {}
        user_data['states'] = raw
        self._qt_widget.setData(
            column,
            gui_qt_core.QtCore.Qt.UserRole,
            user_data
        )

    def set_status(self, status, column=0):
        self._qt_widget._set_status_(status, column)

    def get_status(self, column=0):
        return self._qt_widget._get_status_(column)

    def get_view(self):
        qt_tree_view = self._qt_widget.treeWidget()
        return qt_tree_view.gui_proxy

    def _set_filter_keyword_(self, keyword, column=0):
        _ = self._qt_widget.data(column, gui_qt_core.QtCore.Qt.UserRole)
        if isinstance(_, dict):
            user_data = _
        else:
            user_data = {}
        #
        user_data['filter_keyword'] = keyword
        self._qt_widget.setData(
            column, gui_qt_core.QtCore.Qt.UserRole,
            user_data
        )

    def set_visible_connect_to(self, key, prx_item_tgt):
        self.set_visible_src_key(key)
        self.set_visible_tgt_view(prx_item_tgt.get_view())
        prx_item_tgt.set_visible_tgt_key(key)
        prx_item_tgt.set_hidden(self.get_is_hidden())

    def set_visible_connection_clear(self):
        pass

    def set_visible_tgt_view(self, view_prx):
        self.set_gui_attribute(
            'visible_tgt_view',
            view_prx
        )

    def get_visible_tgt_view(self):
        return self.get_gui_attribute('visible_tgt_view')

    def set_visible_connection_refresh(self):
        src_item_prx = self
        src_key = src_item_prx.get_visible_src_key()
        if src_key is not None:
            tgt_view_prx = src_item_prx.get_visible_tgt_view()
            if tgt_view_prx is not None:
                tgt_raw = tgt_view_prx.get_visible_tgt_raw()
                if tgt_raw is not None:
                    if src_key in tgt_raw:
                        tgt_item_prxes = tgt_raw[src_key]
                        for i_prx_item_tgt in tgt_item_prxes:
                            i_prx_item_tgt.set_hidden(self.get_is_hidden())
                            i_prx_item_tgt.widget._get_item_()._set_item_show_start_auto_()

    def start_loading(self):
        self._qt_widget._set_item_dag_loading_start_()

    def set_loading_end(self):
        # if self._loading_item_prx is not None:
        #     view = self.get_view()
        #     self._qt_widget.takeChild(
        #         self._qt_widget.indexOfChild(self._loading_item_prx.widget)
        #     )
        #     self._loading_item_prx = None
        #     view.set_loading_item_remove(self._loading_item_prx)

        self._qt_widget._set_item_dag_loading_end_()

    def set_show_build_fnc(self, method):
        self._qt_widget._set_item_show_build_fnc_(method)

    def connect_press_db_clicked_to(self, fnc):
        self._qt_widget._signals.press_db_clicked.connect(fnc)

    def set_drag_enable(self, boolean):
        self._qt_widget._set_drag_enable_(boolean)

    def set_drag_urls(self, urls):
        self._qt_widget._set_drag_urls_(urls)

    def set_drag_data(self, data):
        self._qt_widget._set_drag_data_(data)

    def get_drag_data(self):
        return self._qt_widget._get_drag_data_()

    def get_drag_mime_data(self):
        return self._qt_widget._get_drag_mime_data_()

    def connect_drag_pressed_to(self, fnc):
        self._qt_widget.drag_pressed.connect(fnc)

    def connect_drag_released_to(self, fnc):
        self._qt_widget.drag_released.connect(fnc)

    def set_show_fnc(self, cache_fnc, show_fnc):
        self._qt_widget._set_item_show_fnc_(cache_fnc, show_fnc)

    def __str__(self):
        return '{}(names={})'.format(
            self.__class__.__name__,
            ', '.join(map(lambda x: '"{}"'.format(x), self.get_names()))
        )

    def __repr__(self):
        return self.__str__()


class PrxLabelTreeItem(PrxTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxLabelTreeItem, self).__init__(*args, **kwargs)
        self.set_normal_state()

    def set_normal_state(self):
        self.set_icon_by_file(gui_core.GuiIcon.get('tag'))
        self.set_foreground_update(gui_qt_core.QtBrushes.Text)

    def set_error_state(self):
        self.set_icon_by_file(gui_core.GuiIcon.get('error'))
        self.set_foreground_update(gui_qt_core.QtBrushes.TextError)

    def set_warning_state(self):
        self.set_icon_by_file(gui_core.GuiIcon.get('warning'))
        self.set_foreground_update(gui_qt_core.QtBrushes.TextWarning)

    def set_adopt_state(self):
        self.set_icon_by_file(gui_core.GuiIcon.get('adopt'))
        self.set_foreground_update(gui_qt_core.QtBrushes.TextCorrect)

    def set_disable_state(self):
        self.set_icon_by_file(gui_core.GuiIcon.get('disable'))
        self.set_foreground_update(gui_qt_core.QtBrushes.TextDisable)

    def set_temporary_state(self):
        self.set_icon_by_file(gui_core.GuiIcon.get('temporary'))
        self.set_foreground_update(gui_qt_core.QtBrushes.TextTemporary)

    def set_foreground_update(self, qt_brush):
        qt_tree_widget = self._qt_widget.treeWidget()
        if qt_tree_widget is not None:
            for column in range(qt_tree_widget.columnCount()):
                self._qt_widget.setForeground(column, qt_brush)
        else:
            self._qt_widget.setForeground(0, qt_brush)


class PrxLoadingTreeItem(PrxTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxLoadingTreeItem, self).__init__(*args, **kwargs)
        self.set_name('loading ...')
        self.set_icon_by_file(gui_core.GuiIcon.get('refresh'))


class PrxObjTreeItem(PrxTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxObjTreeItem, self).__init__(*args, **kwargs)
        self._qt_widget.setForeground(0, gui_qt_core.QtBrushes.Text)
        # self.set_icon_by_file(gui_core.GuiIcon.get('tag'))
        self.set_normal_state()

    @property
    def check_state(self):
        return PrxTreeItemCheckState(self)

    def set_temporary_state(self, column=0):
        self._qt_widget.setForeground(column, gui_qt_core.QtBrushes.TextDisable)
        self.set_gui_attribute(
            'state', 'temporary'
        )

    def set_normal_state(self, column=0):
        self._qt_widget.setForeground(column, gui_qt_core.QtBrushes.Text)
        self.set_gui_attribute(
            'state', 'normal'
        )

    def set_error_state(self, column=0):
        self._qt_widget.setForeground(column, gui_qt_core.QtBrushes.TextError)
        self.set_gui_attribute(
            'state', 'error'
        )

    def set_warning_state(self, column=0):
        self._qt_widget.setForeground(column, gui_qt_core.QtBrushes.TextWarning)
        self.set_gui_attribute(
            'state', 'warning'
        )

    def set_adopt_state(self, column=0):
        self._qt_widget.setForeground(column, gui_qt_core.QtBrushes.TextCorrect)
        self.set_gui_attribute(
            'state', 'adopt'
        )

    def set_current_state(self, column=0):
        self._qt_widget.setForeground(column, gui_qt_core.QtBrushes.TextActive)
        self.set_gui_attribute(
            'state', 'current'
        )


class PrxDccObjTreeItem(PrxObjTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxDccObjTreeItem, self).__init__(*args, **kwargs)


class PrxStgObjTreeItem(PrxObjTreeItem):
    def __init__(self, *args, **kwargs):
        super(PrxStgObjTreeItem, self).__init__(*args, **kwargs)


class PrxListItemWidget(
    gui_prx_abstracts.AbsPrxWidget,
    gui_prx_abstracts.AbsPrxMenuDef,
    #
    gui_prx_abstracts.AbsPrxItemFilterTgtDef,
    gui_prx_abstracts.AbsPrxItemVisibleConnectionDef
):
    QT_WIDGET_CLS = gui_qt_wgt_item_for_list.QtListItemWidget

    def __init__(self, *args, **kwargs):
        super(PrxListItemWidget, self).__init__(*args, **kwargs)
        self._visible_tgt_key = None

    def get_item(self):
        return self._qt_widget._get_item_()

    item = property(get_item)

    def set_gui_menu_raw(self, raw):
        self._qt_widget._set_menu_data_(raw)

    def set_index(self, index):
        self._qt_widget._set_index_(index)

    def set_icons_by_pixmap(self, icons):
        self._qt_widget._set_icon_pixmaps_(icons)

    def set_index_draw_enable(self, boolean):
        self._qt_widget._set_index_draw_enable_(boolean)

    def set_icon_by_file(self, name=None, file_path=None):
        if name is not None:
            self._qt_widget._set_icon_name_text_(
                gui_core.GuiIcon.get(name)
            )
        elif file_path is not None:
            self._qt_widget._set_icon_file_path_(
                file_path
            )

    def set_icon_sub_by_file(self, name=None, file_path=None):
        if name is not None:
            self._qt_widget._set_icon_sub_file_path_(
                gui_core.GuiIcon.get(name)
            )
        elif file_path is not None:
            self._qt_widget._set_icon_sub_file_path_(
                file_path
            )

    def set_file_icons(self, icon_names=None, icon_file_paths=None):
        if isinstance(icon_names, (tuple, list)):
            self._qt_widget._set_icon_file_paths_(
                [gui_core.GuiIcon.get(i) for i in icon_names]
            )
        elif isinstance(icon_file_paths, (tuple, list)):
            self._qt_widget._set_icon_file_paths_(icon_file_paths)

    def set_file_icon_add(self, icon_name):
        self._qt_widget._set_icon_file_path_add_(
            gui_core.GuiIcon.get(icon_name)
        )

    def set_icon_by_name(self, text):
        self._qt_widget._set_icon_name_text_(
            text
        )

    def set_icon_frame_size(self, w, h):
        self._qt_widget._set_icon_frame_draw_size_(w, h)

    def set_icon_size(self, w, h):
        self._qt_widget._set_icon_size_(w, h)

    def set_sort_name_key(self, text):
        self._qt_widget._set_sort_name_key_(text)

    # name
    def set_name(self, text):
        self._qt_widget._set_name_text_(text)
        self._qt_widget._get_item_()._set_name_text_(text)

    def set_names(self, texts):
        self._qt_widget._set_name_texts_(texts)
        self._qt_widget._get_item_()._set_name_texts_(texts)

    def set_name_dict(self, name_dict):
        self._qt_widget._set_name_text_dict_(name_dict)

    def get_name_dict(self):
        return self._qt_widget._get_name_text_dict_()

    def get_names(self):
        return self._qt_widget._get_name_texts_()

    def set_name_align_center_top(self):
        self._qt_widget._set_name_text_option_to_align_center_top_()

    def set_name_frame_border_color(self, color):
        return self._qt_widget._set_name_frame_border_color_(color)

    def set_name_frame_background_color(self, color):
        return self._qt_widget._set_name_frame_background_color_(color)

    def set_image(self, file_path):
        self._qt_widget._set_image_file_path_(file_path)

    def get_image(self):
        return self._qt_widget._get_image_file_path_()

    def set_movie_enable(self, boolean):
        self._qt_widget._set_play_draw_enable_(boolean)

    def set_image_by_name(self, text):
        self._qt_widget._set_image_text_(text)

    def set_image_by_file(self, file_path):
        self._qt_widget._set_image_file_path_(file_path)

    def set_image_sub_by_file(self, file_path):
        self._qt_widget._set_image_sub_file_path_(file_path)

    def set_image_size(self, size):
        pass

    def set_image_show_sub_process(self, sub_process):
        pass

    def set_image_show_args(self, image, cmd):
        self._qt_widget._get_item_()._set_item_show_image_cmd_(image, cmd)

    def set_visible_tgt_key(self, key):
        self.set_gui_attribute(
            'visible_tgt_key',
            key
        )

    def get_visible_tgt_key(self):
        return self.get_gui_attribute('visible_tgt_key')

    def get_view(self):
        return self.get_gui_attribute(
            'view_prx'
        )

    def set_view(self, view_prx):
        self.set_gui_attribute(
            'view_prx',
            view_prx
        )

    def set_hidden(self, boolean=True):
        self._qt_widget.setHidden(boolean)
        self._qt_widget._get_item_().setHidden(boolean)

    def set_tool_tip(self, text):
        self._qt_widget._set_tool_tip_(text)

    def set_border_color(self, color):
        self._qt_widget._set_border_color_(color)

    def set_show_build_fnc(self, method):
        self._qt_widget._get_item_()._set_item_show_build_fnc_(method)

    def set_show_fnc(self, cache_fnc, show_fnc):
        self._qt_widget._get_item_()._set_item_show_fnc_(cache_fnc, show_fnc)

    def set_image_loading_start(self):
        self._qt_widget._get_item_()._checkout_item_show_image_loading_()

    def connect_press_clicked_to(self, fnc):
        self._qt_widget.press_clicked.connect(fnc)

    def connect_press_db_clicked_to(self, fnc):
        self._qt_widget.press_db_clicked.connect(fnc)

    def set_press_db_clicked_method_add_(self, fnc):
        self._qt_widget._set_action_press_db_clicked_method_add_(fnc)

    def set_check_enable(self, boolean):
        self._qt_widget._set_check_enable_(boolean)
        self._qt_widget._set_check_action_enable_(True)

    def set_drag_enable(self, boolean):
        self._qt_widget._set_drag_enable_(boolean)

    def set_drag_urls(self, urls):
        self._qt_widget._set_drag_urls_(urls)

    def set_drag_data(self, data):
        self._qt_widget._set_drag_data_(data)

    def get_drag_data(self):
        return self._qt_widget._get_drag_data_()

    def get_drag_mime_data(self):
        return self._qt_widget._get_drag_mime_data_()

    def connect_drag_pressed_to(self, fnc):
        self._qt_widget.drag_pressed.connect(fnc)

    def connect_drag_released_to(self, fnc):
        self._qt_widget.drag_released.connect(fnc)

    def set_status(self, status):
        self._qt_widget._set_status_(status)

    def get_is_checked(self):
        return self._qt_widget._get_is_checked_()

    def get_is_visible(self):
        return self.get_item()._get_is_visible_()

    def set_visible(self, boolean, **kwargs):
        self.get_item()._set_visible_(boolean)

    def set_force_hidden(self, boolean):
        self.get_item()._set_force_hidden_(boolean)

    def refresh_widget_force(self):
        self._qt_widget._refresh_widget_force_()

    def __str__(self):
        return '{}(names={})'.format(
            self.__class__.__name__,
            ', '.join(map(lambda x: '"{}"'.format(x), self.get_names()))
        )

    def __repr__(self):
        return self.__str__()


class PrxMediaItem(object):
    pass


class PrxGuideBar(
    gui_prx_abstracts.AbsPrxWidget,
):
    QT_WIDGET_CLS = gui_qt_wgt_input_for_guide.QtInputAsGuide

    def __init__(self, *args, **kwargs):
        super(PrxGuideBar, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self._qt_widget._guide_entry._set_name_text_(text)

    def set_path(self, path):
        self._qt_widget._guide_entry._set_guide_path_text_(path)

    def set_types(self, texts):
        self._qt_widget._guide_entry._set_guide_type_texts_(texts)

    def set_dict(self, dict_):
        self._qt_widget._guide_entry._set_guide_dict_(dict_)

    def connect_user_text_choose_accepted_to(self, fnc):
        self._qt_widget._guide_entry.guide_text_choose_accepted.connect(fnc)

    def connect_user_text_press_accepted_to(self, fnc):
        self._qt_widget._guide_entry.guide_text_press_accepted.connect(fnc)

    def set_clear(self):
        pass


class PrxTagBar(
    gui_prx_abstracts.AbsPrxWidget,
):
    QT_WIDGET_CLS = gui_qt_wgt_input_for_guide.QtInputAsGuide

    def __init__(self, *args, **kwargs):
        super(PrxTagBar, self).__init__(*args, **kwargs)
