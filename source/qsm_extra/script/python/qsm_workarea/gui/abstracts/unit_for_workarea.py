# coding:utf-8
import collections

import lxbasic.content as bsc_content

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.abstracts as prx_abstracts


class _GuiBaseOpt(object):
    GUI_NAMESPACE = 'storage'

    def __init__(self, window, session):
        self._window = window
        self._session = session


class _GuiDirectoryOpt(
    _GuiBaseOpt,
    prx_abstracts.AbsGuiPrxTreeViewOpt
):
    def __init__(self, window, session, prx_tree_view):
        super(_GuiDirectoryOpt, self).__init__(window, session)
        self._init_tree_view_opt_(prx_tree_view, self.GUI_NAMESPACE)

        self._variants = dict()

        self._directory_ptn_opt = bsc_core.BscStgParseOpt(
            '{location}/{entity}/workarea/user.{artist}/{step}.{task}'
        )
        self._file_ptn_opt = bsc_core.BscStgParseOpt(
            '{location}/{entity}/workarea/user.{artist}/{step}.{task}/{task_extra}/{entity}.{step}.{task}.{task_extra}.v{version}{ext}'
        )

        self._gui_thread_flag = 0
        self._root = None
        self._root_opt = None

        self._cache_expand_all = dict()
        self._cache_expand_current = dict()

        self._prx_tree_view.create_header_view(
            [('name', 2)],
            480
        )

    def restore(self):
        self.__push_expand_cache()

        self._prx_tree_view.set_clear()
        self._keys.clear()

    def __push_expand_cache(self):
        if self._root is not None:
            if self._root not in self._cache_expand_all:
                expand_dict = dict()
                self._cache_expand_all[self._root] = expand_dict
            else:
                expand_dict = self._cache_expand_all[self._root]

            for k, v in self._item_dict.items():
                expand_dict[k] = v.get_is_expanded()

    def __pull_expand_cache(self):
        # load expand cache
        if self._root in self._cache_expand_all:
            self._cache_expand_current = self._cache_expand_all[self._root]

    def gui_add_root(self, directory_path):
        directory_opt = bsc_storage.StgDirectoryOpt(directory_path)
        self._root = directory_opt.get_parent_path()
        self._root_opt = directory_opt

        self.__pull_expand_cache()

        path = directory_path[len(self._root):]
        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscPathOpt(path)
            prx_item = self._prx_tree_view.create_item(
                path_opt.get_name(),
                icon=gui_core.GuiIcon.get('database/all'),
            )
            self.gui_register(path, prx_item)

            prx_item.set_gui_dcc_obj(
                directory_opt, self._namespace
            )

            prx_item.set_expanded(True)
            prx_item.set_gui_menu_data(
                [
                    ('system',),
                    ('open folder', 'file/open-folder', directory_opt.open_in_system)
                ]
            )
            return True, prx_item
        return False, self.gui_get_one(path)

    def gui_add_directory(self, directory_opt):
        directory_path = directory_opt.get_path()
        path = directory_path[len(self._root):]
        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscPathOpt(path)
            #
            parent_gui = self.gui_get_one(path_opt.get_parent_path())
            #
            prx_item = parent_gui.add_child(
                path_opt.name,
                icon=gui_core.GuiIcon.get_directory(),
            )
            self.gui_register(path, prx_item)
            prx_item.set_tool_tip(path)
            if path in self._cache_expand_current:
                prx_item.set_expanded(self._cache_expand_current[path])

            prx_item.set_gui_dcc_obj(
                directory_opt, self._namespace
            )

            prx_item.set_gui_menu_data(
                [
                    ('system',),
                    ('open folder', 'file/open-folder', directory_opt.open_in_system)
                ]
            )
            if directory_opt.get_is_readable() is False:
                prx_item.set_status(
                    prx_item.ValidationStatus.Unreadable
                )
            elif directory_opt.get_is_writeable() is False:
                prx_item.set_status(
                    prx_item.ValidationStatus.Unwritable
                )
            return prx_item
        return self.gui_get_one(path)

    def gui_add_next_directories(self, directory_path):
        directory_opt = bsc_storage.StgDirectoryOpt(directory_path)
        directory_opts = directory_opt.get_directories()
        # sort result
        directory_opts.sort(key=lambda x: bsc_core.RawTextMtd.to_number_embedded_args(x.path))
        for i_directory_opt in directory_opts:
            self.gui_add_directory(i_directory_opt)

    def gui_add_next_directories_use_thread(self, directory_path):
        def cache_fnc_():
            directory_opts = directory_opt.get_directories()
            directory_opts.sort(key=lambda x: bsc_core.RawTextMtd.to_number_embedded_args(x.path))
            return [
                self._gui_thread_flag,
                directory_opts
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _directory_opts = args[0]
            with self._prx_tree_view.gui_bustling():
                for _i_directory_opt in _directory_opts:
                    if _index_thread_batch_current != self._gui_thread_flag:
                        break
                    self.gui_add_directory(_i_directory_opt)

        def post_fnc_():
            pass

        self._gui_thread_flag += 1

        directory_opt = bsc_storage.StgDirectoryOpt(directory_path)

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()

    def gui_get_current_directory(self):
        _ = self._prx_tree_view.get_current_item()
        if _:
            directory_opt = _.get_gui_dcc_obj(self.GUI_NAMESPACE)
            if directory_opt != self._root_opt:
                return directory_opt

    def gui_setup(self, variants):
        self._variants = variants
        self._directory_ptn_opt.update_variants(**variants)
        self._file_ptn_opt.update_variants(**variants)
        if not self._directory_ptn_opt.get_keys():
            root = self._directory_ptn_opt.get_value()
            root_opt = bsc_storage.StgDirectoryOpt(root)
            if root_opt.get_is_exists() is False:
                root_opt.set_create()

            self.gui_add_root(root)
            self.gui_add_next_directories_use_thread(root)

    def get_file_opts(self):
        list_ = []
        directory_opt = self.gui_get_current_directory()
        if directory_opt is not None:
            variants = dict()
            variants['task_extra'] = directory_opt.get_name()

            ptn_opt = self._file_ptn_opt.update_variants_to(**variants)
            matches = ptn_opt.get_matches()
            matches.reverse()
            if matches:
                for i_variants in matches:
                    i_file_path = i_variants['result']
                    i_properties = bsc_content.NodeProperties(i_variants)
                    i_file_opt = bsc_storage.StgFileOpt(i_file_path)
                    i_file_opt.properties = i_properties
                    list_.append(i_file_opt)

        return list_


class _GuiFileOpt(
    _GuiBaseOpt,
    prx_abstracts.AbsGuiPrxListViewAsFileOpt
):

    @classmethod
    def find_image(cls, file_opt):
        directory_path = file_opt.get_directory_path()
        file_name_base = file_opt.get_name_base()
        image_file_path = '{}/.snapshot/{}.jpg'.format(directory_path, file_name_base)
        if bsc_storage.StgPath.get_is_file(image_file_path):
            return image_file_path

    def __init__(self, window, session, prx_list_view):
        super(_GuiFileOpt, self).__init__(window, session)
        self._init_list_view_as_file_opt_(prx_list_view, self.GUI_NAMESPACE)

        self._item_frame_size = 200, 100+16*2
        self._item_image_frame_size = 200, 100
        self._item_name_frame_size = 16, 16
        self._prx_list_view.set_item_frame_size_basic(*self._item_frame_size)
        self._prx_list_view.set_item_image_frame_size(*self._item_image_frame_size)
        self._prx_list_view.set_item_name_frame_size(*self._item_name_frame_size)
        self._prx_list_view.set_item_name_frame_draw_enable(False)
        self._prx_list_view.set_item_names_draw_range([None, 2])
        self._prx_list_view.set_item_image_frame_draw_enable(False)
        self._prx_list_view.set_selection_use_multiply()

        self._prx_list_view.connect_press_released_to(self.do_copy_to_clipboard_by_selection)

    def do_copy_to_clipboard_by_selection(self):
        pass

    def gui_add_file(self, file_opt):
        def cache_fnc_():
            def copy_path_fnc_():
                gui_qt_core.GuiQtUtil.copy_text_to_clipboard(file_path)

            def open_folder_fnc():
                bsc_storage.StgFileOpt(file_path).open_in_system()

            _name_dict = collections.OrderedDict()
            _location = file_opt.get_path()

            _name_dict['version'] = file_opt.properties.version
            _name_dict['time'] = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                file_opt.get_modify_timestamp(), language=1
            )

            _menu_data = [
                (),
                ('Copy Path', 'copy', copy_path_fnc_),
                ('Open Folder', 'file/open-folder', open_folder_fnc)
            ]
            return [
                prx_item_widget, _location, _name_dict, _menu_data,
            ]

        def build_fnc_(*args):
            _prx_item_widget, _location, _name_dict, _menu_data = args[0]
            _image_path = self.find_image(file_opt)
            if _image_path is not None:
                _thumbnail_file_path, _image_shell_script = bsc_storage.ImgOiioOptForThumbnail(
                    _image_path).generate_thumbnail_create_args(
                    width=240, ext='.jpg'
                )
                prx_item_widget.set_image(_thumbnail_file_path)
                if _image_shell_script is not None:
                    prx_item_widget.set_image_show_args(_thumbnail_file_path, _image_shell_script)
            else:
                file_icon = gui_qt_core.GuiQtDcc.get_qt_file_icon(file_path)
                if file_icon:
                    pixmap = file_icon.pixmap(80, 80)
                    prx_item_widget.set_image(
                        pixmap
                    )
            _prx_item_widget.set_name_dict(_name_dict)
            if _menu_data:
                _prx_item_widget.set_menu_data(
                    _menu_data
                )
            _prx_item_widget.set_tool_tip(
                file_path
            )
            _prx_item_widget.refresh_widget_force()

        file_path = file_opt.path
        file_name = file_opt.name

        if self.gui_check_exists(file_path) is False:
            prx_item_widget = self._prx_list_view.create_item_widget()
            self._item_dict[file_path] = prx_item_widget
            version = file_opt.properties.version
            # prx_item_widget.set_names([version])
            prx_item_widget.set_drag_enable(True)
            prx_item_widget.set_drag_urls([file_opt.get_path()])
            prx_item_widget.get_item()._update_item_keyword_filter_keys_tgt_(
                [file_opt.name]
            )
            prx_item_widget.set_show_fnc(
                cache_fnc_, build_fnc_
            )
            prx_item_widget.set_gui_dcc_obj(
                file_opt, namespace=self.GUI_NAMESPACE
            )
            return prx_item_widget
        return self.gui_get_one(file_path)


