# coding:utf-8
import copy

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxresolver.core as rsv_core

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.core as gui_core

import lxsession.commands as ssn_commands

import lxsession.core as ssn_core
# publish
from ... import core as pbs_core


class _PublishOptForGeneral(object):
    VERSION_NAME_PATTERN = '{project}.{resource}.{task}.{version}'

    def __init__(self, window, session, rsv_task, version_properties, options):
        self._window = window
        self._session = session
        self._rsv_task = rsv_task
        self._version_properties = version_properties
        self._options = options

        self._version_name = self.VERSION_NAME_PATTERN.format(
            **self._version_properties.get_value()
        )
        self._review_mov_file_path = None

        self._maya_scene_src_file_paths = []
        self._katana_scene_src_file_paths = []

    def create_or_unlock_version_directory_fnc(self):
        directory_path = self._options.get('version_directory')
        if bsc_storage.StgDirectoryOpt(directory_path).get_is_exists() is False:
            bsc_storage.StgPermissionMtd.create_directory(
                directory_path
            )

    def pre_fnc(self):
        self.create_or_unlock_version_directory_fnc()

    def get_scene_src_file_path(self):
        keyword = '{branch}-maya-scene-src-file'
        rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        return rsv_unit.get_result(
            version=self._version_properties.get('version')
        )

    def collection_review_fnc(self):
        self._review_mov_file_path = None
        #
        file_paths = self._options['review']
        movie_file_path = None
        if file_paths:
            movie_file_path = pbs_core.VideoComp.comp_movie(
                file_paths
            )
        #
        if movie_file_path:
            version = self._version_properties.get('version')
            review_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-review-file'
            )
            review_file_path = review_file_rsv_unit.get_result(
                version=version
            )
            #
            bsc_storage.StgPermissionMtd.copy_to_file(
                movie_file_path, review_file_path
            )
            self._review_mov_file_path = movie_file_path

    def collection_scene_src_fnc(self):
        self._maya_scene_src_file_paths = []
        self._katana_scene_src_file_paths = []
        #
        count_dict = {}
        file_paths = self._options.get('extra.scene')
        if file_paths:
            version = self._version_properties.get('version')
            with self._window.gui_progressing(maximum=len(file_paths), label='export scene') as g_p:
                for i_index, i_file_path in enumerate(file_paths):
                    g_p.do_update()
                    i_file_opt = bsc_storage.StgFileOpt(i_file_path)
                    if i_file_opt.get_is_file():
                        i_ext = i_file_opt.get_ext()
                        if i_ext in count_dict:
                            i_c = len(count_dict[i_ext])
                        else:
                            i_c = 0

                        if i_ext == '.ma':
                            i_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-maya-scene-src-file'
                            )
                        elif i_ext == '.katana':
                            i_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
                                keyword='{branch}-katana-scene-src-file'
                            )
                        else:
                            raise RuntimeError()
                        #
                        i_scene_src_file_path_tgt = i_scene_src_file_rsv_unit.get_result(
                            version=version
                        )
                        if i_c > 0:
                            i_scene_src_file_path_opt_tgt = bsc_storage.StgFileOpt(
                                i_scene_src_file_path_tgt
                            )
                            i_scene_src_file_path_tgt = '{}.{}{}'.format(
                                i_scene_src_file_path_opt_tgt.get_path_base(),
                                i_c,
                                i_scene_src_file_path_opt_tgt.get_ext()
                            )
                        #
                        if i_ext == '.ma':
                            self._maya_scene_src_file_paths.append(i_scene_src_file_path_tgt)
                        elif i_ext == '.katana':
                            self._katana_scene_src_file_paths.append(i_scene_src_file_path_tgt)
                        #
                        count_dict.setdefault(
                            i_ext, []
                        ).append(i_file_path)
                        if i_file_opt.get_is_readable() is False:
                            bsc_storage.StgPermissionMtd.unlock(i_file_path)
                        #
                        i_file_opt.copy_to_file(
                            i_scene_src_file_path_tgt
                        )

    def collection_image_fnc(self):
        file_paths = self._options.get('extra.image')
        if file_paths:
            version = self._version_properties.get('version')
            image_directory_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword='{branch}-image-dir'
            )
            image_directory_path = image_directory_rsv_unit.get_result(
                version=version
            )
            with self._window.gui_progressing(maximum=len(file_paths), label='export image') as g_p:
                for i_index, i_file_path in enumerate(file_paths):
                    g_p.do_update()
                    i_file_tile_paths = bsc_storage.StgFileTiles.get_tiles(i_file_path)
                    for j_file_path in i_file_tile_paths:
                        j_file_opt = bsc_storage.StgFileOpt(j_file_path)
                        j_file_path_tgt = '{}/{}'.format(
                            image_directory_path, j_file_opt.get_name()
                        )
                        if j_file_opt.get_is_readable() is False:
                            bsc_storage.StgPermissionMtd.unlock(j_file_path)
                        #
                        j_file_opt.copy_to_file(
                            j_file_path_tgt
                        )

    def farm_process_fnc(self):
        file_path = self.get_scene_src_file_path()
        #
        extra_data = dict(
            user=bsc_core.BscSystem.get_user_name(),
            #
            version_type=self._options['version_type'],
            version_status='pub',
            description=self._options['description'],
            notice=self._options['notice'],
        )
        #
        extra_key = ssn_core.SsnHookFileMtd.set_extra_data_save(extra_data)
        #
        option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key='rsv-task-batchers/asset/gen-any-export-build',
                # choice_scheme='asset-maya-create-and-publish',
                choice_scheme='asset-maya-publish',
                #
                file=file_path,
                #
                extra_key=extra_key,
                maya_scene_srcs=self._maya_scene_src_file_paths,
                katana_scene_srcs=self._katana_scene_src_file_paths,
                movie_file=self._review_mov_file_path,
                # settings for any export
                with_scene=self._options.get('process.settings.with_scene'),
                #
                with_render_texture=self._options.get('process.settings.with_render_texture'),
                with_preview_texture=self._options.get('process.settings.with_preview_texture'),
                #
                with_look_yml=self._options.get('process.settings.with_look_yml'),
                #
                with_camera_abc=self._options.get('process.settings.with_camera_abc'),
                with_camera_usd=self._options.get('process.settings.with_camera_usd'),
                #
                td_enable=self._session.get_is_td_enable(),
                rez_beta=self._session.get_is_beta_enable(),
            )
        )
        #
        ssn_commands.execute_option_hook_by_deadline(
            option=option_opt.to_string()
        )

    @bsc_core.MdfBaseMtd.run_with_exception_catch
    def execute(self):
        fncs = [
            self.pre_fnc,
            self.collection_review_fnc,
            self.collection_scene_src_fnc,
            self.collection_image_fnc,
            #
            self.farm_process_fnc,
        ]
        with self._window.gui_progressing(maximum=len(fncs), label='execute publish process') as g_p:
            for i_fnc in fncs:
                g_p.do_update()
                i_fnc()
        #
        self._window.show_message(
            'publish process is complected',
            self._window.ValidationStatus.Correct
        )


