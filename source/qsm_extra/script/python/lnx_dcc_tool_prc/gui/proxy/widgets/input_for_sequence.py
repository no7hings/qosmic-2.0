# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import lnx_parsor.swap as lnx_prs_swap


class PrxInputForSequence(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    HISTORY_KEY = 'gui.input-entity-path-sequence'

    def __init__(self, *args, **kwargs):
        if 'history_key' in kwargs:
            history_key = kwargs.pop('history_key')
        else:
            history_key = None

        super(PrxInputForSequence, self).__init__(*args, **kwargs)

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
                    '点击从缓存中重载实体。\n'
                    '右键/点击小三角：\n'
                    '   从系统中重载：重新同步缓存。'
                )
            )
        else:
            self._qt_reload_button._set_name_text_('Reload')
            self._qt_reload_button._set_tool_tip_(
                (
                    'Click on Reload Entity from Cache. \n'
                    'Right click/click on the small triangle: \n'
                    'Reload from System: Sync cache.'
                )
            )

        self._qt_entity_input = gui_qt_widgets.QtInputForEntity()
        self._qt_layout_0.addWidget(self._qt_entity_input)

        self._prs_root = lnx_prs_swap.Swap.generate_root()

        self._qt_entity_input._set_next_buffer_fnc_(
            self._next_buffer_fnc
        )

        # self._qt_entity_input._set_root_text_('Shot:')
        self._qt_entity_input._set_value_('/')

        self._qt_entity_input._setup_()

        if history_key is None:
            history_key = self.HISTORY_KEY

        self._qt_entity_input._set_history_key_(history_key)
        self._qt_entity_input._pull_history_latest_()
        self._qt_entity_input.user_history_pull_accepted.connect(self._pull_history_fnc)

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
                    ('reload form system', 'reload-force', self._on_resync_entities)
                ]
            )

        self._cache_entities()
        self._on_reload_entities()

    def _cache_projects(self):
        name_texts = []
        gui_name_dict = {}
        keyword_filter_dict = collections.OrderedDict()
        tag_filter_dict = collections.OrderedDict()
        for i_entity in self._prs_root.projects(cache_flag=self._scan_cache_flag):
            i_name = i_entity.name
            name_texts.append(i_entity.name)

            i_gui_name = i_entity.variants.get('entity_gui_name')
            gui_name_dict[i_name] = i_gui_name
            keyword_filter_dict[i_name] = filter(None, [i_name, i_gui_name])
            tag_filter_dict[i_name] = ['All']

        return dict(
            type_text='project',
            name_texts=name_texts,
            gui_name_dict=gui_name_dict,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

    def _cache_sequences(self, path_opt):
        name_texts = []
        gui_name_dict = {}
        keyword_filter_dict = collections.OrderedDict()
        tag_filter_dict = collections.OrderedDict()

        project = self._prs_root.get_entity(path_opt.to_string())
        if project is not None:
            sequences = project.sequences(cache_flag=self._scan_cache_flag)
            for i_entity in sequences:
                i_name = i_entity.name
                name_texts.append(i_entity.name)
                i_gui_name = i_entity.variants.get('entity_gui_name')
                gui_name_dict[i_name] = i_gui_name
                keyword_filter_dict[i_name] = filter(None, [i_name, i_gui_name])
                tag_filter_dict[i_name] = ['All', i_entity.properties.episode]

        return dict(
            type_text='sequence',
            gui_name_dict=gui_name_dict,
            name_texts=name_texts,
            tag_filter_dict=tag_filter_dict,
            keyword_filter_dict=keyword_filter_dict
        )

    def _pull_history_fnc(self, path_text):
        self._next_buffer_fnc(
            bsc_core.BscNodePathOpt(path_text)
        )

    def _next_buffer_fnc(self, path_opt):
        cs = path_opt.get_components()
        cs.reverse()
        d = len(cs)
        if d == 1:
            project_data = self._cache_projects()
            return project_data
        elif d == 2:
            sequence_data = self._cache_sequences(path_opt)
            return sequence_data
        return dict()

    def connect_input_change_accepted_to(self, fnc):
        self._qt_entity_input.input_value_accepted.connect(fnc)

    def _cache_entities(self):
        path = self._qt_entity_input._get_value_()
        path_opt = bsc_core.BscNodePathOpt(path)
        cs = path_opt.get_components()
        cs.reverse()

        for i in cs:
            i_d = i.get_depth()
            if i_d == 1:
                self._cache_projects()
            elif i_d == 2:
                self._cache_sequences(i)

    def _on_reload_entities(self):
        def post_fnc_():
            self._scan_cache_flag = True

        path_text = self._qt_entity_input._get_value_()
        self._scan_cache_flag = False
        self._qt_entity_input._update_next_data_for_(path_text, post_fnc_)

    def _on_resync_entities(self):
        def post_fnc_():
            self._scan_cache_flag = True
            lnx_prs_swap.Swap.set_sync_cache_flag(True)

        def fnc_():
            self._scan_cache_flag = False
            lnx_prs_swap.Swap.set_sync_cache_flag(False)
            self._qt_entity_input._update_next_data_for_(path_text, post_fnc_)

        path_text = self._qt_entity_input._get_value_()

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

    def get_entity(self, path_text):
        return self._prs_root.get_entity(path_text)

    def get_path(self):
        return self._qt_entity_input._get_value_()

    def set_path(self, path_text):
        self._qt_entity_input._set_value_(path_text)
        # cache when path is applied
        self._cache_entities()
