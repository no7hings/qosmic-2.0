# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core

from ...qt.widgets import button as _qt_widget_button

from ...qt.view_widgets import base as _qt_vew_wgt_base

from ...qt.view_widgets.list import view as _qt_vew_wgt_list
# proxy abstracts
from .. import abstracts as gui_prx_abstracts

from . import container as _container


class PrxSceneView(
    gui_prx_abstracts.AbsPrxWidget,
):
    QT_WIDGET_CLS = _qt_vew_wgt_base._BaseViewWidget
    QT_VIEW_CLS = _qt_vew_wgt_list._QtListView

    def __init__(self, *args, **kwargs):
        super(PrxSceneView, self).__init__(*args, **kwargs)

        self._qt_widget._set_toolbar_hide_flag_(True)

        self._qt_view = self.QT_VIEW_CLS()
        self._qt_widget._grid_lot.addWidget(self._qt_view, 0, 0, 1, 1)
        self._qt_view.setFocusProxy(self._qt_widget)
        self._qt_view._view_model.set_item_frame_size(200, 106)

        self._bottom_prx_tool_bar = _container.PrxHToolBar()
        self._bottom_prx_tool_bar.set_name('bottom')
        self._bottom_prx_tool_bar.set_align_right()
        self._qt_widget._grid_lot.addWidget(self._bottom_prx_tool_bar.widget, 1, 0, 1, 1)
        self._bottom_prx_tool_bar.set_border_radius(1)
        self._bottom_prx_tool_bar.set_expanded(True)

        self._save_qt_button = _qt_widget_button.QtPressButton()
        self._bottom_prx_tool_bar.add_widget(self._save_qt_button)
        self._save_qt_button._set_name_text_('Save')
        self._save_qt_button._set_icon_name_('tool/save')
        self._save_qt_button._fix_width_to_name_(20)
        self._save_qt_button.press_clicked.connect(self._do_save_scene)
        self._save_qt_button._set_menu_data_generate_fnc_(
            self._save_to_menu_data_generate_fnc
        )

        self._root = None

        self._scene_ext = '.ma'
        self._thumbnail_ext = '.jpg'

        self._directory_pattern = None
        self._scene_pattern = None
        self._thumbnail_pattern = None

        self._open_scene_fnc = None
        self._save_scene_fnc = None

        self._scene_gain_fnc = None

        self._name_current = None

        self._item_dict = self._qt_view._view_model._data.item_dict

    def set_root(self, path):
        self._root = path

        self._directory_pattern = '{}/{{name}}'.format(
            self._root
        )
        self._scene_pattern = '{}/{{name}}/{{name}}.v{{version}}{}'.format(
            self._root, self._scene_ext
        )
        self._thumbnail_pattern = '{}/{{name}}/.thumbnails/{{name}}.v{{version}}{}'.format(
            self._root, self._thumbnail_ext
        )

    def set_scene_ext(self, file_ext):
        self._scene_ext = file_ext

    def connect_open_scene_to(self, fnc):
        self._open_scene_fnc = fnc

    def connect_save_scene_to(self, fnc):
        self._save_scene_fnc = fnc

    def update(self):
        self._item_dict.clear()
        _directory_paths = bsc_storage.StgDirectoryOpt(self._root).get_directory_paths()
        for i_directory_path in _directory_paths:
            self._add_for_branch(i_directory_path)
        self.update_current()

    def update_current(self):
        scene_path = self.get_scene_current()
        if scene_path:
            self.update_current_by_scene_path(scene_path)

    def to_thumbnail_path(self, scene_path):
        ptn_opt = bsc_core.BscStgParseOpt(self._scene_pattern)
        variants = ptn_opt.get_variants(scene_path)
        return self._thumbnail_pattern.format(**variants)

    def get_scene_current(self):
        if self._scene_gain_fnc is not None:
            return self._scene_gain_fnc()

    def set_scene_gain_fnc(self, fnc):
        self._scene_gain_fnc = fnc

    def _check_scene_is_valid(self, file_path):
        pass

    def _do_save_scene(self):
        scene_path_current = self.get_scene_current()
        if scene_path_current:
            pth_opt = bsc_core.BscStgParseOpt(self._scene_pattern)
            if pth_opt.check_is_matched(scene_path_current) is True:
                variants = pth_opt.get_variants(scene_path_current)
                name = variants['name']
                self.save_to_name(name)
            else:
                self.save_new()

    def save_to_scene(self, scene_path, new_version=True):
        if new_version is True:
            pth_opt = bsc_core.BscStgParseOpt(self._scene_pattern)
            variants = pth_opt.get_variants(scene_path)
            version = int(variants['version'])
            scene_path_new = self._scene_pattern.format(
                name=variants['name'], version=str(version+1).zfill(3)
            )
            self._on_save_scene(scene_path_new)
        else:
            self._on_save_scene(scene_path)

    def get_all_names(self):
        return [bsc_storage.StgDirectoryOpt(x).name for x in self._item_dict]

    def _save_to_menu_data_generate_fnc(self):
        sub_menu_data = []
        for k, v in self._item_dict.items():
            i_name = bsc_storage.StgDirectoryOpt(k).name
            if i_name != self._name_current:
                sub_menu_data.append(
                    (i_name, 'file/file', functools.partial(self.save_to_name, i_name))
                )
        return [
            [
                'Save to', 'tool/save-to',
                sub_menu_data
            ],
            ('Save New', 'tool/save-as', self.save_new)
        ]

    def save_to_name(self, name):
        scene_paths = self.get_scene_paths_for(name)
        if scene_paths:
            scene_path = scene_paths[-1]
            self.save_to_scene(scene_path, new_version=True)
        else:
            scene_path = self._scene_pattern.format(
                name=name, version='001'
            )
            self.save_to_scene(scene_path, new_version=False)

    def get_scene_paths_for(self, name):
        ptn_opt = bsc_core.BscStgParseOpt(self._scene_pattern)
        ptn_opt = ptn_opt.update_variants_to(name=name)
        return ptn_opt.get_exists_results()

    def get_scene_path_latest_for(self, name):
        pass

    def save_new(self):
        name = _gui_core.GuiApplication.exec_input_dialog(
            type='string', info='Entry name for create...', title='New Scene'
        )
        if name is not None:
            all_name = self.get_all_names()
            if name not in all_name:
                self.save_to_name(name)
                directory_path = self._directory_pattern.format(name=name)
                self._add_for_branch(directory_path)
                self.update_current()
            else:
                _gui_core.GuiApplication.exec_message_dialog(
                    'Name is exists.'
                )

    def _open_file_menu_data_generate_fnc(self, name):
        scene_paths = self.get_scene_paths_for(name)
        if scene_paths:
            # clip to 20
            scene_paths = scene_paths[-20:]
            sub_menu_data = []
            for i_file_path in scene_paths:
                sub_menu_data.append(
                    (
                        bsc_storage.StgFileOpt(i_file_path).name,
                        'file/file',
                        functools.partial(self._on_open_scene, i_file_path)
                    ),
                )
            return [
                ['Open File', 'file/folder-open', sub_menu_data],
                ('Open Folder', 'file/folder', lambda: bsc_storage.StgFileOpt(scene_paths[0]).show_in_system())
            ]
        return []

    def _on_open_scene(self, scene_path):
        if self._open_scene_fnc is not None:
            result = self._open_scene_fnc(scene_path)
            if result is True:
                self.update_current_by_scene_path(scene_path)

    def _on_open_latest_scene(self, qt_item):
        if self._open_scene_fnc is not None:
            scene_path = qt_item._item_model.get_assign_file()
            ptn_opt = bsc_core.BscStgParseOpt(self._scene_pattern)
            variants = ptn_opt.get_variants(scene_path)
            scene_paths = self.get_scene_paths_for(variants['name'])
            if scene_paths:
                scene_path_latest = scene_paths[-1]
                result = self._open_scene_fnc(scene_path_latest)
                if result is True:
                    self.update_current_by_scene_path(scene_path_latest)

    def _on_save_scene(self, scene_path):
        if self._save_scene_fnc is not None:
            thumbnail_path = self.to_thumbnail_path(scene_path)
            result = self._save_scene_fnc(scene_path, thumbnail_path)
            if result is True:
                self.update_current_by_scene_path(scene_path)

    def update_current_by_scene_path(self, scene_path):
        file_opt = bsc_storage.StgFileOpt(scene_path)
        ptn_opt = bsc_core.BscStgParseOpt(self._scene_pattern)
        variants = ptn_opt.get_variants(scene_path)
        directory_path = file_opt.directory_path
        qt_item = self._qt_view._view_model._get_item(directory_path)
        if qt_item is not None:
            self._name_current = variants['name']

            qt_item._item_model.set_name(file_opt.name)
            thumbnail_path = self._thumbnail_pattern.format(**variants)
            qt_item._item_model.set_image(thumbnail_path)
            self._update_current_status(qt_item)

    def _update_current_status(self, qt_item):
        [x._item_model.set_status_enable(False) for x in self._qt_view._view_model.get_all_items()]
        qt_item._item_model.set_status(qt_item._item_model.Status.Warning)

    def _add_for_branch(self, directory_path, *args, **kwargs):
        directory_opt = bsc_storage.StgDirectoryOpt(directory_path)
        name = directory_opt.name
        flag, qt_item = self._qt_view._view_model.create_item(directory_opt.path)
        scene_paths = self.get_scene_paths_for(name)
        if scene_paths:
            scene_path_current = scene_paths[-1]
            thumbnail_path_current = self.to_thumbnail_path(scene_path_current)
            qt_item._item_model.set_image(thumbnail_path_current)
            qt_item._item_model.set_name(bsc_storage.StgFileOpt(scene_path_current).name)
            qt_item._item_model.set_menu_data_generate_fnc(
                functools.partial(self._open_file_menu_data_generate_fnc, name)
            )
            qt_item._item_model.set_assign_file(scene_path_current)
            qt_item._item_model.register_press_dbl_click_fnc(
                functools.partial(self._on_open_latest_scene, qt_item)
            )
        return qt_item
