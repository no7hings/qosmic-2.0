# coding:utf-8
import six

import fnmatch

import collections

import functools

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.extra.methods as bsc_etr_methods

import lxresolver.core as rsv_core
# session
import lxsession.core as ssn_core

import lxsession.objects as ssn_objects

import lxsession.commands as ssn_commands
# gui
import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt_for_usd.core as gui_qt_usd_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as prx_widgets


class _GuiBaseOpt(object):
    DCC_NAMESPACE = 'resolver'

    def __init__(self, window, session, resolver):
        self._window = window
        self._session = session
        self._resolver = resolver


# noinspection PyUnusedLocal
class _GuiEntityOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxTreeViewOpt
):
    ROOT_NAME = 'All'

    def __init__(self, window, session, resolver, prx_tree_view):
        super(_GuiEntityOpt, self).__init__(window, session, resolver)
        self._init_tree_view_opt_(
            prx_tree_view, self.DCC_NAMESPACE
        )

    def gui_add_root(self):
        path = '/'
        if self.gui_get_is_exists(path) is False:
            prx_item = self._prx_tree_view.create_item(
                self.ROOT_NAME,
                icon=gui_core.GuiIcon.get('database/all'),
            )
            self.gui_register(path, prx_item)
            prx_item.set_gui_dcc_obj(self._resolver, namespace=self.DCC_NAMESPACE)
            prx_item.set_expanded(True)
            prx_item.set_checked(False)
            return True, prx_item
        return False, self.gui_get(path)

    def gui_add(self, obj, use_show_thread=False):
        name = obj.name
        path = obj.path
        type_name = obj.type
        if self.gui_get_is_exists(path) is True:
            prx_item = self.gui_get(path)
            return False, prx_item
        else:
            create_kwargs = dict(
                name=name,
                filter_key=obj.path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self.gui_get(parent.path)
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **create_kwargs
                )
            #
            prx_item.set_type(obj.get_type_name())
            prx_item.set_checked(False)
            prx_item.update_keyword_filter_keys_tgt(
                [type_name, name]
            )
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.DCC_NAMESPACE)
            self.gui_register(path, prx_item)
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    functools.partial(
                        self.gui_show_deferred_fnc, prx_item
                    )
                )
                return True, prx_item
            #
            self.gui_show_deferred_fnc(prx_item)
            return True, prx_item

    def gui_show_deferred_fnc(self, prx_item):
        obj = prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
        obj_type_name = obj.type_name
        name = obj.name
        #
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        prx_item.set_icon_by_file(obj.icon)
        prx_item.set_name(name)
        prx_item.set_tool_tip(obj.description)
        #
        menu_raw.extend(
            [
                ('expanded',),
                ('Expand branch', None, prx_item.set_expand_branch),
                ('Collapse branch', None, prx_item.set_collapse_branch),
            ]
        )
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def gui_add_one(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i in ancestors:
                i_path = i.get_path()
                if self.gui_get_is_exists(i_path) is False:
                    self.gui_add(i, use_show_thread=True)
        #
        return self.gui_add(obj, use_show_thread=True)

    def gui_add_project(self, rsv_project):
        is_create, prx_item = self.gui_add_one(
            rsv_project
        )
        if is_create is True:
            prx_item.set_expanded(True)
            self.gui_add_for_all_resources(rsv_project)

    def gui_add_for_all_resources(self, rsv_project):
        def post_fnc_():
            self._end_timestamp = bsc_core.SysBaseMtd.get_timestamp()
            #
            bsc_log.Log.trace_method_result(
                'load asset/shot from "{}"'.format(
                    rsv_project.path
                ),
                'count={}, cost-time="{}"'.format(
                    self.__resource_count,
                    bsc_core.RawIntegerMtd.second_to_time_prettify(self._end_timestamp-self._start_timestamp)
                )
            )

        def quit_fnc_():
            ts.do_quit()

        #
        self.__resource_count = 0
        self._start_timestamp = bsc_core.SysBaseMtd.get_timestamp()
        #
        rsv_resource_groups = rsv_project.get_rsv_resource_groups(**self._window._rsv_filter_opt.value)
        #
        if self._window._qt_thread_enable is True:
            ts = gui_qt_core.QtBuildThreadStack(self._window.widget)
            ts.run_finished.connect(post_fnc_)
            for i_rsv_resource_group in rsv_resource_groups:
                ts.register(
                    cache_fnc=functools.partial(self.gui_cache_fnc_for_resources_by_group, i_rsv_resource_group),
                    build_fnc=self.gui_build_fnc_for_resources
                )
            #
            ts.set_start()
            #
            self._window.connect_window_close_to(quit_fnc_)
        else:
            with bsc_log.LogProcessContext.create(
                maximum=len(rsv_resource_groups), label='gui-add for resource'
            ) as g_p:
                for i_rsv_resource_group in rsv_resource_groups:
                    g_p.do_update()
                    self.gui_build_fnc_for_resources(
                        self.gui_cache_fnc_for_resources_by_group(i_rsv_resource_group)
                    )

    # refresh resources by group
    def gui_cache_fnc_for_resources_by_group(self, rsv_resource_group):
        rsv_objs = rsv_resource_group.get_rsv_resources(**self._window._rsv_filter_opt.value)
        return rsv_objs

    def gui_build_fnc_for_resources(self, rsv_resources):
        for i_rsv_resource in rsv_resources:
            self.gui_add_resource(i_rsv_resource)

            self.register_completion(i_rsv_resource.name)
            self.register_occurrence(
                i_rsv_resource.name, i_rsv_resource.path
            )
        #
        self.__resource_count += len(rsv_resources)

    def gui_add_resource(self, rsv_resource):
        is_create, prx_item = self.gui_add_one(
            rsv_resource
        )
        if is_create is True:
            prx_item.start_loading()
            #
            branch = rsv_resource.properties.get('branch')
            if branch == 'asset':
                menu_content = self.__generate_rsv_resource_menu_content(rsv_resource)
                if menu_content:
                    rsv_resource.set_gui_menu_content(
                        menu_content
                    )
            #
            self._prx_tree_view.connect_item_expand_to(
                prx_item,
                lambda *args, **kwargs: self._window._do_gui_refresh_for_tasks_by_resource_expand_changed(
                    rsv_resource
                ),
                time=100
            )

    def __generate_rsv_resource_menu_content(self, rsv_resource):
        hook_keys = self._window._hook_configure.get(
            'actions.asset.hooks'
        ) or []
        return self._window._get_menu_content_by_hook_keys_(
            self._window._session_dict, hook_keys, rsv_resource
        )

    def gui_add_task(self, rsv_task):
        is_create, rsv_task_item_prx = self.gui_add_one(
            rsv_task
        )
        if is_create is True:
            task_menu_content = self.__generate_rsv_task_menu_content(rsv_task)
            if task_menu_content:
                rsv_task.set_gui_menu_content(
                    task_menu_content
                )

    def __generate_rsv_task_menu_content(self, rsv_task):
        hook_keys = self._window._hook_configure.get(
            'actions.task.hooks'
        ) or []
        return self._window._get_menu_content_by_hook_keys_(
            self._window._session_dict, hook_keys, rsv_task
        )


class _GuiTagOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiTreeViewAsTagOpt
):
    GROUP_SCHEME = gui_prx_abstracts.AbsGuiTreeViewAsTagOpt.GroupScheme.Hide

    def __init__(self, window, session, resolver, prx_tree_view):
        super(_GuiTagOpt, self).__init__(window, session, resolver)
        self._init_tree_view_as_tag_opt_(prx_tree_view, self.DCC_NAMESPACE)

        self._index_thread_batch = 0

    def gui_add_all_groups(self, rsv_project):
        self.gui_add_root()
        branch = self._window._rsv_filter_opt.get('branch')
        all_steps = rsv_project.get_all_steps(branch=branch)
        for i_step in all_steps:
            i_path = '/{}'.format(i_step)
            self.gui_add_group_by_path(i_path)

    def gui_add_all_groups_use_thread(self, rsv_project):
        def cache_fnc_():
            branch = self._window._rsv_filter_opt.get('branch')
            return [
                self._index_thread_batch,
                rsv_project.get_all_steps(branch=branch)
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _all_steps = args[0]
            for _i_step in _all_steps:
                _i_path = '/{}'.format(_i_step)
                self.gui_add_group_by_path(_i_path)

        def post_fnc_():
            pass

        self.gui_add_root()

        self._index_thread_batch += 1

        t = gui_qt_core.QtBuildThread(self._window.widget)
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


# noinspection PyUnusedLocal
class _GuiTaskOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxListViewOpt
):
    CACHE = dict()

    def __init__(self, window, session, resolver, prx_list_view):
        super(_GuiTaskOpt, self).__init__(window, session, resolver)
        self._init_list_view_opt_(
            prx_list_view, self.DCC_NAMESPACE
        )

    def gui_add_one(self, rsv_task):
        def build_fnc_(data_):
            self.__gui_built_fnc(
                rsv_task, prx_item_widget, data_
            )

        path = rsv_task.get_path()
        if self.gui_get_is_exists(path) is True:
            return self.gui_get(path)

        valid = self.__get_is_valid(rsv_task)
        if valid is True:
            project = rsv_task.get('project')
            branch = rsv_task.get('branch')
            name = rsv_task.get(branch)
            step = rsv_task.get('step')
            task = rsv_task.get('task')

            name_dict = collections.OrderedDict(
                [
                    (branch, name),
                    ('step', step),
                    ('task', task)
                ]
            )
            path = rsv_task.get_path()
            prx_item_widget = self._prx_list_view.create_item_widget()
            self.gui_register(path, prx_item_widget)
            prx_item_widget.set_index_draw_enable(True)
            prx_item_widget.set_check_enable(True)
            prx_item_widget.set_gui_dcc_obj(
                rsv_task, namespace=self.DCC_NAMESPACE
            )
            prx_item_widget.set_gui_attribute('path', rsv_task.get_path())
            prx_item_widget.set_name(rsv_task.get_path())
            prx_item_widget.set_name_dict(name_dict)
            prx_item_widget.set_icon_by_name(step)
            prx_item_widget.set_tool_tip(rsv_task.description)
            prx_item_widget.set_sort_name_key(rsv_task.get_name())
            prx_item_widget.set_keyword_filter_keys_tgt(
                {rsv_task.properties.get(i) or 'unknown' for i in self._resolver.VariantTypes.Mains}
            )
            tag_path = '/{}/{}'.format(step, task)
            prx_item_widget.get_item()._update_item_tag_filter_keys_tgt_([tag_path])
            self._window._gui_tag_opt.gui_register_tag_by_path(tag_path, rsv_task.get_path())

            prx_item_widget.set_show_fnc(
                functools.partial(self.__gui_cache_fnc, rsv_task),
                build_fnc_
            )
            return prx_item_widget

    def __get_is_valid(self, rsv_task):
        for i_keyword, i_hidden in self._window._available_rsv_show_args:
            i_rsv_unit = rsv_task.get_rsv_unit(
                keyword=i_keyword
            )
            i_file_path = i_rsv_unit.get_result(version='latest')
            if i_file_path:
                return True
        return False

    def __gui_cache_fnc(self, rsv_task):
        key = rsv_task.get_path()

        if key in self.__class__.CACHE:
            return self.__class__.CACHE[key]

        project = rsv_task.get('project')
        branch = rsv_task.get('branch')
        name = rsv_task.get(branch)
        step = rsv_task.get('step')
        task = rsv_task.get('task')
        #
        name_dict = collections.OrderedDict(
            [
                (branch, name),
                ('step', step),
                ('task', task)
            ]
        )
        #
        review_rsv_unit = rsv_task.get_rsv_unit(
            keyword='{branch}-review-file'
        )
        image_args = None
        movie_file_path = review_rsv_unit.get_exists_result(
            version='latest'
        )
        if movie_file_path:
            session, execute_fnc = ssn_commands.get_option_hook_args(
                bsc_core.ArgDictStringOpt(
                    dict(
                        option_hook_key='actions/movie-open',
                        file=movie_file_path,
                        gui_group_name='movie',
                        gui_name='open movie'
                    )
                ).to_string()
            )

            movie_file_opt = bsc_storage.StgFileOpt(movie_file_path)
            name_dict['update'] = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                movie_file_opt.get_modify_timestamp(),
                language=1
            )
            name_dict['user'] = movie_file_opt.get_user()
            image_file_path, image_sp_cmd = bsc_storage.VdoFileOpt(movie_file_path).generate_thumbnail_create_args()
            image_args = image_file_path, image_sp_cmd, movie_file_path, execute_fnc
        else:
            name_dict['update'] = 'N/a'
            name_dict['user'] = 'N/a'

        self.__class__.CACHE[key] = image_args, name_dict
        return image_args, name_dict

    def __gui_built_fnc(self, rsv_task, prx_item_widget, data):
        image_args, name_dict = data
        #
        if image_args is not None:
            image_file_path, image_sp_cmd, movie_file_path, execute_fnc = image_args
            prx_item_widget.connect_press_db_clicked_to(execute_fnc)
            prx_item_widget.set_image(image_file_path)
            prx_item_widget.set_movie_enable(True)
            if image_sp_cmd is not None:
                prx_item_widget.set_image_show_args(image_file_path, image_sp_cmd)
        else:
            prx_item_widget.set_image(
                gui_core.GuiIcon.get('image_loading_failed')
            )
        #
        unit_menu_content = self.__generate_rsv_task_menu_content(rsv_task)
        if unit_menu_content:
            prx_item_widget.set_menu_content(unit_menu_content)

        prx_item_widget.set_name_dict(name_dict)
        prx_item_widget.refresh_widget_force()

    def __generate_rsv_task_menu_content(self, rsv_task):
        hook_keys = self._window._hook_configure.get(
            'actions.task_unit.hooks'
        ) or []
        #
        return self._window._get_menu_content_by_hook_keys_(
            self._window._session_dict, hook_keys, rsv_task, view_gui=self._window._task_prx_view
        )

    def get_current_rsv_task(self):
        _ = self._prx_list_view.get_selected_items()
        if _:
            return _[-1].get_gui_dcc_obj(self.DCC_NAMESPACE)


