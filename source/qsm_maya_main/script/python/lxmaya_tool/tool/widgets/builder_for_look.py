# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class PnlBuilderForAssetLook(gui_prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlBuilderForAssetLook, self).__init__(session, *args, **kwargs)

    def gui_setup_fnc(self):
        s = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(s)
        self._options_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        s.add_widget(self._options_prx_node)
        self._options_prx_node.build_by_data(
            self._session.configure.get('build.node.options'),
        )
        # tip
        self._tip_prx_tool_group = gui_prx_widgets.PrxHToolGroupA()
        s.add_widget(self._tip_prx_tool_group)
        self._tip_prx_tool_group.set_expanded(True)
        self._tip_prx_tool_group.set_name('tips')
        self._tip_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        self._tip_prx_tool_group.add_widget(self._tip_prx_text_browser)

        self.post_setup_fnc()

    def post_setup_fnc(self):
        import lxresolver.core as rsv_core

        import lxresolver.scripts as rsv_scripts

        import lxgui.core as gui_core

        session = self.session

        env_data = rsv_scripts.ScpEnvironment.get_as_dict()

        self._resolver = rsv_core.RsvBase.generate_root()

        self._rsv_task = self._resolver.get_rsv_task(
            **env_data
        )
        if self._rsv_task is not None:
            self._rsv_project = self._rsv_task.get_rsv_project()
            self._dcc_data = self._rsv_project.get_dcc_data(application='maya')

            o = self._options_prx_node

            o.set('look.import_render', self.import_look_render_fnc)
            o.set('look.import_preview', self.import_look_preview_fnc)
            o.set('geometry_uv_map.import', self.import_geometry_uv_map_fnc)
            self._tip_prx_text_browser.set_content(self._session.gui_configure.get('content'))
        else:
            gui_core.GuiDialog.create(
                session.gui_name,
                content='open a task scene file and retry',
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            #
            self.do_close_window_later()

    def import_look_render_fnc(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_objects.FncBuilderForAssetNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_look=True,
                #
                with_surface=True,
                surface_space=kwargs.get('look.surface.space'),
            )
        ).execute()

    def import_look_preview_fnc(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_objects.FncBuilderForAssetNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_look=True,
                #
                with_surface_preview=True,
                surface_space=kwargs.get('look.surface.space'),
            )
        ).execute()

    def import_geometry_uv_map_fnc(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_objects.FncBuilderForAssetNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry_uv_map=True,
                #
                with_surface=True,
                surface_space=kwargs.get('geometry_uv_map.surface.space'),
            )
        ).execute()

    def apply_fnc(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_objects.FncBuilderForAssetNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry_uv_map='geometry_uv_map' in kwargs.get('includes'),
                #
                with_look='look' in kwargs.get('includes'),
                with_surface_preview=kwargs.get('look.surface.mode') == 'preview',
                #
                with_surface=True,
                surface_space=kwargs.get('geometry_uv_map.surface.space'),
            )
        ).execute()
