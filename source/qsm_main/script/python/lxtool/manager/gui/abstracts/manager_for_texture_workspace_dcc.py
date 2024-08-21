# coding:utf-8
import time

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.core as gui_qt_core

import lxgeneral.dcc.objects as gnl_dcc_objects

import lxsession.commands as ssn_commands

import lxresolver.core as rsv_core

import lxgui.core as gui_core


class _GuiCmdForNewVersion(object):
    def __init__(self, window, session, workspace_opt):
        self._window = window
        self._session = session
        self._workspace_opt = workspace_opt

    def _pull_textures(self, w, from_variant, from_version, to_version):
        directory_path_src_0 = self._workspace_opt.get_src_directory_path_at(
            from_variant, from_version
        )
        directory_path_tx_0 = self._workspace_opt.get_tx_directory_path_at(
            from_variant, from_version
        )

        directory_path_src_1 = self._workspace_opt.get_src_directory_path_at(
            from_variant, to_version
        )
        directory_path_tx_1 = self._workspace_opt.get_tx_directory_path_at(
            from_variant, to_version
        )

        method_args = [
            (self._pull_texture_as_link, (w, directory_path_src_0, directory_path_src_1)),
            (self._pull_texture_as_link, (w, directory_path_tx_0, directory_path_tx_1))
        ]

        with w.gui_progressing(maximum=len(method_args), label='pull textures from "{}"'.format(from_version)) as g_p:
            for i_method, i_args in method_args:
                g_p.do_update()
                i_method(*i_args)

    @classmethod
    def _pull_texture_as_link(cls, w, directory_path_src, directory_path_tgt):
        file_paths_src = bsc_storage.StgDirectoryMtd.get_file_paths(
            directory_path_src
        )
        if file_paths_src:
            with w.gui_progressing(maximum=len(file_paths_src), label='pull texture as link') as g_p:
                for i_file_path in file_paths_src:
                    g_p.do_update()

                    i_texture_src = gnl_dcc_objects.StgTexture(
                        i_file_path
                    )

                    i_texture_src.set_link_to_directory(
                        directory_path_tgt
                    )

    def show_dialog(self):
        def ok_fnc_():
            _directory_paths = v_p_0.get_all(check_only=True)
            if _directory_paths:
                # pull last version first
                _directory_paths.reverse()
                with w.gui_progressing(maximum=len(_directory_paths), label='new version') as g_p:
                    for _i_directory_path in _directory_paths:
                        g_p.do_update()
                        if _i_directory_path in all_directory_paths:
                            _i_directory_opt = bsc_storage.StgDirectoryOpt(_i_directory_path)
                            _i_variant = variant
                            _i_version_from = _i_directory_opt.get_name()
                            _i_version_to = next_version

                            self._pull_textures(
                                w, _i_variant, _i_version_from, _i_version_to,
                            )

                            self._workspace_opt.lock_version_at(
                                _i_variant, _i_version_from
                            )

                # lock may be delay
                time.sleep(2)
                self._window._set_texture_workspace_update_()

        variant = self._window._options_prx_node.get('control.variant')
        next_version = self._workspace_opt.get_new_version_at(variant)

        w = gui_core.GuiDialog.create(
            self._session.gui_name,
            content=(
                'new version:\n'
                '   1. create new version "{}" in variant "{}"\n'
                '   2. pull textures by checked version (use link, when texture is duplicates use latest version)\n'
                '   3. lock version by checked version\n'
                'press "Apply and Close" to continue'
            ).format(
                next_version, variant
            ),
            status=gui_core.GuiDialog.ValidationStatus.Warning,
            #
            options_configure=self._session.configure.get('build.node.new_version'),
            #
            ok_label='Apply and Close',
            #
            ok_method=ok_fnc_,
            #
            no_visible=False,
            show=False,
            #
            parent=self._window.widget,
            window_size=(480, 480),
        )

        n = w.get_options_node()

        v_p_0 = n.get_port('versions')
        root = self._workspace_opt.get_root_at(variant)
        v_p_0.set_root(root)
        all_directory_paths = self._workspace_opt.get_all_directories_at(variant)
        v_p_0.set(all_directory_paths)
        v_p_0.set_all_items_checked(False)
        v_p_0.set_checked_by_include_paths(all_directory_paths[-1])

        w.show_window_auto()