class _GuiGuideOpt(_GuiBaseOpt):
    def __init__(self, window, session, resolver, prx_guide_bar, prx_tree_view, prx_list_view):
        super(_GuiGuideOpt, self).__init__(window, session, resolver)

        self._prx_guide_bar = prx_guide_bar
        self._prx_tree_view = prx_tree_view
        self._prx_list_view = prx_list_view

        branch = self._window._rsv_filter_opt.get('branch')
        if branch == self._resolver.EntityTypes.Asset:
            self._types = [
                None,
                self._resolver.EntityTypes.Project,
                self._resolver.EntityTypes.Role,
                self._resolver.EntityTypes.Asset,
                self._resolver.EntityTypes.Step,
                self._resolver.EntityTypes.Task
            ]
        elif branch == self._resolver.EntityTypes.Shot:
            self._types = [
                None,
                self._resolver.EntityTypes.Project,
                self._resolver.EntityTypes.Sequence,
                self._resolver.EntityTypes.Shot,
                self._resolver.EntityTypes.Step,
                self._resolver.EntityTypes.Task
            ]
        else:
            raise RuntimeError()

        self._prx_guide_bar.set_dict(self._prx_tree_view._item_dict)
        self._prx_guide_bar.set_types(self._types)

    def gui_refresh(self):
        path = None
        list_item_prxes = self._prx_list_view.get_selected_items()
        # gain list first
        if list_item_prxes:
            list_item_prx = list_item_prxes[-1]
            path = list_item_prx.get_gui_attribute('path')
        else:
            tree_item_prxes = self._prx_tree_view.get_selected_items()
            if tree_item_prxes:
                tree_item_prx = tree_item_prxes[-1]
                path = tree_item_prx.get_gui_attribute('path')
        #
        if path is not None:
            for i in self._window._rsv_project_paths:
                if i not in self._prx_tree_view._item_dict:
                    self._prx_tree_view._item_dict[i] = None
            #
            self._prx_guide_bar.set_path(path)