class AbsPrxUnitForWorkarea(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    def do_gui_refresh_files(self):
        self._gui_file_opt.restore()
        file_opts = self._gui_directory_opt.get_file_opts()
        if file_opts:
            for i_file_opt in file_opts:
                self._gui_file_opt.gui_add_file(i_file_opt)

    def do_save(self):
        pass

    def do_save_to(self):
        pass

    def do_save_new(self):
        pass

    def __init__(self, *args, **kwargs):
        super(AbsPrxUnitForWorkarea, self).__init__(*args, **kwargs)

        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_lot = qt_widgets.QtVBoxLayout(self.widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)
        # qt_lot._set_align_top_()
        # label
        self._qt_title_label = qt_widgets.QtTextItem()
        qt_lot.addWidget(self._qt_title_label)
        self._qt_title_label._set_name_align_h_center_()
        self._qt_title_label.setFixedHeight(20)
        #
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        qt_lot.addWidget(prx_sca._qt_widget)

        prx_spt_h = gui_prx_widgets.PrxHSplitter()
        prx_sca.add_widget(prx_spt_h)

        self._directory_prx_tree_view = gui_prx_widgets.PrxTreeView()
        prx_spt_h.add_widget(self._directory_prx_tree_view)

        self._root = None

        self._gui_directory_opt = _GuiDirectoryOpt(self, None, self._directory_prx_tree_view)
        self._directory_prx_tree_view.connect_item_select_changed_to(self.do_gui_refresh_files)

        # self._prx_version_file_view = PrxViewForFile()
        self._file_prx_list_view = gui_prx_widgets.PrxListView()
        prx_spt_h.add_widget(self._file_prx_list_view)

        self._gui_file_opt = _GuiFileOpt(self, None, self._file_prx_list_view)

        prx_spt_h.set_fixed_size_at(0, 200)

        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_lot.addWidget(self._bottom_prx_tool_bar._qt_widget)
        self._bottom_prx_tool_bar.set_expanded(True)
        self._bottom_prx_tool_bar.set_align_right()

        self._save_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._save_prx_button)
        self._save_prx_button.set_name('Save')
        self._save_prx_button.set_icon_name('tool/save')
        self._save_prx_button.set_width(96)
        self._save_prx_button.connect_press_clicked_to(self.do_save)

        self._save_to_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._save_to_prx_button)
        self._save_to_prx_button.set_name('Save to')
        self._save_to_prx_button.set_icon_name('tool/save-to')
        self._save_to_prx_button.set_width(96)
        self._save_to_prx_button.connect_press_clicked_to(self.do_save_to)

        self._save_new_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._save_new_prx_button)
        self._save_new_prx_button.set_name('Save New')
        self._save_new_prx_button.set_icon_name('tool/save-new')
        self._save_new_prx_button.set_width(96)
        self._save_new_prx_button.connect_press_clicked_to(self.do_save_new)

        self._variants = dict()
        self._title_ptn = '{entity}.{step}.{task}'

    def setup(self, variants):
        self._variants = variants
        self.set_title(self._title_ptn.format(**self._variants))
        self._gui_directory_opt.gui_setup(variants)

    def get_variants(self):
        return self._variants

    def set_title(self, name_text):
        self._qt_title_label._set_name_text_(name_text)

    def create_group(self, name_text):
        pass