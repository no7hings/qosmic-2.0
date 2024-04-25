# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import qsm_general.scan as qsm_gnl_scan


class PrxInputForAsset(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    def __init__(self, *args, **kwargs):
        super(PrxInputForAsset, self).__init__(*args, **kwargs)

        self._qt_layout_0 = qt_widgets.QtHBoxLayout(self.get_widget())
        self._qt_layout_0.setContentsMargins(*[0]*4)
        # self._qt_layout_0._set_align_top_()
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

        self._qt_path_input._set_history_key_('gui.input-entity-path-asset')
        self._qt_path_input._pull_history_latest_()

        # self._qt_path_input.input_value_change_accepted.connect(self._update_fnc)
        # self._qt_path_input.user_input_entry_finished.connect(self._update_fnc_1)

        self._qt_path_input._run_fnc_use_thread_(self._cache_entities)

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
            assets = project.find_assets(dict(role=['chr', 'prp']))
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
        self._qt_path_input.input_value_change_accepted.connect(fnc)

    def _cache_entities(self):
        path = self._qt_path_input._get_value_()
        path_opt = bsc_core.PthNodeOpt(path)
        cs = path_opt.get_components()
        cs.reverse()

        for i in cs:
            i_d = i.get_depth()
            if i_d == 1:
                projects = self._scan_root.projects
            elif i_d == 2:
                project = self._scan_root.get_entity(i.get_path())
                assets = project.find_assets(dict(role=['chr', 'prp']))

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