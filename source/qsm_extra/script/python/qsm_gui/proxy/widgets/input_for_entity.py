# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import qsm_general.scan as qsm_gnl_scan

import qsm_general.core as qsm_gnl_core


class PrxAssetInputForCharacterAndProp(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    HISTORY_KEY = 'gui.input-entity-path-asset'

    ROLE_MASK = qsm_gnl_core.QsmAsset.CHARACTER_AND_PROP_ROLE_MASK
    ROLE_MASK_NEW = qsm_gnl_core.QsmAsset.CHARACTER_AND_PROP_ROLE_MASK_NEW

    def __init__(self, *args, **kwargs):
        super(PrxAssetInputForCharacterAndProp, self).__init__(*args, **kwargs)

        self._qt_layout_0 = qt_widgets.QtHBoxLayout(self.get_widget())
        self._qt_layout_0.setContentsMargins(*[0]*4)
        # self._qt_layout_0._set_align_as_top_()
        self._qt_path_input = qt_widgets.QtInputAsPath()
        self._qt_layout_0.addWidget(self._qt_path_input)

        self._scan_root = qsm_gnl_scan.Root.generate()

        self._qt_path_input._set_buffer_fnc_(
            self._buffer_fnc
        )

        self._qt_path_input._set_value_('/')
        self._qt_path_input._set_choose_popup_auto_resize_enable_(False)
        self._qt_path_input._set_choose_popup_tag_filter_enable_(True)
        self._qt_path_input._set_choose_popup_keyword_filter_enable_(True)

        self._qt_path_input._set_choose_popup_item_size_(40, 40)

        self._qt_path_input._setup_()

        self._qt_path_input._set_history_key_(self.HISTORY_KEY)
        self._qt_path_input._pull_history_latest_()
        self._qt_path_input.user_history_pull_accepted.connect(self._pull_history_fnc)

        self._cache_entities()

    def _cache_projects(self):
        name_texts = []
        keyword_filter_dict = collections.OrderedDict()
        tag_filter_dict = collections.OrderedDict()
        for i_project in self._scan_root.projects:
            i_name = i_project.name
            name_texts.append(i_project.name)

            keyword_filter_dict[i_name] = [i_name]
            tag_filter_dict[i_name] = ['All']

        return dict(
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

            assets = project.find_assets(dict(role=role_mask))
            for i_asset in assets:
                i_name = i_asset.name
                name_texts.append(i_asset.name)

                keyword_filter_dict[i_name] = [i_name]
                tag_filter_dict[i_name] = ['All', i_asset.properties.role]

        return dict(
            name_texts=name_texts,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

    def _pull_history_fnc(self, path):
        self._buffer_fnc(
            bsc_core.BscPathOpt(path)
        )

    def _buffer_fnc(self, path_opt):
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
        path_opt = bsc_core.BscPathOpt(path)
        cs = path_opt.get_components()
        cs.reverse()

        for i in cs:
            i_d = i.get_depth()
            if i_d == 1:
                _projects = self._scan_root.projects
            elif i_d == 2:
                if qsm_gnl_core.scheme_is_release():
                    role_mask = self.ROLE_MASK_NEW
                else:
                    role_mask = self.ROLE_MASK

                project = self._scan_root.get_entity(i.get_path())
                _assets = project.find_assets(dict(role=role_mask))

    def do_update(self):
        self._cache_entities()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def add_button(self, name):
        button = qt_widgets.QtPressButton()
        self._qt_layout_0.addWidget(button)
        button._set_name_text_(name)
        button.setMaximumWidth(64)
        button.setMinimumWidth(64)
        return button

    def get_entity(self, path):
        return self._scan_root.get_entity(path)

    def get_path(self):
        return self._qt_path_input._get_value_()


class PrxAssetInputForScenery(PrxAssetInputForCharacterAndProp):
    HISTORY_KEY = 'gui.input-entity-path-assembly'

    ROLE_MASK = qsm_gnl_core.QsmAsset.SCENERY_ROLE_MASK
    ROLE_MASK_NEW = qsm_gnl_core.QsmAsset.SCENERY_ROLE_MASK_NEW

    def __init__(self, *args, **kwargs):
        super(PrxAssetInputForScenery, self).__init__(*args, **kwargs)
