# coding:utf-8
from __future__ import print_function

import six

import os

import collections

import time

import functools
# basic
import lxbasic.log as bsc_log

import lxbasic.scan as bsc_scan

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts


class PnlTextureConverter(gui_prx_widgets.PrxSessionWindow):
    NAMESPACE = 'storage'

    @classmethod
    def do_startup(cls):
        import lxgeneral.dcc.core as gnl_dcc_core

        # gnl_dcc_core.OcioSetup(
        #     bsc_storage.StgPathMapper.map_to_current(
        #         '/l/packages/pg/third_party/ocio/aces/1.2'
        #     )
        # ).set_run()

        # import lxarnold.startup as and_startup
        # and_startup.MtoaSetup(
        #     bsc_storage.StgPathMapper.map_to_current(
        #         '/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019'
        #     )
        # ).set_run()

    def __init__(self, session, *args, **kwargs):
        super(PnlTextureConverter, self).__init__(session, *args, **kwargs)

    def gui_setup_fnc(self):
        s_0 = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(s_0)
        h_s = gui_prx_widgets.PrxHSplitter()
        h_s.install_full_size_shortcut()
        s_0.add_widget(h_s)
        #
        self._gui_data = []
        self._target_format_create_data = []
        self._target_color_space_create_data = []
        #
        s_1 = gui_prx_widgets.PrxVScrollArea()
        h_s.add_widget(s_1)
        self._options_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        s_1.add_widget(self._options_prx_node)
        self._options_prx_node.build_by_data(
            self._session.configure.get('build.node.options'),
        )
        #
        self._tree_view = gui_prx_widgets.PrxTreeView()
        h_s.add_widget(self._tree_view)
        self._tree_view.create_header_view(
            [('name', 4), ('color-space', 1), ('description', 1)],
            self.get_definition_window_size()[0]/2-32
        )
        self._tree_view_add_opt = gui_prx_scripts.GuiPrxScpForStorageTreeAdd(
            self._tree_view,
            prx_tree_item_cls=gui_prx_widgets.PrxStgObjTreeItem,
        )
        #
        h_s.set_fixed_size_at(0, 480)
        #
        self._options_prx_node.set(
            'match_pattern', '*.<udim>.####.{format}, *.<udim>.{format}, *.{format}'
        )
        self._options_prx_node.set_default(
            'match_pattern', '*.<udim>.####.{format}, *.<udim>.{format}, *.{format}'
        )
        self._options_prx_node.set(
            'by_format.execute', self.execute_create_by_format
        )
        #
        self._options_prx_node.set(
            'by_format.create_use_deadline', self.set_target_format_use_deadline_run
        )
        #
        self._options_prx_node.get_port('by_format.execute').connect_finished_to(
            self._set_gui_textures_validator_
        )
        #
        self._options_prx_node.set(
            'by_color_space.execute', self.execute_create_by_color_space
        )
        #
        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )
        self._tree_view.connect_refresh_action_for(
            self.refresh_gui_fnc
        )

        self._refresh_button = gui_prx_widgets.PrxPressButton()
        self.add_button(self._refresh_button)
        self._refresh_button.set_name('refresh')
        self._refresh_button.connect_press_clicked_to(self.refresh_gui_fnc)

    @classmethod
    def _set_file_args_update_0_(cls, file_dict, file_opt, include_patterns, ext_includes):
        name_patterns_ = []
        for i_name_pattern in include_patterns:
            if i_name_pattern.endswith('{format}'):
                for j_ext in ext_includes:
                    j_name_pattern = i_name_pattern.replace('.{format}', j_ext)
                    name_patterns_.append(j_name_pattern)
            else:
                name_patterns_.append(i_name_pattern)
        #
        for i_name_pattern_ in name_patterns_:
            i_enable = cls._set_file_args_update_1_(file_dict, file_opt, i_name_pattern_)
            if i_enable is True:
                break

    @classmethod
    def _set_file_args_update_1_(cls, file_dict, file_opt, name_pattern):
        if bsc_core.BscFileTiles.is_valid(name_pattern):
            match_args = bsc_storage.StgFileTiles.get_number_args(
                file_opt.name, name_pattern
            )
            if match_args:
                file_name_, numbers = match_args
                #
                file_path_ = '{}/{}'.format(file_opt.directory_path, file_name_)
                file_dict.setdefault(
                    file_path_, []
                ).append(file_opt.path)
                return True
        else:
            if file_opt.is_name_match_pattern(name_pattern):
                file_dict.setdefault(
                    file_opt.path, []
                ).append(file_opt.path)
                return True
        return False

    @classmethod
    def _get_directory_paths_(cls, directory_path, recursion_enable):
        if directory_path:
            lis = [directory_path]
            if recursion_enable is True:
                lis.extend(
                    bsc_scan.ScanBase.get_all_directory_paths(directory_path)
                )
            return lis
        return []

    def refresh_gui_fnc(self):
        def post_fnc_():
            pass

        directory_path = self._options_prx_node.get('directory')
        recursion_enable = self._options_prx_node.get('recursion_enable')
        output_directory_path = self._options_prx_node.get('by_format.directory')
        match_patterns = self._options_prx_node.get('match_pattern')
        match_formats = self._options_prx_node.get('match_format')

        ext_includes = map(lambda x: '.'+x, map(lambda x: x.rstrip().lstrip(), match_formats.split(',')))
        include_patterns = map(lambda x: x.rstrip().lstrip(), match_patterns.split(','))

        directory_paths = self._get_directory_paths_(directory_path, recursion_enable)
        self._tree_view_add_opt.restore_all()

        if directory_paths:
            ts = gui_qt_core.QtBuildThreadStack(self.widget)
            ts.run_finished.connect(post_fnc_)
            for i_directory_path in directory_paths:
                ts.register(
                    functools.partial(
                        self.__gui_cache_files,
                        i_directory_path,
                        include_patterns,
                        ext_includes
                    ),
                    self.__gui_add_files
                )
            ts.do_start()

    def __gui_cache_files(self, directory_path, include_patterns, ext_includes):
        file_paths = bsc_storage.StgDirectory.get_file_paths(directory_path, ext_includes)
        dict_ = collections.OrderedDict()
        for i_file_path in file_paths:
            i_file_opt = bsc_storage.StgFileOpt(i_file_path)
            self._set_file_args_update_0_(
                dict_, i_file_opt, include_patterns, ext_includes
            )
        return dict_.keys()

    def __gui_add_files(self, file_paths):
        import lxgeneral.dcc.objects as gnl_dcc_objects

        for i_k in file_paths:
            i_texture_src = gnl_dcc_objects.StgTexture(i_k)

            i_is_create, i_prx_item = self._tree_view_add_opt.gui_add_as(
                i_texture_src,
                mode='list',
                use_show_thread=True
            )
            if i_is_create is True:
                i_prx_item.connect_press_dbl_clicked_to(
                    self._show_image_detail
                )

        self._set_gui_textures_validator_()

    def _set_gui_textures_validator_(self):
        ext_tgt = self._options_prx_node.get('by_format.extension')
        directory_path_tgt = self._options_prx_node.get('by_format.directory')

        for k, v in self._tree_view._item_dict.items():
            i_prx_item = v
            i_texture_src = i_prx_item.get_gui_dcc_obj(namespace='storage-file')
            # check is assign
            if i_texture_src is not None:
                i_texture_tgt = i_texture_src.get_as_tgt_ext(
                    ext_tgt,
                    directory_path_tgt
                )
                #
                i_descriptions = []
                if i_texture_tgt.get_is_exists() is False:
                    i_descriptions.append(
                        '"{}" is non-exists'.format(ext_tgt)
                    )
                else:
                    if i_texture_src.get_is_exists_as_tgt_ext(
                            ext_tgt,
                            directory_path_tgt
                    ) is False:
                        i_descriptions.append(
                            '"{}" need update'.format(ext_tgt)
                        )

                i_prx_item.set_name(
                    ', '.join(i_descriptions), 2
                )
                if i_descriptions:
                    i_prx_item.set_status(
                        i_prx_item.ValidationStatus.Warning, 2
                    )
                else:
                    i_prx_item.set_status(
                        i_prx_item.ValidationStatus.Normal, 2
                    )

                i_color_space = i_texture_src.get_best_color_space()
                i_prx_item.set_name(i_color_space, 1)

    # to target format
    def format_gain_fnc(self, ext_tgt, directory_path_tgt, force_enable):
        self._target_format_create_data = []

        contents = []
        textures = self._tree_view_add_opt.get_checked_files()
        if textures:
            with bsc_log.LogProcessContext.create(maximum=len(textures), label='gain texture create-data') as g_p:
                for i_texture_src in textures:
                    g_p.do_update()
                    #
                    i_texture_tgt = i_texture_src.__class__(
                        six.u('{}/{}{}').format(
                            directory_path_tgt, i_texture_src.name_base, ext_tgt
                        )
                    )
                    if i_texture_src.path == i_texture_tgt.path:
                        continue
                    #
                    i_directory_path_tgt = i_texture_tgt.directory.path
                    #
                    i_texture_units_src = i_texture_src.get_exists_units()
                    for j_texture_unit_src in i_texture_units_src:
                        if force_enable is True:
                            self._target_format_create_data.append(
                                (j_texture_unit_src.path, i_directory_path_tgt)
                            )
                        else:
                            if j_texture_unit_src.get_is_exists_as_tgt_ext(
                                    ext_tgt,
                                    i_directory_path_tgt
                            ) is False:
                                self._target_format_create_data.append(
                                    (j_texture_unit_src.path, i_directory_path_tgt)
                                )
        else:
            contents = [
                'non-texture(s) to execute, you can click "refresh" or enter a new "directory" and click "refresh"'
            ]
        #
        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False
        else:
            return True

    def format_create_fnc(self, button, ext_tgt, width, copy_same_ext):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            print('\n'.join(results))

        def status_update_at_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            import lxgeneral.dcc.objects as gnl_dcc_objects

            for i_index, (i_file_path_src, i_directory_path_tgt) in enumerate(self._target_format_create_data):
                bsc_storage.StgPath.create_directory(
                    i_directory_path_tgt
                )
                i_path_base, i_ext_src = os.path.splitext(i_file_path_src)
                i_cmd = gnl_dcc_objects.StgTexture._get_unit_create_cmd_as_ext_tgt_by_src_force_(
                    i_file_path_src,
                    ext_tgt=ext_tgt,
                    search_directory_path=i_directory_path_tgt,
                    width=width
                )
                if button.get_is_stopped():
                    break
                #
                if i_cmd:
                    bsc_core.TrdCommandPool.do_pool_wait()
                    #
                    i_t = bsc_core.TrdCommandPool.set_start(i_cmd, i_index)
                    i_t.status_changed.connect_to(status_update_at_fnc_)
                    i_t.finished.connect_to(finished_fnc_)
                else:
                    status_update_at_fnc_(
                        i_index, button.Status.Completed
                    )
                    finished_fnc_(
                        i_index, button.Status.Completed, ['error']
                    )
                    if i_ext_src == ext_tgt:
                        # when ext is same do copy
                        if copy_same_ext is True:
                            bsc_storage.StgFileOpt(
                                i_file_path_src
                            ).copy_to_directory(i_directory_path_tgt)

        def quit_fnc_():
            button.set_stopped()
            #
            time.sleep(1)
            #
            t.quit()
            t.wait()
            t.deleteLater()

        contents = []
        if self._target_format_create_data:
            button.set_stopped(False)

            c = len(self._target_format_create_data)

            button.set_status(button.Status.Started)
            button.initialization(c, button.Status.Started)

            t = gui_qt_core.QtMethodThread(self.widget)
            t.append_method(
                run_fnc_
            )
            t.start()
            self.register_window_close_method(quit_fnc_)
        else:
            button.restore_all()

            contents = [
                'non-texture(s) to execute, you can checked "force enable" or enter a new "output directory"'
            ]

        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False
        else:
            return True

    @gui_core.GuiModifier.run_with_exception_catch
    def execute_create_by_format(self):
        ext_tgt = self._options_prx_node.get('by_format.extension')
        width = self._options_prx_node.get('by_format.width')
        directory_path_tgt = self._options_prx_node.get('by_format.directory')
        copy_same_ext = self._options_prx_node.get('by_format.copy_same_ext')
        force_enable = self._options_prx_node.get('by_format.force_enable')
        button = self._options_prx_node.get_port('by_format.execute')
        #
        if width == 'keep-original':
            width = None
        else:
            width = int(width)

        method_args = [
            (self.format_gain_fnc, (ext_tgt, directory_path_tgt, force_enable)),
            (self.format_create_fnc, (button, ext_tgt, width, copy_same_ext))
        ]
        with bsc_log.LogProcessContext.create(maximum=len(method_args), label='create texture by data') as g_p:
            for i_fnc, i_args in method_args:
                g_p.do_update()
                i_result = i_fnc(*i_args)
                if i_result is False:
                    break

    def set_target_format_use_deadline_run(self):
        import lxsession.commands as ssn_commands

        directory_path = self._options_prx_node.get('directory')
        ext_tgt = self._options_prx_node.get('by_format.extension')
        width = self._options_prx_node.get('by_format.width')
        directory_path_tgt = self._options_prx_node.get('by_format.directory')
        #
        if width == 'keep-original':
            width = None

        j_option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key='methods/texture/texture-convert',
                directory=directory_path,
                output_directory=directory_path_tgt,
                target_ext=ext_tgt,
                width=width,
                #
                td_enable=self._session.get_devlop_flag(),
                test_flag=self._session.get_test_flag(),
            )
        )
        #
        session = ssn_commands.execute_option_hook_by_deadline(
            option=j_option_opt.to_string()
        )
        ddl_job_id = session.get_ddl_job_id()

        gui_core.GuiMonitorForDeadline.set_create(
            session.gui_name, ddl_job_id
        )

    # to target color-space
    def color_space_gain_fnc(self, ext_tgt, directory_path_tgt, force_enable):
        self._target_color_space_create_data = []

        contents = []
        textures = self._tree_view_add_opt.get_checked_files()
        if textures:
            with bsc_log.LogProcessContext.create(maximum=len(textures), label='gain texture create-data') as g_p:
                for i_texture_src in textures:
                    g_p.do_update()
                    #
                    i_texture_tgt = i_texture_src.__class__(
                        '{}/{}{}'.format(
                            directory_path_tgt, bsc_core.ensure_string(i_texture_src.name_base), ext_tgt
                        )
                    )
                    if i_texture_src.path == i_texture_tgt.path:
                        continue
                    #
                    i_texture_units_src = i_texture_src.get_exists_units()
                    #
                    i_color_space_src = i_texture_src.get_best_color_space()
                    i_color_space_tgt = i_texture_src.get_method_for_color_space_as_aces().get_default_color_space()
                    for j_texture_unit_src in i_texture_units_src:
                        j_texture_unit_tgt = j_texture_unit_src.set_directory_repath_to(
                            directory_path_tgt
                        )
                        j_texture_unit_tgt = j_texture_unit_tgt.set_ext_rename_to(
                            ext_tgt
                        )
                        self._target_color_space_create_data.append(
                            (j_texture_unit_src.path, j_texture_unit_tgt.path, i_color_space_src, i_color_space_tgt)
                        )
        else:
            contents = [
                'non-texture(s) to execute, you can click "match" or enter a new "directory" and click "match"'
            ]
        #
        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False
        else:
            return True

    def color_space_create_fnc(self, button, ext_tgt, copy_same_ext):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            print('\n'.join(results))

        def status_update_at_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            import lxarnold.core as and_core

            for i_index, (i_file_path_src, i_directory_path_tgt, i_color_space_src, i_color_space_tgt) in enumerate(
                    self._target_color_space_create_data
                    ):
                bsc_storage.StgFileOpt(i_directory_path_tgt).create_directory()
                #
                i_path_base, i_ext_src = os.path.splitext(i_file_path_src)
                i_cmd = and_core.AndTextureOpt.generate_format_convert_as_aces_command(
                    i_file_path_src, i_directory_path_tgt, i_color_space_src, i_color_space_tgt
                )
                if button.get_is_stopped():
                    break
                #
                if i_cmd:
                    bsc_core.TrdCommandPool.do_pool_wait()
                    #
                    i_t = bsc_core.TrdCommandPool.set_start(i_cmd, i_index)
                    i_t.status_changed.connect_to(status_update_at_fnc_)
                    i_t.finished.connect_to(finished_fnc_)
                else:
                    status_update_at_fnc_(
                        i_index, button.Status.Completed
                    )
                    finished_fnc_(
                        i_index, button.Status.Completed, ['error']
                    )
                    if i_ext_src == ext_tgt:
                        # when ext is same do copy
                        if copy_same_ext is True:
                            bsc_storage.StgFileOpt(
                                i_file_path_src
                            ).copy_to_directory(i_directory_path_tgt)

        def quit_fnc_():
            button.set_stopped()
            #
            time.sleep(1)
            #
            t.quit()
            t.wait()
            t.deleteLater()

        contents = []
        if self._target_color_space_create_data:
            button.set_stopped(False)

            c = len(self._target_color_space_create_data)

            button.set_status(button.Status.Started)
            button.initialization(c, button.Status.Started)

            t = gui_qt_core.QtMethodThread(self.widget)
            t.append_method(
                run_fnc_
            )
            t.start()
            self.register_window_close_method(quit_fnc_)
        else:
            button.restore_all()

            contents = [
                'non-texture(s) to execute, you can checked "force enable" or enter a new "output directory"'
            ]

        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False
        else:
            return True

    @gui_core.GuiModifier.run_with_exception_catch
    def execute_create_by_color_space(self):
        directory_path_tgt = self._options_prx_node.get('by_color_space.directory')
        ext_tgt = self._options_prx_node.get('by_color_space.extension')
        copy_same_ext = self._options_prx_node.get('by_color_space.copy_same_ext')
        force_enable = True

        button = self._options_prx_node.get_port('by_color_space.execute')

        method_args = [
            (self.color_space_gain_fnc, (ext_tgt, directory_path_tgt, force_enable)),
            (self.color_space_create_fnc, (button, ext_tgt, copy_same_ext))
        ]
        with bsc_log.LogProcessContext.create(maximum=len(method_args), label='create texture by data') as g_p:
            for i_fnc, i_args in method_args:
                g_p.do_update()
                i_result = i_fnc(*i_args)
                if i_result is False:
                    break

    def _show_image_detail(self, item, column):
        texture = self._tree_view_add_opt.get_file(item)
        w = gui_core.GuiDialog.create(
            self._session.gui_name,
            window_size=(512, 512),
            #
            ok_visible=False, no_visible=False,
            tip_visible=False,
            show=False,
            #
            parent=self.widget
        )

        v = gui_prx_widgets.PrxImageView()
        w.add_customize_widget(v)

        v.set_textures([texture])

        w.show_window_auto()
