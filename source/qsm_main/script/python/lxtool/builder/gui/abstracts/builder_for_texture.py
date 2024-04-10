# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.texture as bsc_texture
# gui
import lxgui.core as gui_core

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as prx_widgets


class _GuiTextureOpt(gui_prx_abstracts.AbsGuiPrxTreeViewOpt):
    DCC_NAMESPACE = 'texture'
    DCC_GROUP_NAMESPACE = 'texture_type'

    def __init__(self, window, session, prx_tree_view):
        self._window = window
        self._session = session
        self._init_tree_view_opt_(prx_tree_view, self.DCC_NAMESPACE)

    def gui_add_root(self):
        path = '/'
        if self.gui_get_is_exists(path) is False:
            prx_item = self._prx_tree_view.create_item(
                self.ROOT_NAME,
                icon=gui_core.GuiIcon.get('database/all'),
            )

            self.gui_register(path, prx_item)

            prx_item.set_expanded(True)
            prx_item.set_checked(True)
            return True, prx_item
        return False, self.gui_get(path)

    def gui_add_group(self, path):
        if self.gui_get_is_exists(path) is False:
            path_opt = bsc_core.PthNodeOpt(path)
            parent_gui = self.gui_get(path_opt.get_parent_path())
            gui_name = bsc_core.RawStrUnderlineOpt(path_opt.get_name()).to_prettify()
            prx_item = parent_gui.add_child(
                gui_name,
                icon=gui_core.GuiIcon.get('database/group'),
            )

            self.gui_register(path, prx_item)
            prx_item.set_gui_dcc_obj(
                path_opt, self.DCC_GROUP_NAMESPACE
            )

            prx_item.set_tool_tip(path)

            prx_item.set_expanded(True)
            prx_item.set_checked(True)
            return prx_item
        return self.gui_get(path)

    def gui_add_one(self, path, file_opt):
        if self.gui_get_is_exists(path) is False:
            path_opt = bsc_core.PthNodeOpt(path)
            parent_gui = self.gui_get(path_opt.get_parent_path())
            prx_item = parent_gui.add_child(
                path_opt.get_name(),
                icon=gui_core.GuiIcon.get('database/object'),
            )

            self.gui_register(path, prx_item)
            prx_item.set_gui_dcc_obj(
                file_opt, self.DCC_NAMESPACE
            )

            prx_item.set_tool_tip(file_opt.get_path())

            prx_item.set_checked(True)
            return prx_item
        return self.gui_get(path)

    def get_texture_assign(self):
        dict_ = {}
        for i_k, i_v in self._item_dict.items():
            i_obj = i_v.get_gui_dcc_obj(self.DCC_GROUP_NAMESPACE)
            if i_obj is not None:
                i_texture_type = i_obj.get_name()
                i_items_checked = [i for i in i_v.get_children() if i.get_is_checked()]
                if i_items_checked:
                    i_item = i_items_checked[0]
                    i_file_opt = i_item.get_gui_dcc_obj(self.DCC_NAMESPACE)
                    dict_[i_texture_type] = i_file_opt.get_path()
        return dict_


class AbsPnlBuilderForTexture(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlBuilderForTexture, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self._texture_name = None

    def set_all_setup(self):
        sa_1 = prx_widgets.PrxVScrollArea()
        self.add_widget(sa_1)

        self._options_prx_node = prx_widgets.PrxNode('options')
        sa_1.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.main_options'),
        )

        self.__tip = prx_widgets.PrxTextBrowser()
        sa_1.add_widget(self.__tip)
        self.__tip.set_focus_enable(False)

        self.__tip.set_content(
            self._session.configure.get('build.node.main_content')
        )

        self.__next_button = prx_widgets.PrxPressItem()
        self.__next_button.set_name('next')
        self.add_button(self.__next_button)
        self.__next_button.connect_press_clicked_to(self.__do_next)
        self.__next_button.set_enable(False)

        self._options_prx_node.get_port('file').connect_input_changed_to(
            self.__gui_refresh_next_button
        )

        self.__gui_build_create_layer()

    def __gui_build_create_layer(self):
        layer_widget = self.create_layer_widget('create_layer', 'Create')
        s = prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(s)

        self._prx_tree_view = prx_widgets.PrxTreeView()
        s.add_widget(self._prx_tree_view)

        self._prx_tree_view.set_header_view_create(
            [('name', 4)],
            self.get_definition_window_size()[0]-32
        )

        self._gui_texture_opt = _GuiTextureOpt(
            self, self._session, self._prx_tree_view
        )

        tool_bar = prx_widgets.PrxHToolBar()
        layer_widget.add_widget(tool_bar.widget)
        tool_bar.set_expanded(True)
        button = prx_widgets.PrxPressItem()
        tool_bar.add_widget(button)
        button.set_name('Apply')
        button.connect_press_clicked_to(
            self.__create_layer_apply_fnc
        )

    def __create_layer_apply_fnc(self):
        texture_assign = self._gui_texture_opt.get_texture_assign()
        if texture_assign:
            texture_name = self._texture_name
            node_path = self._options_prx_node.get('node')
            if bsc_core.SysApplicationMtd.get_is_katana():
                import lxkatana.scripts as ktn_scripts

                ktn_scripts.ScpTextureBuildForCreate(
                    node_path, texture_name, texture_assign
                ).accept()

        self.close_window_later()

    def __gui_refresh_next_button(self):
        f = self._options_prx_node.get('file')
        if bsc_storage.StgPathMtd.get_is_file(f):
            self.__next_button.set_enable(True)
        else:
            self.__next_button.set_enable(False)

    def __do_next(self):
        self.switch_current_layer_to('create_layer')
        self.__gui_refresh_create()

    def __gui_refresh_create(self):
        f = self._options_prx_node.get('file')
        self._gui_texture_opt.restore()
        self._gui_texture_opt.gui_add_root()
        if bsc_storage.StgPathMtd.get_is_file(f):
            m = bsc_texture.TxrMethodForBuild.generate_instance()
            texture_args = m.generate_all_texture_args(f)
            if texture_args:
                self._texture_name, texture_data = texture_args
                for i_type, i_file_paths in texture_data.items():
                    i_group_path = '/{}'.format(i_type)
                    self._gui_texture_opt.gui_add_group(i_group_path)
                    for j_file_path in i_file_paths:
                        j_file_opt = bsc_storage.StgFileOpt(j_file_path)
                        j_path = '{}/{}'.format(i_group_path, j_file_opt.get_name())
                        self._gui_texture_opt.gui_add_one(j_path, j_file_opt)

    def setup(self, node_path, file_path):
        def fnc_():
            self._options_prx_node.set(
                'node', node_path
            )
            self._options_prx_node.set(
                'file', file_path
            )
            self.__do_next()

        self.connect_window_loading_finished_to(fnc_)
