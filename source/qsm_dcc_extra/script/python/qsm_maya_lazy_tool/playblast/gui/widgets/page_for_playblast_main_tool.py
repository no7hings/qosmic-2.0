# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.animation.core as qsm_mya_anm_core

import qsm_maya.preview.core as qsm_mya_prv_core

import qsm_maya.preview.scripts as qsm_mya_prv_script


class PrxPageForPlayblast(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    RESOLUTION_PRESET_MAPPER = {
        'HD 1080P': (1920, 1080),
        'HD 720P': (1280, 720),
        'HD 540P': (960, 540),
        '640x480': (640, 480),
        '320x240': (320, 240),
        '4k Square': (4096, 4096),
        '3k Square': (3072, 3072),
        '2k Square': (2048, 2048),
        '1k Square': (1024, 1024),
    }

    SCRIPT_JOB_NAME = 'lazy_tool_for_playblast'

    def _do_dcc_register_all_script_jobs(self):
        self._script_job = qsm_mya_core.ScriptJob(
            self.SCRIPT_JOB_NAME
        )
        self._script_job.register(
            self.do_gui_refresh_frame_range,
            self._script_job.EventTypes.FrameRangeChanged
        )
        self._script_job.register_as_attribute_change(
            self.do_gui_refresh_resolution_size_by_render_setting, 'defaultResolution.width'
        )
        self._script_job.register_as_attribute_change(
            self.do_gui_refresh_resolution_size_by_render_setting, 'defaultResolution.height'
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job.destroy()
    
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForPlayblast, self).__init__(*args, **kwargs)
        self._window = window
        self._session = session

        self.gui_setup_page()

    def do_gui_refresh_camera_by_scheme(self):
        scheme = self._camera_scheme_port.get()
        if scheme == 'auto':
            self._camera_path_port.set_locked(True)
            cameras = qsm_mya_core.Cameras.get_all()
            self._camera_path_port.set_options(
                cameras
            )
            self._camera_path_port.set(
                qsm_mya_core.Camera.get_active()
            )
        elif scheme == 'camera_path':
            cameras = qsm_mya_core.Cameras.get_all()
            self._camera_path_port.set_options(
                cameras
            )
            self._camera_path_port.set_locked(False)

    # resolution
    def do_gui_refresh_resolution_by_scheme(self):
        scheme = self._resolution_scheme_port.get()
        if scheme == 'render_setting':
            self._resolution_preset_port.set_locked(True)
            self._resolution_size_port.set_locked(True)
            self.do_gui_refresh_resolution_size_by_render_setting()
        elif scheme == 'resolution_preset':
            self._resolution_preset_port.set_locked(False)
            self._resolution_size_port.set_locked(True)
            self.do_gui_refresh_resolution_size_by_preset()
        elif scheme == 'resolution_size':
            self._resolution_preset_port.set_locked(True)
            self._resolution_size_port.set_locked(False)

    def do_gui_refresh_resolution_size_by_preset(self):
        scheme = self._resolution_scheme_port.get()
        if scheme == 'resolution_preset':
            preset = self._resolution_preset_port.get()
            if preset in self.RESOLUTION_PRESET_MAPPER:
                self._resolution_size_port.set(
                    self.RESOLUTION_PRESET_MAPPER[preset]
                )

    def do_gui_refresh_resolution_size_by_render_setting(self):
        scheme = self._resolution_scheme_port.get()
        if scheme == 'render_setting':
            self._resolution_size_port.set(qsm_mya_core.RenderSettings.get_resolution())

    # frame
    def do_gui_refresh_frame_by_scheme(self):
        scheme = self._frame_scheme_port.get()
        if scheme == 'time_slider':
            self._frame_range_port.set_locked(True)
            self._frame_range_port.set(
                qsm_mya_core.Frame.get_frame_range()
            )
        elif scheme == 'frame_range':
            self._frame_range_port.set_locked(False)

    def do_gui_refresh_frame_range(self):
        scheme = self._frame_scheme_port.get()
        if scheme == 'time_slider':
            self._frame_range_port.set(
                qsm_mya_core.Frame.get_frame_range()
            )

    # output
    def _do_gui_refresh_output_by_save_scheme(self):
        save_scheme = self._output_save_scheme_port.get()
        if save_scheme == 'auto':
            self._output_directory_port.set_locked(True)
            self._output_file_port.set_locked(True)
        elif save_scheme == 'specific_directory':
            self._output_directory_port.set_locked(False)
            self._output_file_port.set_locked(True)
        elif save_scheme == 'specific_file':
            self._output_directory_port.set_locked(True)
            self._output_file_port.set_locked(False)

    def gui_get_camera_path(self):
        scheme = self._camera_scheme_port.get()
        if scheme == 'auto':
            return qsm_mya_core.Camera.get_active()
        elif scheme == 'camera_path':
            return self._camera_path_port.get()

    def gui_get_file_path(self):
        save_scheme = self._output_save_scheme_port.get()
        update_scheme = self._output_save_scheme_port
        if save_scheme == 'auto':
            return qsm_mya_prv_core.Playblast.generate_movie_file_path(update_scheme=update_scheme)
        elif save_scheme == 'specific_directory':
            _ = qsm_mya_prv_core.Playblast.generate_movie_file_path(
                directory_path=self._output_directory_port.get(), update_scheme=update_scheme
            )
            if _ is None:
                self._window.exec_message(
                    'Directory is non exists'
                )
            return _
        elif save_scheme == 'specific_file':
            return self._output_file_port.get()

    def do_dcc_playblast(self):
        movie_path = self.gui_get_file_path()
        if movie_path is None:
            return

        camera_path = self.gui_get_camera_path()
        if camera_path is None:
            return

        resolution_size = self._resolution_size_port.get()
        frame_range = self._frame_range_port.get()
        frame_step = self._prx_options_node.get(
            'frame.step'
        )
        texture_enable = self._prx_options_node.get(
            'render_setting.texture_enable'
        )
        light_enable = self._prx_options_node.get(
            'render_setting.light_enable'
        )
        shadow_enable = self._prx_options_node.get(
            'render_setting.shadow_enable'
        )
        hud_enable = self._prx_options_node.get(
            'display_setting.hud_enable'
        )

        play_enable = self._prx_options_node.get(
            'play_enable'
        )

        q = qsm_mya_anm_core.AdvRigsQuery()

        q.do_update()

        for i in q.get_all():
            i.switch_to_original()

        # noinspection PyBroadException
        try:
            qsm_mya_prv_core.Playblast.execute(
                movie_path,
                camera=camera_path,
                resolution=resolution_size,
                frame=frame_range, frame_step=frame_step,
                texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable,
                show_window=False, play_enable=play_enable,
                hud_enable=hud_enable
            )
        except Exception:
            pass

        finally:
            for i in q.get_all():
                i.switch_to_cache()

    def do_dcc_playblast_backstage(self):
        import lxbasic.web as bsc_web

        import qsm_task.process as qsm_tsk_process

        if qsm_tsk_process.TaskProcessClient.get_server_status():
            movie_path = self.gui_get_file_path()
            if movie_path is None:
                raise RuntimeError()

            camera_path = self.gui_get_camera_path()
            if camera_path is None:
                raise RuntimeError()

            resolution_size = self._resolution_size_port.get()
            frame_range = self._frame_range_port.get()
            frame_step = self._prx_options_node.get(
                'frame.step'
            )
            texture_enable = self._prx_options_node.get(
                'render_setting.texture_enable'
            )
            light_enable = self._prx_options_node.get(
                'render_setting.light_enable'
            )
            shadow_enable = self._prx_options_node.get(
                'render_setting.shadow_enable'
            )
            hud_enable = self._prx_options_node.get(
                'display_setting.hud_enable'
            )

            task_name, file_path, movie_file_path, cmd_script = qsm_mya_prv_script.PlayblastOpt.generate_args(
                camera_path=camera_path, frame=frame_range, frame_step=frame_step, resolution=resolution_size,
                texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
            )

            qsm_tsk_process.TaskProcessClient.new_entity(
                group=None,
                type='playblast',
                name=task_name,
                cmd_script=cmd_script,
                icon_name='application/maya',
                file=file_path,
                output_file=bsc_core.auto_unicode(movie_file_path),
                # must use string
                completed_notice=bsc_web.UrlOptions.to_string(
                    dict(
                        title='通知',
                        message='拍屏结束了, 是否打开视频?',
                        # todo? exec must use unicode
                        ok_python_script='import os; os.startfile("{}".decode("utf-8"))'.format(
                            bsc_core.auto_string(movie_file_path)
                        ),
                        status='normal'
                    )
                )
            )

            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.task_submit_successful')
                ),
                status='correct'
            )
        else:
            self._window.exec_message(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_task_server')
                ),
                status='warning'
            )

    def gui_setup_page(self):
        qt_lot = qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        qt_lot.addWidget(prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.options')
            )
        )
        prx_sca.add_widget(self._prx_options_node)
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.options.parameters')
        )
        # camera
        self._camera_scheme_port = self._prx_options_node.get_port('camera.scheme')
        self._camera_path_port = self._prx_options_node.get_port('camera.path')
        self._camera_scheme_port.connect_input_changed_to(self.do_gui_refresh_camera_by_scheme)

        self.do_gui_refresh_camera_by_scheme()
        # resolution
        self._resolution_scheme_port = self._prx_options_node.get_port('resolution.scheme')
        self._resolution_preset_port = self._prx_options_node.get_port('resolution.preset')
        self._resolution_size_port = self._prx_options_node.get_port('resolution.size')
        self._resolution_scheme_port.connect_input_changed_to(self.do_gui_refresh_resolution_by_scheme)
        self._resolution_preset_port.connect_input_changed_to(self.do_gui_refresh_resolution_size_by_preset)

        self.do_gui_refresh_resolution_by_scheme()
        self.do_gui_refresh_resolution_size_by_preset()
        # frame
        self._frame_scheme_port = self._prx_options_node.get_port('frame.scheme')
        self._frame_range_port = self._prx_options_node.get_port('frame.range')
        self._frame_scheme_port.connect_input_changed_to(self.do_gui_refresh_frame_by_scheme)

        self.do_gui_refresh_frame_by_scheme()
        # output
        self._output_save_scheme_port = self._prx_options_node.get_port('output.save_scheme')
        self._output_update_scheme_port = self._prx_options_node.get_port('output.update_scheme')
        self._output_directory_port = self._prx_options_node.get_port('output.directory')
        self._output_file_port = self._prx_options_node.get_port('output.file')
        self._output_save_scheme_port.connect_input_changed_to(self._do_gui_refresh_output_by_save_scheme)

        self._do_gui_refresh_output_by_save_scheme()
        # tip
        self._tip_prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        prx_sca.add_widget(self._tip_prx_tool_group)
        self._tip_prx_tool_group.set_expanded(True)
        self._tip_prx_tool_group.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.tip')
            )
        )
        self._tip_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        self._tip_prx_tool_group.add_widget(self._tip_prx_text_browser)
        self._tip_prx_text_browser.set_content(
            gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.main.tip')
            )
        )

        tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_lot.addWidget(tool_bar.widget)
        tool_bar.set_expanded(True)

        self._playblast_button = gui_prx_widgets.PrxPressButton()
        tool_bar.add_widget(self._playblast_button)
        self._playblast_button.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.buttons.playblast')
            )
        )
        self._playblast_button.connect_press_clicked_to(self.do_dcc_playblast)

        self._playblast_backstage_button = gui_prx_widgets.PrxPressButton()
        tool_bar.add_widget(self._playblast_backstage_button)
        self._playblast_backstage_button.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.main.buttons.playblast_backstage')
            )
        )
        self._playblast_backstage_button.connect_press_clicked_to(self.do_dcc_playblast_backstage)

        self._do_dcc_register_all_script_jobs()
        self._window.connect_window_close_to(self._do_dcc_destroy_all_script_jobs)

    def do_gui_refresh_all(self, force=False):
        pass
