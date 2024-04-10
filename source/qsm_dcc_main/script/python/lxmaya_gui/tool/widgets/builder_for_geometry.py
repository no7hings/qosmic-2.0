# coding:utf-8
import lxgui.proxy.widgets as prx_widgets


class PnlBuilderForAssetGeometry(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlBuilderForAssetGeometry, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        s = prx_widgets.PrxVScrollArea()
        self.add_widget(s)
        self._options_prx_node = prx_widgets.PrxNode('options')
        s.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )
        # tip
        self._tip_group = prx_widgets.PrxHToolGroup()
        s.add_widget(self._tip_group)
        self._tip_group.set_expanded(True)
        self._tip_group.set_name('tips')
        self._tip_text_browser = prx_widgets.PrxTextBrowser()
        self._tip_group.add_widget(self._tip_text_browser)

        self.post_setup_fnc()

    def post_setup_fnc(self):
        import lxgui.core as gui_core

        import lxresolver.core as rsv_core

        import lxresolver.scripts as rsv_scripts

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

            o.set('geometry.import', self.import_geometry_fnc)
            o.set('geometry_uv_map.import', self.import_geometry_uv_map_fnc)
            self._tip_text_browser.set_content(self._session.gui_configure.get('content'))
        else:
            gui_core.GuiDialog.create(
                session.gui_name,
                content='open a task scene file and retry',
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            #
            self.close_window_later()

    def import_geometry_fnc(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        kwargs = self._options_prx_node.to_dict()

        mya_fnc_objects.FncBuilderForAssetNew(
            option=dict(
                project=self._rsv_task.get('project'),
                asset=self._rsv_task.get('asset'),
                #
                with_geometry=True,
                #
                with_model='model' in kwargs.get('geometry.includes'),
                with_model_dynamic=kwargs.get('geometry.model.mode') == 'dynamic',
                model_space=kwargs.get('geometry.model.space'),
                model_elements=kwargs.get('geometry.model.elements'),
                #
                with_groom='groom' in kwargs.get('geometry.includes'),
                groom_space=kwargs.get('geometry.groom.space'),
                with_groom_grow=kwargs.get('geometry.groom.grow'),
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
                with_geometry='geometry' in kwargs.get('includes'),
                with_geometry_uv_map='geometry_uv_map' in kwargs.get('includes'),
                #
                with_model='model' in kwargs.get('geometry.includes'),
                with_model_dynamic=kwargs.get('geometry.model.mode') == 'dynamic',
                model_space=kwargs.get('geometry.model.space'),
                model_elements=kwargs.get('geometry.model.elements'),
                #
                with_groom='groom' in kwargs.get('geometry.includes'),
                groom_space=kwargs.get('geometry.groom.space'),
                with_groom_grow=kwargs.get('geometry.groom.grow'),
                #
                with_surface=True,
                surface_space=kwargs.get('geometry_uv_map.surface.space'),
            )
        ).execute()