class AbsPnlPublisherForGeneral(gui_prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlPublisherForGeneral, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self.__task_data = {}
        #
        self.__stg_user = None
        self.__stg_task = None
        #
        self._rsv_project = None
        self._rsv_task = None
        self._step_mapper = dict()
        self._version_properties = None

    def gui_setup_fnc(self):
        sa_1 = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(sa_1)

        self.__input = gui_prx_widgets.PrxInputAsStgTask()
        sa_1.add_widget(self.__input)

        self.__input.set_focus_in()

        self.__tip = gui_prx_widgets.PrxTextBrowser()
        sa_1.add_widget(self.__tip)
        self.__tip.set_focus_enable(False)

        self.__next_button = gui_prx_widgets.PrxPressButton()
        self.__next_button.set_name('next')
        self.add_button(self.__next_button)
        self.__next_button.connect_press_clicked_to(self.__do_next)
        self.__next_button.set_enable(False)

        self.__input.connect_result_to(self.__do_accept)
        self.__input.connect_tip_trace_to(self.__do_tip_accept)

        self.__input.setup()
        # publish
        layer_widget = self.create_layer_widget('publish', 'Publish')
        sa_2 = gui_prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(sa_2)
        self._publish_options_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        sa_2.add_widget(self._publish_options_prx_node)
        self._publish_options_prx_node.build_by_data(
            self._session.configure.get('build.node.publish_options')
        )

        self._publish_options_prx_node.get_port('version_scheme').connect_input_changed_to(
            self.refresh_publish_version_directory
        )

        self._publish_tip = gui_prx_widgets.PrxTextBrowser()
        sa_2.add_widget(self._publish_tip)
        self._publish_tip.set_content(
            self._session.configure.get('build.node.publish_content')
        )
        self._publish_tip.set_font_size(12)

        tool_bar = gui_prx_widgets.PrxHToolBar()
        layer_widget.add_widget(tool_bar)
        tool_bar.set_expanded(True)

        self._publish_button = gui_prx_widgets.PrxPressButton()
        tool_bar.add_widget(self._publish_button)
        self._publish_button.set_name('publish')
        self._publish_button.connect_press_clicked_to(
            self.execute_publish
        )

        self.refresh_all_fnc()

    def __do_tip_accept(self, text):
        if self.__input.is_valid():
            self.__next_button.set_enable(True)
        else:
            self.__next_button.set_enable(False)

        self.__tip.set_content(text)

    def __do_accept(self, dict_):
        if dict_:
            task_id = dict_['task_id']
            self.__stg_task = self._stg_connector.get_stg_task(id=task_id)
            self.__task_data = self._stg_connector.get_data_from_task_id(
                str(dict_['task_id'])
            )
            if self.validator_fnc() is True:
                self.switch_current_layer_to('publish')
                self.get_layer_widget('publish').set_name(
                    'publish for [{project}.{resource}.{task}]'.format(
                        **self.__task_data
                    )
                )
                fncs = [
                    self.refresh_publish_options,
                    self.refresh_publish_version_directory,
                    self.refresh_publish_notice,
                    self.refresh_publish_scene,
                    self.refresh_publish_process_settings,
                ]
                #
                with self.gui_progressing(maximum=len(fncs), label='execute refresh process') as g_p:
                    for i_fnc in fncs:
                        g_p.do_update()
                        i_fnc()

    def __do_next(self):
        self.__do_accept(self.__input.get_result())

    def refresh_all_fnc(self):
        import lxbasic.shotgun as bsc_shotgun

        self._stg_connector = bsc_shotgun.StgConnector()
        self._user_name = bsc_core.BscSystem.get_user_name()
        self.__stg_user = self._stg_connector.get_stg_user(user=self._user_name)
        if not self.__stg_user:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content='user "{}" is not available'.format(self._user_name),
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            self.do_close_window_later()
            return

        task_id = bsc_core.EnvBaseMtd.get(
            'QSM_TASK_ID'
        )
        if task_id:
            self.__input.setup_from_task_id(task_id)
            self.__do_accept(dict(task_id=task_id))
        else:
            pass

    def refresh_publish_notice(self):
        def post_fnc_():
            pass

        def cache_fnc_():
            import lxbasic.shotgun as bsc_shotgun

            t_o = bsc_shotgun.StgTaskOpt(self._stg_connector.to_query(stg_task))
            notice_stg_users = t_o.get_notice_stg_users()
            return list(set([self._stg_connector.to_query(i).get('name').decode('utf-8') for i in notice_stg_users]))

        def built_fnc_(user_names):
            self._publish_options_prx_node.set(
                'notice', user_names
            )

        p = self._publish_options_prx_node.get_port('notice')
        p.set_clear()
        p.set_shotgun_entity_kwargs(
            dict(
                entity_type='HumanUser',
                filters=[
                    ['sg_studio', 'is', 'CG'],
                    ['sg_status_list', 'is', 'act']
                ],
                fields=['name', 'email', 'sg_nickname']
            ),
            name_field='name',
            keyword_filter_fields=['name', 'email', 'sg_nickname'],
            tag_filter_fields=['department']
        )

        stg_task = self.__stg_task

        p.run_build_extra_use_thread(
            cache_fnc_, built_fnc_, post_fnc_
        )

    def create_task_directory(self):
        if self.__task_data:
            keyword = '{branch}-release-task-dir'.format(**self.__task_data)
            task_directory_pattern = self._rsv_project.get_pattern(
                keyword
            )
            kwargs = copy.copy(self._rsv_project.properties.get_value())
            kwargs['workspace'] = self._rsv_project.to_workspace(
                self._rsv_project.WorkspaceKeys.Release
            )
            kwargs.update(self.__task_data)
            task_directory_path = task_directory_pattern.format(
                **kwargs
            )
            if bsc_storage.StgPath.get_is_exists(task_directory_path) is False:
                bsc_storage.StgPermissionMtd.create_directory(
                    task_directory_path
                )

    def validator_fnc(self):
        if self.__task_data:
            self._resolver = rsv_core.RsvBase.generate_root()
            self._rsv_project = self._resolver.get_rsv_project(
                **self.__task_data
            )
            if self._rsv_project is None:
                gui_core.GuiDialog.create(
                    self.session.gui_name,
                    content='project is not available',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    #
                    ok_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )
                return False
            #
            self._step_mapper = self._rsv_project.properties.get(
                '{}_steps'.format(self.__task_data.get('branch'))
            )
            #
            self._rsv_task = self._resolver.get_rsv_task(
                **self.__task_data
            )
            if self._rsv_task is None:
                w = gui_core.GuiDialog.create(
                    self.session.gui_name,
                    content='task directory is non-exists, press "Ok" to create and continue',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    ok_method=self.create_task_directory,
                    # do not use thread
                    # use_thread=False
                )
                result = w.get_result()
                if result is True:
                    self._rsv_task = self._resolver.get_rsv_task(
                        **self.__task_data
                    )
                return result
            return True
        return False

    def refresh_publish_version_directory(self):
        version_scheme = self._publish_options_prx_node.get('version_scheme')
        #
        branch = self._rsv_task.properties.get('branch')
        self._step_mapper = self._rsv_project.properties.get('{}_steps'.format(branch))
        #
        version_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='{branch}-release-version-dir'
        )
        version_directory_path = version_directory_rsv_unit.get_result(
            version=version_scheme
        )
        self._publish_options_prx_node.set(
            'version_directory', version_directory_path
        )
        self._version_properties = version_directory_rsv_unit.generate_properties_by_result(
            version_directory_path
        )
        self._version_properties.update_from(self.__task_data)
        self._version_properties.set('user', self._user_name)

    def refresh_publish_options(self):
        self._publish_options_prx_node.set('version_type', 'daily')
        self._publish_options_prx_node.set('version_scheme', 'new')
        self._publish_options_prx_node.set('description', '')
        self._publish_options_prx_node.get_port('review').set_clear()
        self._publish_options_prx_node.get_port('extra.scene').set_clear()
        self._publish_options_prx_node.get_port('extra.image').set_clear()
        self._publish_options_prx_node.set(
            'process.settings.with_scene', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_render_texture', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_preview_texture', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_look_yml', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_camera_abc', False
        )
        self._publish_options_prx_node.set(
            'process.settings.with_camera_usd', False
        )

    def refresh_publish_scene(self):
        if bsc_core.BasApplication.get_is_dcc():
            if bsc_core.BasApplication.get_is_maya():
                import lxmaya.dcc.objects as mya_dcc_objects

                self._publish_options_prx_node.set(
                    'extra.scene', [mya_dcc_objects.Scene.get_current_file_path()]

                )
            elif bsc_core.BasApplication.get_is_katana():
                import lxkatana.dcc.objects as ktn_dcc_objects

                self._publish_options_prx_node.set(
                    'extra.scene', [ktn_dcc_objects.Scene.get_current_file_path()]

                )

    def refresh_publish_process_settings(self):
        step = self.__task_data['step']
        if self._step_mapper:
            if step in {self._step_mapper.get('surface')}:
                self._publish_options_prx_node.set(
                    'process.settings.with_scene', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_preview_texture', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_look_yml', True
                )
            elif step in {self._step_mapper.get('camera')}:
                self._publish_options_prx_node.set(
                    'process.settings.with_scene', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_camera_abc', True
                )
                self._publish_options_prx_node.set(
                    'process.settings.with_camera_usd', True
                )

    def __do_next_(self):
        if self.__next_button.get_is_enable() is True:
            self.__task_data = self._stg_connector.get_data_from_task_id(
                str(self.__stg_task['id'])
            )
            if self.validator_fnc() is True:
                self.switch_current_layer_to('publish')
                self.get_layer_widget('publish').set_name(
                    'publish for [{project}.{resource}.{task}]'.format(
                        **self.__task_data
                    )
                )
                fncs = [
                    self.refresh_publish_options,
                    self.refresh_publish_version_directory,
                    self.refresh_publish_notice,
                    self.refresh_publish_scene,
                    self.refresh_publish_process_settings,
                ]
                #
                with self.gui_progressing(maximum=len(fncs), label='execute refresh process') as g_p:
                    for i_fnc in fncs:
                        g_p.do_update()
                        i_fnc()

    def execute_publish(self):
        p = _PublishOptForGeneral(
            self,
            self._session,
            self._rsv_task,
            self._version_properties,
            self._publish_options_prx_node.to_dict()
        )
        p.execute()