class _GuiDirectoryOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxTreeViewAsDirectoryOpt
):
    ROOT_NAME = 'All'
    DCC_NAMESPACE = 'resolver'

    def __init__(self, window, session, resolver, prx_tree_view):
        super(_GuiDirectoryOpt, self).__init__(window, session, resolver)
        self._init_tree_view_as_directory_opt_(
            prx_tree_view, self.DCC_NAMESPACE
        )

        self._index_thread_batch = 0


class _GuiFileOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiPrxListViewAsFileOpt
):
    def __init__(self, window, session, resolver, prx_list_view):
        super(_GuiFileOpt, self).__init__(window, session, resolver)
        self._init_list_view_as_file_opt_(prx_list_view, self.DCC_NAMESPACE)
    
    def gui_add(self, file_opt):
        def cache_fnc_():
            def copy_path_fnc_():
                gui_qt_core.GuiQtUtil.copy_text_to_clipboard(file_path)

            def open_folder_fnc():
                bsc_storage.StgFileOpt(file_path).open_in_system()

            _location = file_opt.get_path()

            _menu_data = [
                (),
                ('Copy Path', 'copy', copy_path_fnc_),
                ('Open Folder', 'file/open-folder', open_folder_fnc)
            ]
            return [
                _location, _menu_data
            ]

        def build_fnc_(*args):
            _location, _menu_data = args[0]
            if file_opt.get_ext() in ['.jpg', '.png', '.exr', '.tx']:
                image_file_path, image_sp_cmd = bsc_storage.ImgOiioOptForThumbnail(file_path).generate_thumbnail_create_args(
                    width=128, ext='.jpg'
                )
                prx_item_widget.set_image(image_file_path)
                if image_sp_cmd is not None:
                    prx_item_widget.set_image_show_args(image_file_path, image_sp_cmd)
            else:
                file_icon = gui_qt_core.GuiQtDcc.get_qt_file_icon(file_path)
                if file_icon:
                    pixmap = file_icon.pixmap(80, 80)
                    prx_item_widget.set_image(
                        pixmap
                    )

            if _menu_data:
                prx_item_widget.set_menu_data(
                    _menu_data
                )

            prx_item_widget.set_tool_tip(
                _location
            )
            prx_item_widget.refresh_widget_force()

        path = file_path = file_opt.get_path()
        if self.gui_get_is_exists(path) is False:
            prx_item_widget = self._prx_list_view.create_item()

            self.gui_register(path, prx_item_widget)

            prx_item_widget.set_names([file_opt.get_name()])
            prx_item_widget.set_name_align_center_top()
            prx_item_widget.set_drag_enable(True)
            prx_item_widget.set_drag_urls([file_path])
            prx_item_widget.set_show_fnc(
                cache_fnc_, build_fnc_
            )
            prx_item_widget.set_gui_dcc_obj(
                file_opt, namespace=self.DCC_NAMESPACE
            )
            return prx_item_widget
        return self.gui_get(path)

    def gui_add_all(self, directory_opt):
        file_opts = directory_opt.get_files()
        if file_opts:
            for i_file_opt in file_opts:
                self.gui_add(i_file_opt)

    def gui_add_all_use_thread(self, directory_opt):
        def cache_fnc_():
            return [
                self._index_thread_batch,
                directory_opt.get_files()
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _file_opts = args[0]
            if _file_opts:
                for _i_file_opt in _file_opts:
                    if _index_thread_batch_current != self._index_thread_batch:
                        break
                    self.gui_add(_i_file_opt)

        def post_fnc_():
            pass

        self._index_thread_batch += 1

        t = gui_qt_core.QtBuildThread(self._prx_list_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


class _GuiUsdStageViewOpt(_GuiBaseOpt):
    CACHE = dict()

    def __init__(self, window, session, database_opt, usd_stage_view):
        super(_GuiUsdStageViewOpt, self).__init__(window, session, database_opt)
        self._usd_stage_view = usd_stage_view
        if gui_qt_usd_core.QT_USD_FLAG is True:
            self._usd_stage_view.get_usd_model().set_camera_light_enable(True)
        self._index_thread_batch = 1

    def gui_load_use_thread(self, rsv_task):
        def cache_fnc_():
            _rsv_unit = rsv_task.get_rsv_unit(keyword='{branch}-component-usd-file')
            _file_path = _rsv_unit.get_exists_result()
            self._usd_stage_view.load_usd_file(
                usd_file=_file_path,
            )
            return [self._index_thread_batch, None]

        def build_fnc_(*args):
            _index_thread_batch_current, _ = args[0]
            if _index_thread_batch_current != self._index_thread_batch:
                return
            self._usd_stage_view.refresh_usd_view_draw()

        def post_fnc_():
            pass

        self._index_thread_batch += 1

        self._usd_stage_view.run_as_thread(
            cache_fnc_,
            build_fnc_,
            post_fnc_
        )

    def gui_load(self, rsv_task):
        rsv_unit = rsv_task.get_rsv_unit(keyword='{branch}-component-usd-file')
        file_path = rsv_unit.get_exists_result()
        self._usd_stage_view.load_usd_file(
            usd_file=file_path
        )
        self._usd_stage_view.refresh_usd_view_draw()

    def restore(self):
        self._usd_stage_view.restore()


# noinspection PyUnusedLocal
class AbsPnlLoaderForRsvTask(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = 'resolver'
    ITEM_ICON_FRAME_SIZE = 20, 20
    ITEM_ICON_SIZE = 20, 20

    THREAD_STEP = 16

    LOADING_DELAY_TIME = 2000

    def set_all_setup(self):
        self._hook_configure = self._session.configure
        self._hook_gui_configure = self._session.gui_configure

        self._resolver = rsv_core.RsvBase.generate_root()

        self._rsv_filter = self._hook_configure.get('resolver.filter')
        #
        self._item_frame_size = self._hook_gui_configure.get('item_frame_size')

        self._session_dict = {}

        self.__asset_keys = set()
        self.__task_keys = set()

        v_qt_widget = qt_widgets.QtWidget()
        self.add_widget(v_qt_widget)
        v_qt_layout = qt_widgets.QtVBoxLayout(v_qt_widget)
        v_qt_layout.setContentsMargins(0, 0, 0, 0)
        # top
        self._top_tool_bar = prx_widgets.PrxHToolBar()
        v_qt_layout.addWidget(self._top_tool_bar._qt_widget)
        self._top_tool_bar.set_expanded(True)
        #   guide
        self._guide_tool_box = prx_widgets.PrxHToolBox()
        self._top_tool_bar.add_widget(self._guide_tool_box)
        self._guide_tool_box.set_expanded(True)
        self._guide_tool_box.set_size_mode(1)
        #
        self._task_guide_bar = prx_widgets.PrxGuideBar()
        self._guide_tool_box.add_widget(self._task_guide_bar)
        #
        h_qt_widget = qt_widgets.QtWidget()
        v_qt_layout.addWidget(h_qt_widget)
        h_qt_layout = qt_widgets.QtHBoxLayout(h_qt_widget)
        h_qt_layout.setContentsMargins(0, 0, 0, 0)
        #
        h_scroll_area = prx_widgets.PrxHScrollArea()
        h_qt_layout.addWidget(h_scroll_area._qt_widget)
        # main
        self._main_h_s = prx_widgets.PrxHSplitter()
        h_scroll_area.add_widget(self._main_h_s)
        self._main_h_s.install_full_size_shortcut()
        # left
        self._left_v_s = prx_widgets.PrxVSplitter()
        self._main_h_s.add_widget(self._left_v_s)
        #
        self.__gui_build_main()
        self.__setup_gui_options_()
        # right
        self._right_v_s = prx_widgets.PrxVSplitter()
        self._main_h_s.add_widget(self._right_v_s)
        # usd
        self._usd_stage_prx_view = prx_widgets.PrxUsdStageView()

        self._right_v_s.add_widget(self._usd_stage_prx_view)
        #
        directory_widget = qt_widgets.QtWidget()
        self._right_v_s.add_widget(directory_widget)
        directory_layout = qt_widgets.QtVBoxLayout(directory_widget)
        directory_layout.setContentsMargins(*[0]*4)
        directory_layout.setSpacing(2)

        self._qt_workspace_capsule = qt_widgets.QtInputAsCapsule()
        directory_layout.addWidget(self._qt_workspace_capsule)
        self._qt_workspace_capsule.input_value_changed.connect(
            self.__do_gui_refresh_for_directories
        )
        # directory tree view
        self._directory_prx_view = prx_widgets.PrxTreeView()
        directory_layout.addWidget(self._directory_prx_view.get_widget())
        self._directory_prx_view.set_header_view_create(
            [('directory', 1)]
        )
        self._directory_prx_view.connect_item_select_changed_to(
            self.__do_gui_refresh_for_files
        )
        # file
        self._file_prx_view = prx_widgets.PrxListView()
        self._right_v_s.add_widget(self._file_prx_view)
        self._file_frame_size = 80, 124
        self._item_name_frame_size = 80, 44
        self._file_prx_view.set_item_frame_size_basic(*self._file_frame_size)
        self._file_prx_view.set_item_name_frame_size(*self._item_name_frame_size)
        self._file_prx_view.set_item_icon_frame_draw_enable(False)
        self._file_prx_view.set_item_name_frame_draw_enable(False)
        self._file_prx_view.set_item_names_draw_range([None, 1])
        self._file_prx_view.set_item_image_frame_draw_enable(False)
        self._file_prx_view.set_selection_use_multiply()
        #
        self._left_v_s.set_fixed_size_at(1, 320)
        self._left_v_s.set_fixed_size_at(2, 60)
        #
        self._main_h_s.set_fixed_size_at(0, 320)
        self._main_h_s.set_fixed_size_at(2, 320)
        if bsc_core.SysApplicationMtd.get_is_dcc():
            self._main_h_s.set_contract_right_or_bottom_at(2)

        self._right_v_s.set_fixed_size_at(0, 320)

        self._gui_guide_opt = _GuiGuideOpt(
            self, self._session, self._resolver,
            self._task_guide_bar, self._entity_prx_view, self._task_prx_view
        )
        self._entity_prx_view.connect_item_select_changed_to(
            self._gui_guide_opt.gui_refresh
        )
        self._task_prx_view.connect_item_select_changed_to(
            self._gui_guide_opt.gui_refresh
        )

        self.refresh_all()

    def __gui_build_main(self):
        self._entity_prx_view = prx_widgets.PrxTreeView()
        self._left_v_s.add_widget(self._entity_prx_view)

        self._entity_prx_view.set_filter_entry_tip('fiter by resource ...')
        #
        self._tag_prx_view = prx_widgets.PrxTreeView()
        self._left_v_s.add_widget(self._tag_prx_view)
        self._tag_prx_view.connect_item_check_changed_to(
            self.__do_gui_refresh_for_resources_by_tag_checking
        )
        #
        self._task_prx_view = prx_widgets.PrxListView()
        self._main_h_s.add_widget(self._task_prx_view)

        self._options_prx_node = prx_widgets.PrxNode('options')
        self._left_v_s.add_widget(self._options_prx_node)
        #
        self._entity_prx_view.set_header_view_create(
            [('name', 3)],
            320-48
        )
        self._entity_prx_view.set_selection_use_single()
        #
        self._tag_prx_view.set_header_view_create(
            [('name', 3), ('count', 1)],
            320-48
        )
        self._tag_prx_view.view._set_selection_disable_()
        #
        self._entity_prx_view.connect_item_select_changed_to(
            self._do_gui_refresh_tasks_and_units_by_entity_selection
        )
        #
        self._task_prx_view.set_item_frame_size_basic(*self._item_frame_size)
        self._task_prx_view.get_check_tool_box().set_visible(True)
        self._task_prx_view.get_scale_switch_tool_box().set_visible(True)
        self._task_prx_view.get_sort_switch_tool_box().set_visible(True)
        #
        self._task_prx_view.set_item_icon_frame_size(*self.ITEM_ICON_FRAME_SIZE)
        self._task_prx_view.set_item_icon_size(*self.ITEM_ICON_SIZE)
        self._task_prx_view.set_item_icon_frame_draw_enable(True)
        self._task_prx_view.set_item_name_frame_draw_enable(True)
        self._task_prx_view.set_item_names_draw_range([None, 3])
        self._task_prx_view.set_item_image_frame_draw_enable(True)
        #
        self._task_prx_view.connect_refresh_action_for(self._do_gui_refresh_tasks_and_units_by_entity_selection)
        self._task_prx_view.connect_item_select_changed_to(
            self.__do_gui_refresh_for_usd_stage
        )
        self._task_prx_view.connect_item_select_changed_to(
            self.__do_gui_refresh_for_directories
        )
        #
        self._task_guide_bar.connect_user_text_choose_accepted_to(self.gui_tree_select_cbk_0)
        self._task_guide_bar.connect_user_text_press_accepted_to(self.gui_tree_select_cbk_1)

        self._entity_prx_view.set_completion_gain_fnc(
            self.__gui_rsv_entity_completion_gain_fnc_
        )
        self._tag_prx_view.set_completion_gain_fnc(
            self.__filter_completion_gain_fnc_
        )

        self._entity_prx_view.connect_refresh_action_for(
            self.refresh_all
        )

    def restore_variants(self):
        self.__running_threads_stacks = []
        self._index_thread_batch = 0
        self.__resource_count = 0

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlLoaderForRsvTask, self).__init__(session, *args, **kwargs)

    def refresh_all(self):
        if self._rsv_filters_dict:
            key = self._options_prx_node.get('filter')
            if key == 'auto':
                self._rsv_filter = self._get_resolver_application_filter_()
            else:
                self._rsv_filter = self._rsv_filters_dict[key]
            #
            self._rsv_filter_opt = bsc_core.ArgDictStringOpt(self._rsv_filter)

        self._gui_entity_opt = _GuiEntityOpt(
            self, self._session, self._resolver, self._entity_prx_view
        )

        self._gui_task_opt = _GuiTaskOpt(
            self, self._session, self._resolver, self._task_prx_view
        )
        self._gui_tag_opt = _GuiTagOpt(
            self, self._session, self._resolver, self._tag_prx_view
        )
        self._gui_directory_opt = _GuiDirectoryOpt(
            self, self._session, self._resolver, self._directory_prx_view
        )
        self._gui_file_opt = _GuiFileOpt(
            self, self._session, self._resolver, self._file_prx_view
        )
        self._gui_usd_stage_view_opt = _GuiUsdStageViewOpt(
            self, self._session, self._resolver, self._usd_stage_prx_view
        )

        self.gui_refresh_fnc()

    def gui_tree_select_cbk_0(self, text):
        if text is not None:
            self._entity_prx_view.select_item_by_key(
                text,
                exclusive=True
            )
            #
            if text in self._rsv_project_paths:
                self._rsv_project_name_cur = bsc_core.PthNodeOpt(text).get_name()
                self.refresh_all()

    def gui_tree_select_cbk_1(self, text):
        if text is not None:
            self._entity_prx_view.select_item_by_key(
                text,
                exclusive=True
            )

    def set_filter_update(self):
        self._task_prx_view.set_visible_tgt_raw_update()

    def set_filter_refresh(self):
        pass

    def gui_refresh_fnc(self):
        project = self._rsv_project_name_cur
        self._rsv_project = self._resolver.get_rsv_project(project=project)
        if self._rsv_project is not None:
            gui_core.GuiHistory.append(
                'gui.projects',
                project
            )
        #
        self._rsv_project.restore_all_gui_variants()

        self._entity_prx_view.set_filter_history_key(
            'filter.{}-{}-entity'.format(self._session.name, project)
        )

        workspace_keys = self._rsv_project.WorkspaceKeys.All
        self._qt_workspace_capsule._set_value_options_(workspace_keys)
        #
        self._entity_prx_view.restore_filter()
        self._gui_entity_opt.restore()
        self._gui_tag_opt.restore()
        self._task_guide_bar.set_clear()
        #
        self.__asset_keys = set()
        self.__task_keys = set()
        #
        is_create, prx_item = self._gui_entity_opt.gui_add_root()
        if is_create is True:
            prx_item.set_selected(True)
            self._gui_entity_opt.gui_add_project(self._rsv_project)

            if self._qt_thread_enable is True:
                self._gui_tag_opt.gui_add_all_groups_use_thread(self._rsv_project)
            else:
                self._gui_tag_opt.gui_add_all_groups(self._rsv_project)

    def __gui_rsv_entity_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = fnmatch.filter(
                self._gui_entity_opt.get_completion_keys(), '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:50]
        return []

    def __setup_gui_options_(self):
        self._available_rsv_show_args = self._get_available_rsv_show_args_()
        self._rsv_filter_opt = bsc_core.ArgDictStringOpt(self._rsv_filter)
        self._project_name_from_filter = self._rsv_filter_opt.get('project')
        #
        self._rsv_projects = self._resolver.get_rsv_projects()
        self._rsv_project_paths = [i.get_path() for i in self._rsv_projects]
        self._rsv_project_names = [i.get_name() for i in self._rsv_projects]
        #
        _port = self._options_prx_node.add_port(
            prx_widgets.PrxPortAsConstantChoose('filter')
        )
        self._rsv_filters_dict = self._hook_configure.get('resolver.filters')
        if self._rsv_filters_dict is not None:
            _port.set(
                self._rsv_filters_dict.keys()
            )
        #
        current_project = self._get_current_project_()
        if current_project:
            if current_project in self._rsv_project_names:
                self._rsv_project_names.remove(current_project)
            #
            self._rsv_project_names.append(current_project)
        #
        gui_core.GuiHistory.extend(
            'gui.projects',
            self._rsv_project_names
        )
        self._rsv_project_name_cur = self._rsv_project_names[0]
        if self._project_name_from_filter is not None:
            if self._project_name_from_filter in self._rsv_project_names:
                self._rsv_project_name_cur = self._project_name_from_filter
        else:
            project_name_from_history = gui_core.GuiHistory.get_latest(
                'gui.projects'
            )
            if project_name_from_history is not None:
                if project_name_from_history in self._rsv_project_names:
                    self._rsv_project_name_cur = project_name_from_history

    def __filter_completion_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = fnmatch.filter(
                self.__task_keys, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)
        return []

    def __restore_thread_stack_(self):
        if self.__running_threads_stacks:
            [i.do_kill() for i in self.__running_threads_stacks]
        #
        self.__running_threads_stacks = []

    # refresh tasks by resource
    def _do_gui_refresh_for_tasks_by_resource_expand_changed(self, rsv_resource):
        def post_fnc_():
            rsv_resource.get_obj_gui().set_loading_end()
            #
            self.set_filter_update()

        def quit_fnc_():
            t.do_quit()

        #
        t = gui_qt_core.QtBuildThread(self.widget)
        t.set_cache_fnc(
            functools.partial(self.__gui_cache_fnc_for_tasks_by_resource_, rsv_resource)
        )
        t.cache_value_accepted.connect(self.__gui_build_fnc_for_tasks_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()

        self.connect_window_close_to(quit_fnc_)

    def __gui_cache_fnc_for_tasks_by_resource_(self, rsv_resource):
        return rsv_resource.get_rsv_tasks(**self._rsv_filter_opt.value)

    def __gui_build_fnc_for_tasks_(self, rsv_tasks):
        for i_rsv_task in rsv_tasks:
            self._gui_entity_opt.gui_add_task(i_rsv_task)

            self.__task_keys.add(i_rsv_task.name)

    def _do_gui_refresh_tasks_and_units_by_entity_selection(self):
        tree_item_prxes = self._entity_prx_view.get_selected_items()
        # kill running
        self.__restore_thread_stack_()

        self._index_thread_batch += 1

        self._start_timestamp = bsc_core.SysBaseMtd.get_timestamp()

        self._gui_task_opt.restore()
        self._gui_tag_opt.reset()
        if tree_item_prxes:
            tree_item_prx = tree_item_prxes[-1]
            rsv_entity = tree_item_prx.get_gui_dcc_obj(self.DCC_NAMESPACE)
            if rsv_entity is not None:
                obj_type_name = rsv_entity.type_name
                if obj_type_name in [
                    'role', 'sequence',
                    'asset', 'shot',
                    'step',
                    'task'
                ]:
                    self.__batch_add_tasks_and_units_by_entities_([rsv_entity], self._index_thread_batch)

    # refresh task unit by any entity
    # todo: thread bug in katana
    def __batch_add_tasks_and_units_by_entities_(self, rsv_entities, thread_stack_index):
        def post_fnc_():
            pass

        def quit_fnc_():
            ts.do_quit()

        rsv_entities_map = bsc_core.RawListMtd.grid_to(
            rsv_entities, self.THREAD_STEP
        )
        #
        if self._qt_thread_enable is True:
            ts = gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_rsv_entities in rsv_entities_map:
                ts.register(
                    functools.partial(
                        self.__batch_gui_cache_fnc_for_tasks_and_units_by_entities_, i_rsv_entities, thread_stack_index
                        ),
                    self.__batch_gui_build_fnc_for_tasks_and_units_
                )
            #
            ts.set_start()
            #
            self.connect_window_close_to(quit_fnc_)
        else:
            for i_rsv_entities in rsv_entities_map:
                self.__batch_gui_build_fnc_for_tasks_and_units_(
                    self.__batch_gui_cache_fnc_for_tasks_and_units_by_entities_(i_rsv_entities, thread_stack_index)
                )

    def __batch_gui_cache_fnc_for_tasks_and_units_by_entities_(self, rsv_entities, thread_stack_index):
        if rsv_entities:
            type_name = rsv_entities[0].type_name
            if type_name in [
                'role', 'sequence',
            ]:
                return [
                    [j for i in rsv_entities for j in i.get_rsv_resources(**self._rsv_filter_opt.value)],
                    thread_stack_index
                ]
            else:
                return [
                    rsv_entities,
                    thread_stack_index
                ]

    def __batch_gui_build_fnc_for_tasks_and_units_(self, *args):
        def post_fnc_():
            # update for filter
            self.set_filter_update()

        def quit_fnc_():
            ts.do_quit()

        rsv_entities, thread_stack_index = args[0]
        rsv_entities_map = bsc_core.RawListMtd.grid_to(
            rsv_entities, self.THREAD_STEP
        )

        if self._qt_thread_enable is True:
            ts = gui_qt_core.QtBuildThreadStack(self.widget)
            self.__running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_rsv_entities in rsv_entities_map:
                ts.register(
                    functools.partial(
                        self.__gui_cache_fnc_for_tasks_and_units_by_entities_, i_rsv_entities, thread_stack_index
                        ),
                    self.__gui_build_fnc_for_tasks_and_units_
                )
            #
            ts.set_start()
            #
            self.connect_window_close_to(quit_fnc_)
        else:
            with bsc_log.LogProcessContext.create(
                maximum=len(rsv_entities_map), label='gui-add for task unit'
            ) as g_p:
                for i_rsv_entities in rsv_entities_map:
                    g_p.do_update()
                    self.__gui_build_fnc_for_tasks_and_units_(
                        self.__gui_cache_fnc_for_tasks_and_units_by_entities_(i_rsv_entities, thread_stack_index)
                    )

    def __gui_cache_fnc_for_tasks_and_units_by_entities_(self, rsv_entities, thread_stack_index):
        if rsv_entities:
            if rsv_entities[0].type_name == 'task':
                return [
                    rsv_entities,
                    thread_stack_index
                ]
            else:
                return [
                    [j for i in rsv_entities for j in i.get_rsv_tasks(**self._rsv_filter_opt.value)],
                    thread_stack_index
                ]

    def __gui_build_fnc_for_tasks_and_units_(self, *args):
        rsv_tasks, thread_stack_index = args[0]
        # print rsv_tasks
        with self.gui_bustling():
            for i_rsv_task in rsv_tasks:
                if thread_stack_index != self._index_thread_batch:
                    break
                i_task = i_rsv_task.get('task')

                self._gui_entity_opt.gui_add_task(i_rsv_task)
                self._gui_task_opt.gui_add_one(i_rsv_task)
                self.__task_keys.add(i_task)

    def _get_available_rsv_show_args_(self):
        list_ = []
        keywords_args = self._hook_configure.get('resolver.task_unit.keywords') or []
        for i_arg in keywords_args:
            if isinstance(i_arg, six.string_types):
                i_keyword = i_arg
                list_.append((i_keyword, True))
            elif isinstance(i_arg, dict):
                for j_keyword, j_raw in i_arg.items():
                    j_hidden = j_raw.get('hidden') or False
                    j_system_keys = j_raw.get('systems') or []
                    if j_system_keys:
                        if bsc_core.SysBaseMtd.get_is_matched(j_system_keys):
                            list_.append((j_keyword, j_hidden))
                    else:
                        list_.append((j_keyword, j_hidden))
        return list_

    @classmethod
    def _get_current_application_(cls):
        return bsc_core.SysApplicationMtd.get_current()

    @classmethod
    def _get_current_project_(cls):
        return bsc_etr_methods.EtrBase.get_project()

    def _get_resolver_application_filter_(self):
        _ = self._hook_configure.get('resolver.application_filter') or {}
        for k, v in _.items():
            if bsc_core.SysBaseMtd.get_is_matched(['*-{}'.format(k)]):
                return v
        return self._hook_configure.get('resolver.filter')

    @classmethod
    def _get_menu_content_by_hook_keys_(cls, session_dict, hooks, *args, **kwargs):
        content = ctt_core.Dict()
        for i_hook in hooks:
            if isinstance(i_hook, six.string_types):
                i_hook_key = i_hook
                i_hook_option = None
            elif isinstance(i_hook, dict):
                i_hook_key = i_hook.keys()[0]
                i_hook_option = i_hook.values()[0]
            else:
                raise RuntimeError()
            #
            i_args = cls._get_rsv_unit_action_hook_args_(
                session_dict, i_hook_key, *args, **kwargs
            )
            if i_args:
                i_session, i_execute_fnc = i_args
                if i_session.get_is_loadable() is True and i_session.get_is_visible() is True:
                    i_gui_configure = i_session.gui_configure
                    #
                    i_gui_parent_path = '/'
                    #
                    i_gui_name = i_gui_configure.get('name')
                    if i_hook_option:
                        if 'gui_name' in i_hook_option:
                            i_gui_name = i_hook_option.get('gui_name')
                        #
                        if 'gui_parent' in i_hook_option:
                            i_gui_parent_path = i_hook_option['gui_parent']
                    #
                    i_gui_parent_path_opt = bsc_core.PthNodeOpt(i_gui_parent_path)
                    #
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_path = '/{}'.format(i_gui_name)
                    else:
                        i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                    #
                    i_gui_separator_name = i_gui_configure.get('group_name')
                    if i_gui_separator_name:
                        if i_gui_parent_path_opt.get_is_root():
                            i_gui_separator_path = '/{}'.format(i_gui_separator_name)
                        else:
                            i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_separator_name)
                        #
                        content.set(
                            '{}.properties.type'.format(i_gui_separator_path), 'separator'
                        )
                        content.set(
                            '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                        )
                    #
                    content.set(
                        '{}.properties.type'.format(i_gui_path), 'action'
                    )
                    content.set(
                        '{}.properties.group_name'.format(i_gui_path), i_gui_configure.get('group_name')
                    )
                    content.set(
                        '{}.properties.name'.format(i_gui_path), i_gui_name
                    )
                    content.set(
                        '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                    )
                    if i_hook_option:
                        if 'gui_icon_name' in i_hook_option:
                            content.set(
                                '{}.properties.icon_name'.format(i_gui_path), i_hook_option.get('gui_icon_name')
                            )
                        if 'gui_sub_icon_name' in i_hook_option:
                            content.set(
                                '{}.properties.sub_icon_name'.format(i_gui_path), i_hook_option.get('gui_sub_icon_name')
                            )
                    #
                    content.set(
                        '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                    )
                    content.set(
                        '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                    )
        return content

    @staticmethod
    def _get_rsv_unit_action_hook_args_(session_dict, key, *args, **kwargs):
        def execute_fnc():
            session.execute_python_file(python_file_path, session=session)

        #
        rsv_task = args[0]
        session_path = '{}/{}'.format(rsv_task.path, key)
        if session_path in session_dict:
            return session_dict[session_path]
        else:
            python_file_path = ssn_core.SsnHookFileMtd.get_python(key)
            yaml_file_path = ssn_core.SsnHookFileMtd.get_yaml(key)
            if python_file_path and yaml_file_path:
                python_file = bsc_storage.StgFileOpt(python_file_path)
                yaml_file = bsc_storage.StgFileOpt(yaml_file_path)
                if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
                    configure = ctt_core.Content(value=yaml_file.path)
                    type_name = configure.get('option.type')
                    if type_name is not None:
                        kwargs['configure'] = configure
                        #
                        if type_name in ['asset', 'shot', 'step', 'task']:
                            session = ssn_objects.RsvActionSession(
                                *args,
                                **kwargs
                            )
                        elif type_name in ['unit']:
                            session = ssn_objects.RsvUnitActionSession(
                                *args,
                                **kwargs
                            )
                            if 'view_gui' in kwargs:
                                session.set_view_gui(
                                    kwargs['view_gui']
                                )
                        else:
                            raise TypeError()
                        #
                        session_dict[session_path] = session, execute_fnc
                        return session, execute_fnc

    def __do_gui_refresh_for_resources_by_tag_checking(self):
        tag_filter_data_src = self._gui_tag_opt.generate_tag_filter_data_src()
        qt_view = self._task_prx_view._qt_view
        qt_view._set_view_tag_filter_data_src_(tag_filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._task_prx_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

    def __do_gui_refresh_for_usd_stage(self):
        if gui_qt_usd_core.QT_USD_FLAG is True:
            self._gui_usd_stage_view_opt.restore()
            if (
                self._main_h_s.get_is_contracted_at(2) is False
                and self._right_v_s.get_is_contracted_at(1) is False
            ):
                rsv_task = self._gui_task_opt.get_current_obj()
                if rsv_task is not None:
                    self.__gui_refresh_usd_stage(rsv_task)

    def __gui_refresh_usd_stage(self, rsv_task):
        if self._qt_thread_enable is True:
            self._gui_usd_stage_view_opt.gui_load_use_thread(rsv_task)
        else:
            self._gui_usd_stage_view_opt.gui_load(rsv_task)

    def __do_gui_refresh_for_directories(self):
        self._gui_directory_opt.restore()
        self._gui_file_opt.restore()
        if (
            self._main_h_s.get_is_contracted_at(2) is False
            and self._right_v_s.get_is_contracted_at(1) is False
        ):
            workspace_key = self._qt_workspace_capsule._get_value_()
            rsv_task = self._gui_task_opt.get_current_obj()
            if rsv_task is not None:
                if workspace_key == self._rsv_project.WorkspaceKeys.User:
                    variant_extend = dict(artist=bsc_core.SysBaseMtd.get_user_name())
                else:
                    variant_extend = dict()

                rsv_unit = rsv_task.get_rsv_unit(
                    keyword='{{branch}}-{}-task-dir'.format(workspace_key)
                )
                directory_path = rsv_unit.get_exists_result(version='latest', variants_extend=variant_extend)
                if directory_path is not None:
                    if self._qt_thread_enable is True:
                        self._gui_directory_opt.gui_add_all_use_thread(directory_path)
                    else:
                        self._gui_directory_opt.gui_add_all(directory_path)

    def __do_gui_refresh_for_files(self):
        self._gui_file_opt.restore()
        if (
            self._main_h_s.get_is_contracted_at(2) is False
            and self._right_v_s.get_is_contracted_at(2) is False
        ):
            directory_opt = self._gui_directory_opt.get_current_obj()
            if directory_opt is not None:
                if self._qt_thread_enable is True:
                    self._gui_file_opt.gui_add_all_use_thread(directory_opt)
                else:
                    self._gui_file_opt.gui_add_all(directory_opt)
