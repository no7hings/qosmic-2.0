# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_shark.scan as lnx_srk_scan

import qsm_general.core as qsm_gnl_core


class PrxInputForAssetCharacterAndProp(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    HISTORY_KEY = 'gui.input-entity-path-asset'

    ROLE_MASK = qsm_gnl_core.QsmAsset.CHARACTER_AND_PROP_ROLE_MASK
    ROLE_MASK_NEW = qsm_gnl_core.QsmAsset.CHARACTER_AND_PROP_ROLE_MASK_NEW

    def __init__(self, *args, **kwargs):
        if 'history_key' in kwargs:
            history_key = kwargs.pop('history_key')
        else:
            history_key = None

        super(PrxInputForAssetCharacterAndProp, self).__init__(*args, **kwargs)
        
        self._scan_cache_flag = True

        self._qt_layout_0 = gui_qt_widgets.QtHBoxLayout(self.get_widget())
        self._qt_layout_0.setContentsMargins(*[0]*4)
        
        self._qt_reload_button = gui_qt_widgets.QtIconPressButton()
        self._qt_layout_0.addWidget(self._qt_reload_button)
        self._qt_reload_button._set_icon_name_('reload')
        if gui_core.GuiUtil.language_is_chs():
            self._qt_reload_button._set_name_text_('重载')
            self._qt_reload_button._set_tool_tip_(
                (
                    '点击重缓存中重载实体。\n'
                    '右键/点击小三角：\n'
                    '   从系统中重载：重新生成实体缓存。'
                )
            )
        else:
            self._qt_reload_button._set_name_text_('Reload')
            self._qt_reload_button._set_tool_tip_(
                (
                    'Click on Reload Entity from Cache. \n'
                    'Right click/click on the small triangle: \n'
                    'Reload from System: Regenerate the entity cache.'
                )
            )

        self._qt_path_input = gui_qt_widgets.QtInputForPath()
        self._qt_layout_0.addWidget(self._qt_path_input)

        self._scan_root = lnx_srk_scan.Stage().root()

        self._qt_path_input._set_next_buffer_fnc_(self._next_buffer_fnc)

        self._qt_path_input._set_value_('/')
        self._qt_path_input._set_choose_popup_auto_resize_enable_(False)
        self._qt_path_input._set_choose_popup_tag_filter_enable_(True)
        self._qt_path_input._set_choose_popup_keyword_filter_enable_(True)

        self._qt_path_input._set_choose_popup_item_size_(40, 40)

        self._qt_path_input._setup_()

        if history_key is None:
            history_key = self.HISTORY_KEY

        self._qt_path_input._set_history_key_(history_key)
        self._qt_path_input._pull_history_latest_()
        self._qt_path_input.user_history_pull_accepted.connect(self._pull_history_fnc)

        self._qt_reload_button.press_clicked.connect(self._on_reload_entities)

        if gui_core.GuiUtil.language_is_chs():
            self._qt_reload_button._set_menu_data_(
                [
                    ('从系统中重载', 'reload-force', self._on_resync_entities)
                ]
            )
        else:
            self._qt_reload_button._set_menu_data_(
                [
                    ('Reload form system', 'reload-force', self._on_resync_entities)
                ]
            )

        self._cache_entities()

    def _cache_projects(self):
        name_texts = []
        keyword_filter_dict = collections.OrderedDict()
        tag_filter_dict = collections.OrderedDict()
        for i_project in self._scan_root.find_projects(cache_flag=self._scan_cache_flag):
            i_name = i_project.name
            name_texts.append(i_project.name)

            keyword_filter_dict[i_name] = [i_name]
            tag_filter_dict[i_name] = ['All']

        return dict(
            type_text='project',
            name_texts=name_texts,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

    def _cache_assets(self, path_opt):
        name_texts = []
        keyword_filter_dict = collections.OrderedDict()
        tag_filter_dict = collections.OrderedDict()

        project = self._scan_root.get_entity(path_opt.to_string())
        if project is not None:
            if qsm_gnl_core.scheme_is_release():
                role_mask = self.ROLE_MASK_NEW
            else:
                role_mask = self.ROLE_MASK

            assets = project.assets(role=role_mask, cache_flag=self._scan_cache_flag)
            for i_asset in assets:
                i_name = i_asset.name
                name_texts.append(i_asset.name)

                keyword_filter_dict[i_name] = [i_name]
                tag_filter_dict[i_name] = ['All', i_asset.properties.role]

        return dict(
            type_text='asset',
            name_texts=name_texts,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

    def _on_reload_entities(self):
        def post_fnc_():
            self._scan_cache_flag = True

        path_text = self._qt_path_input._get_value_()
        self._scan_cache_flag = False
        self._qt_path_input._update_next_data_for_(path_text, post_fnc_)

    def _on_resync_entities(self):
        def post_fnc_():
            self._scan_cache_flag = True
            lnx_srk_scan.Stage.set_sync_cache_flag(True)

        def fnc_():
            self._scan_cache_flag = False
            lnx_srk_scan.Stage.set_sync_cache_flag(False)
            self._qt_path_input._update_next_data_for_(path_text, post_fnc_)

        path_text = self._qt_path_input._get_value_()

        if gui_core.GuiUtil.language_is_chs():
            result = gui_core.GuiApplication.exec_message_dialog(
                '从“{}”重载实体，这个过程可能会花费1-2分钟甚至更长，点击“Ok”以继续。'.format(path_text)
            )
        else:
            result = gui_core.GuiApplication.exec_message_dialog(
                (
                    'Reload entities from "{}", '
                    'This process may take 1-2 minutes or even longer. Click "Ok" to continue.'
                ).format(path_text)
            )

        if result is True:
            fnc_()

    def _pull_history_fnc(self, path):
        self._next_buffer_fnc(
            bsc_core.BscNodePathOpt(path)
        )

    def _next_buffer_fnc(self, path_opt):
        cs = path_opt.get_components()
        cs.reverse()
        d = len(cs)
        if d == 1:
            return self._cache_projects()
        elif d == 2:
            return self._cache_assets(path_opt)
        return dict()

    def connect_input_change_accepted_to(self, fnc):
        self._qt_path_input.input_value_accepted.connect(fnc)

    def _cache_entities(self):
        path = self._qt_path_input._get_value_()
        path_opt = bsc_core.BscNodePathOpt(path)
        cs = path_opt.get_components()
        cs.reverse()

        for i in cs:
            i_d = i.get_depth()
            if i_d == 1:
                self._cache_projects()
            elif i_d == 2:
                self._cache_assets(i)

    def do_update(self):
        self._cache_entities()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def add_button(self, name):
        button = gui_qt_widgets.QtPressButton()
        self._qt_layout_0.addWidget(button)
        button._set_name_text_(name)
        button.setMaximumWidth(64)
        button.setMinimumWidth(64)
        return button

    def get_entity(self, path):
        return self._scan_root.get_entity(path)

    def get_path(self):
        return self._qt_path_input._get_value_()

    def set_path(self, path):
        self._qt_path_input._set_value_(path)
        # cache when path is applied
        self._cache_entities()


class PrxInputForAssetScenery(PrxInputForAssetCharacterAndProp):
    HISTORY_KEY = 'gui.input-entity-path-assembly'

    ROLE_MASK = qsm_gnl_core.QsmAsset.SCENERY_ROLE_MASK
    ROLE_MASK_NEW = qsm_gnl_core.QsmAsset.SCENERY_ROLE_MASK_NEW

    def __init__(self, *args, **kwargs):
        super(PrxInputForAssetScenery, self).__init__(*args, **kwargs)


class PrxInputForAsset(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    HISTORY_KEY = 'gui.input-entity-path-asset_new'

    ROLE_MASK = qsm_gnl_core.QsmAsset.CHARACTER_AND_PROP_ROLE_MASK
    ROLE_MASK_NEW = qsm_gnl_core.QsmAsset.CHARACTER_AND_PROP_ROLE_MASK_NEW

    def __init__(self, *args, **kwargs):
        if 'history_key' in kwargs:
            history_key = kwargs.pop('history_key')
        else:
            history_key = None

        super(PrxInputForAsset, self).__init__(*args, **kwargs)

        self._scan_cache_flag = True

        self._qt_layout_0 = gui_qt_widgets.QtHBoxLayout(self.get_widget())
        self._qt_layout_0.setContentsMargins(*[0]*4)

        self._qt_reload_button = gui_qt_widgets.QtIconPressButton()
        self._qt_layout_0.addWidget(self._qt_reload_button)
        self._qt_reload_button._set_icon_name_('reload')
        if gui_core.GuiUtil.language_is_chs():
            self._qt_reload_button._set_name_text_('重载')
            self._qt_reload_button._set_tool_tip_(
                (
                    '点击重缓存中重载实体。\n'
                    '右键/点击小三角：\n'
                    '   从系统中重载：重新生成实体缓存。'
                )
            )
        else:
            self._qt_reload_button._set_name_text_('Reload')
            self._qt_reload_button._set_tool_tip_(
                (
                    'Click on Reload Entity from Cache. \n'
                    'Right click/click on the small triangle: \n'
                    'Reload from System: Regenerate the entity cache.'
                )
            )

        self._qt_path_input = gui_qt_widgets.QtInputForPath()
        self._qt_layout_0.addWidget(self._qt_path_input)

        self._scan_root = lnx_srk_scan.Stage().root()

        self._qt_path_input._set_next_buffer_fnc_(self._next_buffer_fnc)

        self._qt_path_input._set_value_('/')
        self._qt_path_input._set_choose_popup_auto_resize_enable_(False)
        self._qt_path_input._set_choose_popup_tag_filter_enable_(True)
        self._qt_path_input._set_choose_popup_keyword_filter_enable_(True)

        self._qt_path_input._set_choose_popup_item_size_(40, 40)

        self._qt_path_input._setup_()

        if history_key is None:
            history_key = self.HISTORY_KEY

        self._qt_path_input._set_history_key_(history_key)
        self._qt_path_input._pull_history_latest_()
        self._qt_path_input.user_history_pull_accepted.connect(self._pull_history_fnc)

        self._qt_reload_button.press_clicked.connect(self._on_reload_entities)

        if gui_core.GuiUtil.language_is_chs():
            self._qt_reload_button._set_menu_data_(
                [
                    ('从系统中重载', 'reload-force', self._on_resync_entities)
                ]
            )
        else:
            self._qt_reload_button._set_menu_data_(
                [
                    ('Reload form system', 'reload-force', self._on_resync_entities)
                ]
            )

        self._cache_entities()

    def _cache_projects(self):
        name_texts = []
        keyword_filter_dict = collections.OrderedDict()
        tag_filter_dict = collections.OrderedDict()
        for i_project in self._scan_root.find_projects(cache_flag=self._scan_cache_flag):
            i_name = i_project.name
            name_texts.append(i_project.name)

            keyword_filter_dict[i_name] = [i_name]
            tag_filter_dict[i_name] = ['All']

        return dict(
            type_text='project',
            name_texts=name_texts,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

    def _cache_roles(self, path_opt):
        pass

    def _cache_assets(self, path_opt):
        name_texts = []
        keyword_filter_dict = collections.OrderedDict()
        tag_filter_dict = collections.OrderedDict()

        project = self._scan_root.get_entity(path_opt.to_string())
        if project is not None:
            if qsm_gnl_core.scheme_is_release():
                role_mask = self.ROLE_MASK_NEW
            else:
                role_mask = self.ROLE_MASK

            assets = project.assets(role=role_mask, cache_flag=self._scan_cache_flag)
            for i_asset in assets:
                i_name = i_asset.name
                name_texts.append(i_asset.name)

                keyword_filter_dict[i_name] = [i_name]
                tag_filter_dict[i_name] = ['All', i_asset.properties.role]

        return dict(
            type_text='asset',
            name_texts=name_texts,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

    def _on_reload_entities(self):
        def post_fnc_():
            self._scan_cache_flag = True

        path_text = self._qt_path_input._get_value_()
        self._scan_cache_flag = False
        self._qt_path_input._update_next_data_for_(path_text, post_fnc_)

    def _on_resync_entities(self):
        def post_fnc_():
            self._scan_cache_flag = True
            lnx_srk_scan.Stage.set_sync_cache_flag(True)

        def fnc_():
            self._scan_cache_flag = False
            lnx_srk_scan.Stage.set_sync_cache_flag(False)
            self._qt_path_input._update_next_data_for_(path_text, post_fnc_)

        path_text = self._qt_path_input._get_value_()

        if gui_core.GuiUtil.language_is_chs():
            result = gui_core.GuiApplication.exec_message_dialog(
                '从“{}”重载实体，这个过程可能会花费1-2分钟甚至更长，点击“Ok”以继续。'.format(path_text)
            )
        else:
            result = gui_core.GuiApplication.exec_message_dialog(
                (
                    'Reload entities from "{}", '
                    'This process may take 1-2 minutes or even longer. Click "Ok" to continue.'
                ).format(path_text)
            )

        if result is True:
            fnc_()

    def _pull_history_fnc(self, path):
        self._next_buffer_fnc(
            bsc_core.BscNodePathOpt(path)
        )

    def _next_buffer_fnc(self, path_opt):
        cs = path_opt.get_components()
        cs.reverse()
        d = len(cs)
        if d == 1:
            return self._cache_projects()
        elif d == 2:
            return self._cache_assets(path_opt)
        return dict()

    def connect_input_change_accepted_to(self, fnc):
        self._qt_path_input.input_value_accepted.connect(fnc)

    def connect_input_finish_to(self, fnc):
        self._qt_path_input.user_input_entry_finished.connect(fnc)

    def _cache_entities(self):
        path = self._qt_path_input._get_value_()
        path_opt = bsc_core.BscNodePathOpt(path)
        cs = path_opt.get_components()
        cs.reverse()

        for i in cs:
            i_d = i.get_depth()
            if i_d == 1:
                self._cache_projects()
            elif i_d == 2:
                self._cache_assets(i)

    def do_update(self):
        self._cache_entities()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def add_button(self, name):
        button = gui_qt_widgets.QtPressButton()
        self._qt_layout_0.addWidget(button)
        button._set_name_text_(name)
        button.setMaximumWidth(64)
        button.setMinimumWidth(64)
        return button

    def get_entity(self, path):
        return self._scan_root.get_entity(path)

    def get_path(self):
        return self._qt_path_input._get_value_()

    def set_path(self, path):
        self._qt_path_input._set_value_(path)
        # cache when path is applied
        self._cache_entities()

    def set_focus_in(self):
        self._qt_path_input._set_input_entry_focus_in_()


class PrxWindowForAssetInput(gui_prx_widgets.PrxDialogWindow1):
    def __init__(self, *args, **kwargs):
        super(PrxWindowForAssetInput, self).__init__(*args, **kwargs)
        self.set_tip_visible(False)
        self._asset_prx_input = PrxInputForAsset(history_key='lazy.input.asset-path')
        self.add_customize_widget(self._asset_prx_input)
        self._asset_prx_input.set_focus_in()

        self._asset_prx_input.connect_input_finish_to(self._accept_fnc)

    def _accept_fnc(self):
        self._result = True
        self.close_window()

    def get_entity(self):
        return self._asset_prx_input.get_entity(
            self._asset_prx_input.get_path()
        )