# noinspection PyUnusedLocal
class AbsPnlManagerForTextureSpaceDcc(gui_prx_widgets.PrxSessionWindow):
    GUI_NAMESPACE = None
    DCC_SELECTION_CLS = None
    TEXTURE_WORKSPACE_CLS = None

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlManagerForTextureSpaceDcc, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self._dcc_texture_references = None
        self._dcc_objs = []

        self._create_data = []

        self._is_disable = False

        self._file_path = None

    def gui_setup_fnc(self):
        self.set_main_style_mode(1)
        self._prx_tab_view = gui_prx_widgets.PrxTabView()
        self.add_widget(self._prx_tab_view)

        s_0 = gui_prx_widgets.PrxVScrollArea()
        self._prx_tab_view.add_widget(
            s_0,
            name='workspace',
            icon_name_text='workspace',
        )

        self._options_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        s_0.add_widget(self._options_prx_node)
        self._options_prx_node.build_by_data(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.set(
            'control.new_version', self._set_wsp_version_new_
        )
        self._options_prx_node.get_port(
            'control.variant'
        ).connect_input_changed_to(
            self._set_wsp_texture_directories_update_
        )

        self._options_prx_node.set(
            'control.lock_all_version', self._set_wsp_all_version_lock_
        )

        self._options_prx_node.set(
            'texture.create.execute', self._set_wsp_tx_create_execute_
        )

        self._options_prx_node.set(
            'texture.create.execute_us_deadline', self._set_wsp_tx_create_execute_by_deadline_
        )

        self._options_prx_node.set(
            'refresh', self._set_texture_workspace_update_
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )

        self.set_refresh_all()

    def _set_dcc_scene_update_(self):
        self._file_path = None

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = None

    def _set_dcc_objs_update_(self):
        self._dcc_objs = []

    def _set_texture_workspace_update_(self):
        import qsm_prc_general.rsv.objects as gnl_rsv_objects

        self._rsv_workspace_texture_opt = gnl_rsv_objects.RsvAssetTextureOpt(self._rsv_task)
        current_variant = 'main'
        self._rsv_workspace_texture_opt.set_current_variant(current_variant)
        if self._set_workspace_check_(current_variant) is True:
            self._options_prx_node.set(
                'resolver.task', self._rsv_task.path
            )

            self._options_prx_node.set(
                'control.variant', [current_variant]
            )

            self._options_prx_node.set(
                'control.variant', current_variant
            )
            #
            self._set_wsp_texture_directories_update_()

    def _set_wsp_texture_directories_update_(self):
        variant = self._options_prx_node.get(
            'control.variant'
        )
        unlocked_versions = self._rsv_workspace_texture_opt.get_all_unlocked_versions_at(
            variant
        )
        if unlocked_versions:
            self._options_prx_node.set(
                'texture.directories',
                [self._rsv_workspace_texture_opt.get_directory_path_at(variant, i) for i in unlocked_versions]
            )
        else:
            if unlocked_versions:
                self._options_prx_node.set(
                    'texture.directories',
                    []
                )

    def _set_workspace_check_(self, current_variant):
        def ok_fnc_():
            self._rsv_workspace_texture_opt.set_version_create_at(
                current_variant, 'new'
            )

        self._is_disable = True

        directory_path = self._rsv_workspace_texture_opt.get_directory_path_at(
            current_variant, 'latest'
        )
        if directory_path:
            return True
        else:
            w = gui_core.GuiDialog.create(
                self._session.gui_name,
                content='workspace is not install in variant "{}", press "Apply and Close" to continue'.format(
                    current_variant
                ),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Apply and Close',
                #
                ok_method=ok_fnc_,
                #
                no_visible=False,
                # show=False,
                parent=self.widget,
                window_size=(480, 480),
            )
            result = w.get_result()
            if result is True:
                return True
            else:
                self._is_disable = True
                self.close_window()

    def _set_wsp_version_new_(self):
        _GuiCmdForNewVersion(
            self, self._session, self._rsv_workspace_texture_opt
        ).show_dialog()

    def _set_wsp_all_version_lock_(self):
        def ok_fnc_():
            if unlocked_directory_paths:
                with bsc_log.LogProcessContext.create(
                    maximum=len(unlocked_directory_paths), label='lock version directory'
                ) as g_p:
                    for _i in unlocked_directory_paths:
                        bsc_storage.StgPermissionMtd.lock(_i)
                        g_p.do_update()
            #
            time.sleep(2)
            self._set_texture_workspace_update_()

        self._set_dcc_texture_references_update_()
        self._set_dcc_objs_update_()

        directory_paths = self._rsv_workspace_texture_opt.get_all_directories(
            self._dcc_objs
        )

        unlocked_directory_paths = [i for i in directory_paths if bsc_storage.StgPath.get_is_writeable(i) is True]
        if unlocked_directory_paths:
            w = gui_core.GuiDialog.create(
                self._session.gui_name,
                sub_label='Lock All Version',
                content='lock all texture directories(used and matched "texture workspace" rule), press "Apply and Close" to continue',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                options_configure=self._session.configure.get('build.node.lock_all_version'),
                #
                ok_label='Apply and Close',
                #
                ok_method=ok_fnc_,
                #
                no_visible=False,
                show=False,
                #
                parent=self.widget,
                window_size=(480, 480)
            )

            w.get_options_node().set(
                'directories', unlocked_directory_paths
            )

            w.show_window_auto()
        else:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'all texture directories(used and matched "texture workspace" rule) is locked',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )

    def set_refresh_all(self):
        self._set_dcc_scene_update_()
        #
        if self._file_path is not None:
            self._resolver = rsv_core.RsvBase.generate_root()
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
                self._file_path
            )
            if self._rsv_scene_properties:
                self._rsv_task = self._resolver.get_rsv_task_by_any_file_path(
                    self._file_path
                )
                self._rsv_entity = self._rsv_task.get_rsv_resource()

                self._set_texture_workspace_update_()

    def _set_tx_create_data_update_(self, directory_paths, force_enable=False, ext_tgt='.tx'):
        self._create_data = []
        with bsc_log.LogProcessContext.create(maximum=len(directory_paths), label='create texture-tx in directory') as g_p:
            for i_directory_path in directory_paths:
                i_directory_path_src = '{}/src'.format(i_directory_path)
                i_directory_path_tgt = '{}/{}'.format(i_directory_path, ext_tgt[1:])
                self._set_tx_create_data_update_at_(
                    i_directory_path_src, i_directory_path_tgt,
                    force_enable, ext_tgt,
                )
                g_p.do_update()

    def _set_tx_create_data_update_at_(self, directory_path_src, directory_path_tgt, force_enable=False, ext_tgt='.tx'):
        file_paths_src = bsc_storage.StgDirectoryMtd.get_file_paths(
            directory_path_src
        )
        if file_paths_src:
            with bsc_log.LogProcessContext.create(maximum=len(file_paths_src), label='texture-tx create running') as g_p:
                for i_file_path in file_paths_src:
                    i_texture_src = gnl_dcc_objects.StgTexture(
                        i_file_path
                    )
                    if i_texture_src.ext != ext_tgt:
                        if force_enable is True:
                            self._create_data.append(
                                (i_texture_src.path, directory_path_tgt)
                            )
                        else:
                            if i_texture_src.get_is_exists_as_tgt_ext(
                                    ext_tgt,
                                    directory_path_tgt
                            ) is False:
                                self._create_data.append(
                                    (i_texture_src.path, directory_path_tgt)
                                )
                    #
                    g_p.do_update()

    def _set_tx_create_by_data_(self, button, post_fnc=None):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            # print '\n'.join(results)

        def status_update_at_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            for i_index, (i_file_path, i_output_directory_path) in enumerate(self._create_data):
                bsc_storage.StgPath.create_directory(
                    i_output_directory_path
                )

                # print i_file_path, i_output_directory_path

                i_cmd = gnl_dcc_objects.StgTexture._get_unit_tx_create_cmd_by_src_force_(
                    i_file_path,
                    search_directory_path=i_output_directory_path,
                )
                if button.get_is_stopped():
                    break
                #
                if i_cmd:
                    bsc_core.TrdCommandPool.do_pool_wait()
                    i_t = bsc_core.TrdCommandPool.set_start(i_cmd, i_index)
                    i_t.status_changed.connect_to(status_update_at_fnc_)
                    i_t.finished.connect_to(finished_fnc_)
                else:
                    status_update_at_fnc_(
                        i_index, button.Status.Completed
                    )
                    finished_fnc_(
                        i_index, button.Status.Completed
                    )

        def quit_fnc_():
            button.set_stopped()
            #
            time.sleep(1)
            #
            t.quit()
            t.wait()
            t.deleteLater()

        contents = []
        if self._create_data:
            button.set_stopped(False)

            c = len(self._create_data)

            button.set_status(button.Status.Started)
            button.initialization(c, button.Status.Started)

            t = gui_qt_core.QtMethodThread(self.widget)
            t.append_method(
                run_fnc_
            )
            if post_fnc is not None:
                t.run_finished.connect(
                    post_fnc
                )
            t.start()

            self.register_window_close_method(quit_fnc_)
        else:
            button.restore_all()

            contents = [
                'non-texture(s) for create'
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

    def _set_wsp_tx_create_execute_(self):
        force_enable = self._options_prx_node.get('texture.create.force_enable')
        ext_tgt = '.tx'
        button = self._options_prx_node.get_port('texture.create.execute')
        directory_paths = self._options_prx_node.get('texture.directories')
        if directory_paths:
            method_args = [
                (self._set_tx_create_data_update_, (directory_paths, force_enable, ext_tgt)),
                (self._set_tx_create_by_data_, (button,))
            ]
            with bsc_log.LogProcessContext.create(maximum=len(method_args), label='texture-tx create processing') as g_p:
                for i_fnc, i_args in method_args:
                    g_p.do_update()
                    #
                    i_result = i_fnc(*i_args)
                    if i_result is False:
                        break
        else:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content='non-directory(s) for create',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )

    def _set_wsp_tx_create_execute_by_deadline_(self):
        force_enable = self._options_prx_node.get('texture.create.force_enable')
        ext_tgt = '.tx'
        directory_paths = self._options_prx_node.get('texture.directories')
        if directory_paths:
            directory_paths_src = ['{}/src'.format(i) for i in directory_paths]
            directory_paths_tgt = ['{}/{}'.format(i, ext_tgt[1:]) for i in directory_paths]

            j_option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key='methods/texture/texture-convert',
                    #
                    directories=directory_paths_src,
                    output_directories=directory_paths_tgt,
                    #
                    force_enable=force_enable,
                    #
                    target_ext=ext_tgt,
                    width=None,
                    #
                    td_enable=self._session.get_is_td_enable(),
                    rez_beta=self._session.get_is_beta_enable(),
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
        else:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content='non-directory(s) for create',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
